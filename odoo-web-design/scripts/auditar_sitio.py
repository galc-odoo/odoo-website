"""Audita el sitio publicado como lo ve un visitante (sin sesión). No necesita API key.

  python auditar_sitio.py https://cliente.odoo.com / /nosotros /servicios /contacto [--json]

Por página revisa: estado HTTP y redirección final, <title>, meta description, número de <h1>,
imágenes sin alt, peso total y la imagen más pesada, enlaces internos rotos (404), og:image,
si el footer propio (.owd-sitefooter) y el contenido (.owd-site) están presentes, y si quedó
algún dato de plantilla (yourcompany.example.com, 555-555, "Lorem").
"""
import json, re, sys, urllib.parse, urllib.request
from html.parser import HTMLParser

args = [a for a in sys.argv[1:] if not a.startswith('--')]
BASE, PATHS = args[0].rstrip('/'), args[1:] or ['/']
UA = {'User-Agent': 'Mozilla/5.0 (owd-auditoria)'}


def get(url, head=False):
    req = urllib.request.Request(url, headers=UA, method='HEAD' if head else 'GET')
    try:
        r = urllib.request.urlopen(req, timeout=60)
        return r.status, r.geturl(), (b'' if head else r.read()), r.headers
    except urllib.error.HTTPError as e:
        return e.code, url, b'', e.headers


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.title = ''; s.in_t = False; s.meta = {}; s.h1 = 0; s.imgs = []; s.links = set(); s.cls = set()
    def handle_starttag(s, t, at):
        a = dict(at)
        for c in (a.get('class') or '').split(): s.cls.add(c)
        if t == 'title': s.in_t = True
        if t == 'meta': s.meta[a.get('name') or a.get('property') or ''] = a.get('content', '')
        if t == 'h1': s.h1 += 1
        if t == 'img': s.imgs.append((a.get('src', ''), a.get('alt')))
        if t == 'a' and a.get('href', '').startswith('/') and not a['href'].startswith('//'): s.links.add(a['href'].split('#')[0] or '/')
    def handle_data(s, d):
        if s.in_t: s.title += d
    def handle_endtag(s, t):
        if t == 'title': s.in_t = False


rep, checked = [], {}
for path in PATHS:
    st, final, body, _ = get(BASE + path)
    html = body.decode('utf-8', 'ignore'); p = P(); p.feed(html)
    peso, mayor = 0, ('', 0)
    for src, _alt in p.imgs:
        if not src or src.startswith('data:'): continue
        u = urllib.parse.urljoin(BASE + '/', src)
        if u not in checked:
            s2, _, b2, _ = get(u); checked[u] = (s2, len(b2))
        peso += checked[u][1]
        if checked[u][1] > mayor[1]: mayor = (src.split('/')[-1][:50], checked[u][1])
    rotos = []
    for l in sorted(p.links):
        if l.startswith(('/web/', '/shop/cart', '/website/')): continue
        if l not in checked:
            checked[l] = get(BASE + l)[0:1] + (0,)
        if checked[l][0] == 404: rotos.append(l)
    plantilla = [m for m in ('yourcompany.example.com', '555-555', 'Lorem', 'info@yourcompany') if m in html]
    rep.append({'pagina': path, 'estado': st, 'final': final.replace(BASE, ''), 'titulo': p.title.strip(),
                'descripcion': p.meta.get('description', '')[:90], 'h1': p.h1,
                'sin_alt': sum(1 for _, al in p.imgs if not al), 'imagenes': len(p.imgs),
                'peso_img_kb': peso // 1024, 'mas_pesada': f'{mayor[0]} ({mayor[1]//1024} KB)',
                'og_image': bool(p.meta.get('og:image')), 'enlaces_rotos': rotos,
                'contenido_owd': 'owd-site' in p.cls, 'footer_owd': 'owd-sitefooter' in p.cls,
                'restos_de_plantilla': plantilla})

if '--json' in sys.argv:
    print(json.dumps(rep, ensure_ascii=False, indent=1)); sys.exit()
for r in rep:
    alertas = []
    if r['estado'] != 200: alertas.append(f"estado {r['estado']}")
    if r['h1'] != 1: alertas.append(f"{r['h1']} h1")
    if not r['descripcion'] or 'página principal' in r['descripcion']: alertas.append('sin descripción SEO')
    if r['sin_alt']: alertas.append(f"{r['sin_alt']} imágenes sin alt")
    if r['peso_img_kb'] > 1500: alertas.append(f"imágenes pesan {r['peso_img_kb']} KB")
    if r['enlaces_rotos']: alertas.append(f"enlaces rotos: {r['enlaces_rotos']}")
    if r['restos_de_plantilla']: alertas.append(f"restos de plantilla: {r['restos_de_plantilla']}")
    print(f"{r['pagina']:22} {r['estado']} → {r['final']:22} {r['peso_img_kb']:>5} KB  {'OK' if not alertas else '⚠ ' + '; '.join(alertas)}")
