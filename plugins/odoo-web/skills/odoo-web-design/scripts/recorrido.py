"""Paso 1 del recorrido como usuario: rastrea el sitio publicado SIN sesión (como un visitante) y arma el
inventario de páginas, enlaces, botones y formularios que después se recorre a mano en el navegador.

  python recorrido.py https://cliente.odoo.com [--max 80] [--salida recorrido] [--incluir-tienda]

Descubre páginas desde /sitemap.xml, el menú, el footer y los enlaces internos (hasta --max páginas).
Prueba TODOS los enlaces internos y externos (estado HTTP y redirección) una sola vez cada uno.
Salida:
  recorrido/inventario.json   páginas, enlaces con su estado, formularios, botones de acción
  recorrido/reporte.md        reporte para llenar durante el recorrido en el navegador (paso 2)
No necesita API key. No envía formularios ni agrega nada al carrito.
"""
import argparse, json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser

UA = {'User-Agent': 'Mozilla/5.0 (owd-recorrido)', 'Accept-Language': 'es-MX,es;q=0.9'}
OMITIR = re.compile(r'^/(web|my|odoo|website/(?!social)|shop/(cart|checkout|address|payment|confirmation|wishlist|compare)|'
                    r'@/|logout|im_livechat|mail/|payment/|report/|sitemap|robots|website/info)')


def pedir(url, metodo='GET', cuerpo=True):
    req = urllib.request.Request(url, headers=UA, method=metodo)
    t = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=40)
        data = r.read() if cuerpo else b''
        return r.status, r.geturl(), data, r.headers.get('Content-Type', ''), round(time.time() - t, 2)
    except urllib.error.HTTPError as e:
        return e.code, url, b'', '', round(time.time() - t, 2)
    except Exception as e:
        return 0, url, str(e).encode(), '', round(time.time() - t, 2)


