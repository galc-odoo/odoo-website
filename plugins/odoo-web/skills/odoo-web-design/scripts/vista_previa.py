"""Vista previa local del sitio (sin Odoo): arma un HTML con la estructura de Odoo (header, #wrap, footer),
el CSS y el JS generados por armar.py y las páginas hechas con bloques.py.

  python vista_previa.py --marca odoo/marca.json [--paginas odoo/paginas.py] [--salida maqueta/vista_previa.html]

- Sin --paginas muestra el CATÁLOGO completo de bloques con fotos de muestra: sirve para elegir dirección y
  componentes con el consultor, y para revisar que el tema (claro u oscuro) se vea bien en todos.
- Con --paginas usa el diccionario PAGINAS = {'/': [secciones…], '/nosotros': [...]} de ese archivo.
Ábrelo en el navegador (file://…) y revísalo en 1440 y 375 px antes de subir nada a Odoo.
"""
import argparse, importlib.util, json, os, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import bloques as b  # noqa: E402


def foto(etiqueta, w=1200, h=1500, tono='#8a7a6a'):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{tono}"/>'
           f'<stop offset="1" stop-color="#2a2420"/></linearGradient></defs><rect width="100%" height="100%" fill="url(#g)"/>'
           f'<text x="50%" y="50%" fill="#fff" fill-opacity=".75" font-family="sans-serif" font-size="{w // 22}" '
           f'text-anchor="middle">{etiqueta}</text></svg>')
    import urllib.parse
    return 'data:image/svg+xml,' + urllib.parse.quote(svg)


def catalogo():
    form = b.formulario('owd_form', 'crm.lead', 'Solicitud desde la web',
                        [b.campo('f1', 'Nombre', 'contact_name', custom=False), b.campo('f2', 'Teléfono', 'phone', custom=False, tipo='tel'),
                         b.campo('f3', 'Correo', 'email_from', custom=False, tipo='email'),
                         b.campo('f4', 'Cuéntanos', 'description', custom=False, textarea=True, col='col-12')],
                        'Enviar', 'Gracias.', 'Te contactamos pronto.')
    faq_html, _ = b.preguntas('Preguntas frecuentes', 'Lo que nos preguntan.',
                              [('¿Cuánto tarda?', 'Entre 3 y 5 días hábiles.'), ('¿Dónde están?', 'En la ciudad, con cita.')])
    previews = ('<div class="container owd-section">' + b.grupo_preview(
        'lista', 'i.', 'Lista con vista previa', 'Pasa el cursor por cada elemento.',
        [b.item_preview('Uno', 'Detalle', 'Descripción del primero.', '#b5321c', 'scale(2.2) translate(25%,0%)'),
         b.item_preview('Dos', 'Detalle', 'Descripción del segundo.', '#5e7a3a', 'scale(2.2) translate(0%,0%)'),
         b.item_preview('Tres', 'Detalle', 'Descripción del tercero.', '#8b4a2b', 'scale(2.2) translate(-25%,0%)')],
        foto('Foto con 3 objetos', 1200, 1200), 'Foto', 'Elige uno para acercar.') + '</div>')
    return {'/': [
        b.hero('Eyebrow de la marca', ['Titular', 'de tres', 'líneas.'], 'Texto de apoyo corto que dice qué hace la empresa y para quién.',
               [('Acción principal', '#'), ('Secundaria', '#')], foto('Hero 4:5'), 'Foto principal', ('Colección 01', 'Ciudad'),
               franja=['Frase uno', 'Frase dos', 'Frase tres']),
        b.pilares([('Idea uno', 'Una línea que la explica.'), ('Idea dos', 'Una línea que la explica.'),
                   ('Idea tres', 'Una línea que la explica.'), ('Idea cuatro', 'Una línea que la explica.')]),
        b.dividido(foto('Bloque 5:6', 1000, 1200), 'Foto', 'Sección', 'Bloque dividido.', 'Foto a un lado y texto con botón al otro.', [('Ver más', '#')]),
        b.encabezado('Encabezado de página', ['Página', 'interior.'], 'Así abre cada página que no es el inicio.'),
        b.tarjetas([b.tarjeta('#', 'Etiqueta', foto(f'Tarjeta {i}', 900, 1200), 'Foto', b.ROM[i], f'Producto {i + 1}', 'Descripción breve.') for i in range(3)]),
        previews,
        b.pasos([('lista', 'Elige', 'Qué necesitas.'), ('mensaje', 'Escríbenos', 'Por el canal principal.'),
                 ('calendario', 'Agenda', 'Fecha y hora.'), ('check', 'Listo', 'Lo recibes.')], 'Nota de cierre.', [('Acción principal', '#')]),
        b.tipos([('personas', 'Tipo uno', 'Para quién.'), ('estrella', 'Tipo dos', 'Para quién.'),
                 ('calendario', 'Tipo tres', 'Para quién.'), ('rayo', 'Tipo cuatro', 'Para quién.')], foto('Panorámica 21:9', 2100, 900), 'Foto'),
        b.horarios('Horarios', 'Cuándo y dónde.', [('Horario', 'Lun a Vie', '9:00 a 18:00.'), ('Entregas', 'A tu medida', 'Se acuerdan.'), ('Zona', 'Ciudad', 'Zonas seleccionadas.')]),
        faq_html,
        b.paquetes('Paquetes', 'Elige tu formato.', [('Básico', 'Para empezar.', ['Punto uno', 'Punto dos']), ('Completo', 'Todo incluido.', ['Punto uno', 'Punto dos'])], 'Pedido mínimo <strong>10</strong> piezas'),
        b.notas([('Aviso', 'Texto de un aviso importante.')]),
        b.fundador(foto('Retrato 4:5'), 'Fundador', ['Primer párrafo de la historia en primera persona.', 'Segundo párrafo.'], 'Nombre Apellido', 'Fundador'),
        b.equipo([('Persona Uno', 'Cofundadora', 'Bio corta.', foto('Retrato'), 'Foto'), ('Persona Dos', 'Cofundador', 'Bio corta.', foto('Retrato'), 'Foto')]),
        b.frase('Una frase de marca que se queda.', 'Quién lo dice'),
        b.bloque_formulario('Contacto', 'Hablemos.', 'Formulario nativo de Odoo (crm.lead).', form),
        b.galeria([(foto(f'Galería {i}'), 'Foto') for i in range(3)], b.siguiente('#', 'Siguiente', 'Otra página')),
    ]}


