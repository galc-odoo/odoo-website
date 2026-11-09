"""Arma el CSS y el JS del sitio a partir de la marca del cliente y los módulos elegidos.

  python armar.py --marca odoo/marca.json [--salida odoo]

Lee `marca.json` (copia uno de `assets/temas/*.json` y ajústalo al brief), y genera:
  odoo/sitio.css   variables de la marca (:root) + módulos de assets/css/
  odoo/sitio.js    window.OWD_CONFIG + módulos de assets/js/
  odoo/fuentes.txt valor para `push_code.py --fonts`
Revisa el contraste (WCAG) de los pares que usa el CSS y se detiene si alguno no pasa.

Módulos (en "modulos" de marca.json):
  nucleo         siempre · páginas, tipografía, botones, secciones, tarjetas, vista previa, pasos, galería,
                 formulario, transición entre páginas, fundador, aviso legal
  header-footer  siempre · footer propio, botón del header, botón flotante
  tienda         si hay e-commerce · catálogo, ficha, carrito y pago con los colores del tema
  contenido      horarios, preguntas frecuentes, paquetes, notas, reseñas, equipo
  efectos        intro, botones magnéticos, galería ampliada, menú móvil a pantalla completa
  interactivos   abierto ahora, franja que reacciona, carrete horizontal, test "¿qué … eres?", lista explora
  empaque        caja que se abre con el scroll y "diseña tu caja" (solo si el producto llega en caja)
"""
import argparse, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(AQUI, '..', 'assets')
ORDEN = ['nucleo', 'header-footer', 'tienda', 'contenido', 'efectos', 'interactivos', 'empaque']
JS = {'nucleo': 'nucleo', 'efectos': 'efectos', 'interactivos': 'interactivos', 'empaque': 'empaque'}


def rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(h):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mezcla(a, b, t):
    """t de b sobre a (0 = a, 1 = b)."""
    A, B = rgb(a), rgb(b)
    return '#%02X%02X%02X' % tuple(round(A[i] + (B[i] - A[i]) * t) for i in range(3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--marca', required=True)
    ap.add_argument('--salida', default='odoo')
    ap.add_argument('--forzar', action='store_true', help='genera aunque falle el contraste')
    a = ap.parse_args()
    m = json.load(open(a.marca))
    c = dict(m['colores'])
    # derivados si no vienen
    c.setdefault('surface', mezcla(c['bg'], c['text'], 0.05))
    c.setdefault('surface2', mezcla(c['bg'], c['text'], 0.09))
    c.setdefault('brand2', mezcla(c['brand'], '#FFFFFF', 0.15))
    c.setdefault('brand_dark', mezcla(c['brand'], '#000000', 0.25))
    c.setdefault('on_brand', '#FFFFFF' if contraste(c['brand'], '#FFFFFF') >= contraste(c['brand'], '#111111') else '#111111')
    c.setdefault('on_accent', '#FFFFFF' if contraste(c['accent'], '#FFFFFF') >= contraste(c['accent'], '#111111') else '#111111')
    # acento sobre el color de marca (footer, menú móvil): si no se lee, se usa el texto de marca
    c.setdefault('accent_on_brand', c['accent'] if contraste(c['accent'], c['brand']) >= 4.5 else mezcla(c['brand'], c['on_brand'], 0.8))
    c.setdefault('ok', '#3E9B5B' if lum(c['bg']) > 0.4 else '#7FBF7A')
    c.setdefault('error', '#B3261E' if lum(c['bg']) > 0.4 else '#E9A59D')

    pares = [('text', 'bg', 4.5), ('text', 'surface', 4.5), ('mute', 'bg', 4.5), ('mute', 'surface', 4.5),
             ('on_brand', 'brand', 4.5), ('accent_on_brand', 'brand', 4.5), ('on_accent', 'accent', 4.5), ('accent', 'bg', 3.0)]
    fallas = []
    print('Contraste (WCAG):')
    for f, b, minimo in pares:
        r = contraste(c[f], c[b])
        ok = r >= minimo
        print(f'  {"✓" if ok else "✗"} {f:9} sobre {b:8} {r:5.2f}:1  (mínimo {minimo})')
        if not ok: fallas.append(f'{f}/{b}')
    if fallas and not a.forzar:
        sys.exit(f'Ajusta los colores: {", ".join(fallas)} (o usa --forzar si es un acento solo decorativo).')

    f = m['fuentes']
    e = m.get('estilo', {})
    oscuro = m.get('modo', 'oscuro') == 'oscuro'
    root = [':root{',
            f'  color-scheme:{"dark" if oscuro else "light"};']
    for k in ['bg', 'surface', 'surface2', 'text', 'mute', 'accent', 'on_accent', 'brand', 'brand2', 'brand_dark', 'on_brand', 'accent_on_brand', 'ok', 'error']:
        root.append(f'  --owd-{k.replace("_", "-")}:{c[k]};')
    root += [f'  --owd-rule:color-mix(in srgb,var(--owd-text) {e.get("filete", 14)}%,transparent);',
             f'  --owd-display:{f["display"]};',
             f'  --owd-body:{f["body"]};',
             f'  --owd-display-style:{"italic" if e.get("titular_italica", False) else "normal"};',
             f'  --owd-display-case:{"uppercase" if e.get("titular_mayusculas", False) else "none"};',
             f'  --owd-display-weight:{e.get("titular_peso", 400)};',
             f'  --owd-radius:{e.get("radio", "2px")};',
             f'  --owd-pill:{e.get("pildora", "999px")};',
             f'  --owd-btn-radius:{e.get("boton_radio", "0px")};',
             f'  --owd-track:{e.get("espaciado", 1)};',
             f'  --owd-label-case:{"uppercase" if e.get("etiquetas_mayusculas", True) else "none"};',
             '  --owd-ease:cubic-bezier(.16,.84,.24,1);',
             '}']
    mods = [x for x in ORDEN if x in m.get('modulos', ['nucleo', 'header-footer'])]
    for req in ('nucleo', 'header-footer'):
        if req not in mods: mods.insert(0, req)
    cli = m.get('cliente', 'cliente')
    css = [f'/* odoo_web_design.{cli} · generado con armar.py desde marca.json · módulos: {", ".join(mods)} */', '\n'.join(root)]
    for x in mods:
        css.append(f'/* ===== módulo: {x} ===== */\n' + open(os.path.join(ASSETS, 'css', x + '.css')).read())
    if m.get('css_extra'):
        css.append('/* ===== propio del cliente ===== */\n' + open(os.path.join(os.path.dirname(a.marca), m['css_extra'])).read())
    js = [f'/* odoo_web_design.{cli} · generado con armar.py */',
          'window.OWD_CONFIG=' + json.dumps(m.get('js', {}), ensure_ascii=False) + ';']
    for x in mods:
        if x in JS: js.append(open(os.path.join(ASSETS, 'js', JS[x] + '.js')).read())

    os.makedirs(a.salida, exist_ok=True)
    open(os.path.join(a.salida, 'sitio.css'), 'w').write('\n'.join(css))
    open(os.path.join(a.salida, 'sitio.js'), 'w').write('\n'.join(js))
    open(os.path.join(a.salida, 'fuentes.txt'), 'w').write(f.get('google', ''))
    kb = lambda p: os.path.getsize(os.path.join(a.salida, p)) // 1024
    print(f'Módulos: {", ".join(mods)}')
    print(f'{a.salida}/sitio.css {kb("sitio.css")} KB · {a.salida}/sitio.js {kb("sitio.js")} KB')
    print(f'Siguiente: python push_code.py --cliente {cli} --css {a.salida}/sitio.css --js {a.salida}/sitio.js '
          f'--footer {a.salida}/footer.html --fonts "$(cat {a.salida}/fuentes.txt)" --dry-run')


if __name__ == '__main__':
    main()