class Pagina(HTMLParser):
    def __init__(s):
        super().__init__(); s.enlaces = []; s.forms = []; s.botones = []; s.titulo = ''; s._t = False; s._a = None; s._b = None; s.zona = []
        s.meta = {}; s.h1 = 0; s.imgs = 0; s.imgs_sin_alt = 0

    def handle_starttag(s, t, at):
        a = dict(at)
        if t in ('header', 'footer'):
            s.zona.append('footer-plantilla' if (t == 'footer' and a.get('id') == 'bottom') else t)
        if t == 'title': s._t = True
        if t == 'meta': s.meta[a.get('name') or a.get('property') or ''] = a.get('content', '')
        if t == 'h1': s.h1 += 1
        if t == 'img':
            s.imgs += 1
            if a.get('alt') is None: s.imgs_sin_alt += 1
        if t == 'a' and a.get('href'):
            cls = a.get('class') or ''
            control = bool(a.get('data-bs-toggle') or a.get('role') == 'button' or re.search(r's_website_form_send|dropdown-toggle|o_add_wishlist|js_', cls))
            z = s.zona[-1] if s.zona else 'contenido'
            s._a = {'href': a['href'], 'texto': '', 'nueva': a.get('target') == '_blank', 'control': control, 'zona': z}
        if t == 'form':
            s.forms.append({'id': a.get('id', ''), 'action': a.get('action', ''), 'modelo': a.get('data-model_name', ''), 'campos': []})
        if t in ('input', 'textarea', 'select') and s.forms and a.get('type') != 'hidden' and a.get('name'):
            s.forms[-1]['campos'].append(a['name'] + ('*' if 'required' in a else ''))
        if t == 'button':
            s._b = {'texto': '', 'tipo': a.get('type', 'button')}

    def handle_endtag(s, t):
        if t == 'title': s._t = False
        if t in ('header', 'footer') and s.zona: s.zona.pop()
        if t == 'a' and s._a is not None:
            s._a['texto'] = re.sub(r'\s+', ' ', s._a['texto']).strip()[:60]; s.enlaces.append(s._a); s._a = None
        if t == 'button' and s._b is not None:
            s._b['texto'] = re.sub(r'\s+', ' ', s._b['texto']).strip()[:60]; s.botones.append(s._b); s._b = None

    def handle_data(s, d):
        if s._t: s.titulo += d
        if s._a is not None: s._a['texto'] += d
        if s._b is not None: s._b['texto'] += d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base')
    ap.add_argument('--max', type=int, default=80)
    ap.add_argument('--salida', default='recorrido')
    ap.add_argument('--incluir-tienda', action='store_true', help='rastrea también categorías y productos de /shop')
    a = ap.parse_args()
    base = a.base.rstrip('/')
    host = urllib.parse.urlparse(base).netloc

    def normal(href, desde):
        u = urllib.parse.urlparse(urllib.parse.urljoin(desde, href))
        if u.scheme not in ('http', 'https'): return None
        return u._replace(fragment='').geturl()

    def es_pagina(url):
        u = urllib.parse.urlparse(url)
        if u.netloc != host or OMITIR.match(u.path) or re.search(r'\.(pdf|jpe?g|png|webp|svg|gif|zip|xml|txt|ico|css|js)$', u.path, re.I):
            return False
        if u.query and not a.incluir_tienda:   # /shop?order=…, filtros: misma página
            return False
        if u.path.startswith('/shop') and not a.incluir_tienda and u.path not in ('/shop',):
            return False
        if re.match(r'^/[a-z]{2}(_[A-Z]{2})?/', u.path):  # versiones en otro idioma: se revisan aparte
            return False
        return True

    cola = [base + '/']
    st, _, sm, _, _ = pedir(base + '/sitemap.xml')
    if st == 200:
        for loc in re.findall(rb'<loc>([^<]+)</loc>', sm):
            u = loc.decode().strip()
            if es_pagina(u): cola.append(u)
    vistas, paginas, todos = set(), [], {}
    while cola and len(paginas) < a.max:
        url = cola.pop(0)
        clave = url if a.incluir_tienda else url.split('?')[0].rstrip('/') or url
        if clave in vistas: continue
        vistas.add(clave)
        st, final, html, ct, seg = pedir(url)
        p = Pagina()
        if 'html' in ct:
            p.feed(html.decode('utf-8', 'replace'))
        ruta = urllib.parse.urlparse(url).path or '/'
        info = {'ruta': ruta, 'estado': st, 'final': urllib.parse.urlparse(final).path if final != url else '', 'segundos': seg,
                'titulo': p.titulo.strip(), 'descripcion': p.meta.get('description', ''), 'h1': p.h1, 'imagenes': p.imgs,
                'imagenes_sin_alt': p.imgs_sin_alt, 'kb': len(html) // 1024, 'formularios': p.forms,
                'botones': [b for b in p.botones if b['texto']], 'enlaces': []}
        for e in p.enlaces:
            h = e['href']
            if h.startswith(('mailto:', 'tel:', 'sms:')):
                info['enlaces'].append({**e, 'destino': h, 'tipo': 'contacto'}); continue
            if h in ('#', '') or h.startswith('javascript:'):
                if not e['control']: info['enlaces'].append({**e, 'destino': h, 'tipo': 'vacio'})
                continue
            if h.startswith('#'):
                info['enlaces'].append({**e, 'destino': h, 'tipo': 'ancla'}); continue
            d = normal(h, final)
            if not d: continue
            interno = urllib.parse.urlparse(d).netloc == host
            info['enlaces'].append({**e, 'destino': d, 'tipo': 'interno' if interno else 'externo'})
            todos.setdefault(d, set()).add(ruta)
            if interno and es_pagina(d) and (d.split('?')[0].rstrip('/') or d) not in vistas: cola.append(d)
        paginas.append(info)
        print(f'{st} {ruta}  ({len(info["enlaces"])} enlaces, {len(p.forms)} formularios, {seg}s)')

    # estado de cada enlace (una vez cada uno)
    def probar(d):
        u = urllib.parse.urlparse(d)
        if u.netloc == host:
            st, fin, _, _, _ = pedir(d, cuerpo=False)
        else:
            st, fin, _, _, _ = pedir(d, 'HEAD', cuerpo=False)
            if st in (0, 403, 405, 429): st, fin, _, _, _ = pedir(d, cuerpo=False)
        return d, st, fin
    def agregar_roto(p, e, motivo):
        global_ = e['zona'] in ('header', 'footer', 'footer-plantilla')
        k = (e['zona'] if global_ else p['ruta'], e['texto'], e['destino'])
        if k in vistos_rotos: return
        vistos_rotos.add(k)
        donde = {'header': 'header (todas)', 'footer': 'footer (todas)', 'footer-plantilla': 'footer de la plantilla, oculto pero en el HTML (todas)'}.get(e['zona'], p['ruta'])
        rotos.append((donde, e['texto'], e['destino'], motivo))

    with ThreadPoolExecutor(8) as ex:
        estados = {d: (st, fin) for d, st, fin in ex.map(probar, todos)}
    rotos, vistos_rotos = [], set()
    for p in paginas:
        for e in p['enlaces']:
            if e['tipo'] in ('interno', 'externo'):
                st, fin = estados.get(e['destino'], (None, None))
                e['estado'] = st
                if fin and fin != e['destino']: e['redirige_a'] = fin
                ext_bloquea = e['tipo'] == 'externo' and st in (403, 429, 999)   # redes sociales bloquean bots: revisar a mano
                if (st is None or st >= 400 or st == 0) and not ext_bloquea:
                    agregar_roto(p, e, st)
            elif e['tipo'] == 'vacio':
                agregar_roto(p, e, 'enlace vacío')
    os.makedirs(a.salida, exist_ok=True)
    json.dump({'sitio': base, 'fecha': time.strftime('%Y-%m-%d %H:%M'), 'paginas': paginas,
               'enlaces_rotos': rotos}, open(os.path.join(a.salida, 'inventario.json'), 'w'), ensure_ascii=False, indent=1)

    # reporte para el recorrido en el navegador
    L = [f'# Recorrido como usuario · {host}', '', f'Fecha: {time.strftime("%Y-%m-%d")} · Páginas: {len(paginas)} · '
         f'Enlaces distintos: {len(todos)} · Rotos: {len(rotos)}', '',
         'Paso 1 (automático) listo. Paso 2: recorre cada página en el navegador siguiendo `reference/recorrido.md` y marca cada casilla.', '',
         '## Enlaces rotos o vacíos (paso 1)', '']
    L += [f'- [ ] `{r}` «{t}» → {d} ({s})' for r, t, d, s in rotos] or ['- Ninguno.']
    L += ['', '## Páginas', '']
    for p in paginas:
        prob = []
        if p['estado'] != 200: prob.append(f'estado {p["estado"]}')
        if p['h1'] != 1: prob.append(f'{p["h1"]} h1')
        if not p['descripcion'] or re.search(r'Esta es la|This is the', p['descripcion']): prob.append('sin descripción SEO')
        if p['imagenes_sin_alt']: prob.append(f'{p["imagenes_sin_alt"]} imágenes sin alt')
        L += [f'### {p["ruta"]} — {p["titulo"][:70]}', '',
              f'Estado {p["estado"]}{" → " + p["final"] if p["final"] else ""} · {p["segundos"]} s · {p["kb"]} KB HTML'
              + (f' · **{", ".join(prob)}**' if prob else ''), '',
              '| Revisión | 1440 | 375 |', '|---|---|---|',
              '| Se ve completa (captura) | [ ] | [ ] |', '| `owdRevisar()` sin problemas | [ ] | [ ] |',
              '| Consola sin errores | [ ] | [ ] |', '| Menú y logo llevan a donde dicen | [ ] | [ ] |', '']
        clics = [e for e in p['enlaces'] if e['zona'] == 'contenido' and e['tipo'] in ('interno', 'externo', 'contacto')]
        if clics:
            L += ['Clics del contenido:', '']
            L += [f'- [ ] «{e["texto"] or "(sin texto)"}» → {e["destino"].replace(base, "")}' + (' (pestaña nueva)' if e['nueva'] else '') for e in clics]
            L += ['']
        for f in p['formularios']:
            L += [f'- [ ] Formulario `{f["id"] or f["action"]}` ({f["modelo"] or "sin modelo"}): campos {", ".join(f["campos"])} · '
                  'probar validación vacía; enviar solo con permiso', '']
    L += ['## Flujos completos', '',
          '- [ ] Navegar todo el menú en orden y regresar con el botón Atrás (la transición no deja la pantalla tapada)',
          '- [ ] Menú móvil: abrir, navegar, cerrar',
          '- [ ] Acción principal del sitio de punta a punta (WhatsApp con mensaje, formulario, compra de prueba)',
          '- [ ] Tienda (si aplica): catálogo → producto → carrito → dirección → pago, sin pagar; cotización cancelada',
          '- [ ] 404: una URL inventada muestra la página de error del sitio con salida al inicio', '',
          '## Hallazgos y correcciones', '', '| # | Página | Ancho | Qué vio el usuario | Causa | Corrección | Verificado |',
          '|---|---|---|---|---|---|---|', '']
    open(os.path.join(a.salida, 'reporte.md'), 'w').write('\n'.join(L))
    print(f'\n{len(paginas)} páginas · {len(todos)} enlaces · {len(rotos)} rotos o vacíos → {a.salida}/inventario.json y {a.salida}/reporte.md')


if __name__ == '__main__':
    main()