HEADER = ('<header id="top"><nav class="navbar navbar-expand-lg" style="background:var(--owd-brand);color:var(--owd-on-brand)">'
          '<div class="container"><a class="navbar-brand logo" href="#" style="color:inherit;font-family:var(--owd-display)">{marca}</a>'
          '<ul id="top_menu" class="nav navbar-nav flex-row gap-3">{menu}</ul></div></nav></header>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--marca', required=True)
    ap.add_argument('--paginas')
    ap.add_argument('--salida', default='maqueta/vista_previa.html')
    a = ap.parse_args()
    m = json.load(open(a.marca))
    tmp = tempfile.mkdtemp()
    r = subprocess.run([sys.executable, os.path.join(AQUI, 'armar.py'), '--marca', a.marca, '--salida', tmp, '--forzar'], capture_output=True, text=True)
    print(r.stdout.split('Siguiente')[0].strip())
    css, js, fonts = (open(os.path.join(tmp, f)).read() for f in ('sitio.css', 'sitio.js', 'fuentes.txt'))
    if a.paginas:
        spec = importlib.util.spec_from_file_location('paginas', a.paginas); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        paginas = mod.PAGINAS
    else:
        paginas = catalogo()
    foot_path = os.path.join(os.path.dirname(a.marca), 'footer.html')
    footer = open(foot_path).read() if os.path.exists(foot_path) else open(os.path.join(AQUI, '..', 'assets', 'footer.html')).read()
    marca = m.get('marca', m.get('cliente', 'Marca'))
    import re
    muestra = {'MARCA': marca, 'CLAIM': 'Claim de la marca', 'FRASE_DE_MARCA': 'Una frase de marca.', 'WHATSAPP': '5210000000000',
               'WHATSAPP_VISIBLE': '+52 000 000 0000', 'CORREO': 'hola@ejemplo.mx', 'CIUDAD': 'Ciudad', 'AÑO': '2026',
               'LOGO_URL': foto(marca, 560, 120), 'LOGO_W': '560', 'LOGO_H': '120'}
    footer = re.sub(r'\{\{([^}]+)\}\}', lambda x: muestra.get(x.group(1), x.group(0)), footer)
    menu = ''.join(f'<li class="nav-item"><a class="nav-link" style="color:inherit" href="#{u}">{u}</a></li>' for u in paginas)
    secciones = ''.join(f'<div data-owd-ruta="{u}">{"".join(s)}</div>' for u, s in paginas.items())
    html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vista previa · {marca}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fonts}&display=swap">
<style>{css}</style></head>
<body><div id="wrapwrap">{HEADER.format(marca=marca, menu=menu)}<main><div id="wrap" class="oe_structure owd-site">{secciones}</div></main>
<footer id="bottom">footer de la plantilla (oculto)</footer></div>
{footer}
<script>{js}</script></body></html>'''
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, 'w').write(html)
    print('Vista previa:', 'file://' + os.path.abspath(a.salida))


if __name__ == '__main__':
    main()
