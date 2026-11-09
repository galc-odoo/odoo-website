"""Crea o actualiza una página PROPIA del sitio (la única vista que el skill escribe).

  python escribir_pagina.py --key website.nosotros --nombre "Nosotros" --url /nosotros \
      --arch-file odoo/paginas/nosotros.xml [--titulo "Nosotros · Marca"] [--descripcion "..."] \
      [--og /web/image/...] [--publicar] [--website 1]

Protecciones:
- Se niega a escribir vistas estándar (con XML ID de módulo), heredadas (inherit_id) o sin website_id.
- Valida que el XML esté bien formado antes de escribir.
- Respalda el arch actual en respaldo/ antes de cambiarlo.
- Escribe el mismo arch en TODOS los idiomas activos del sitio (evita que una traducción vieja regrese).
- Avisa si la página se modificó desde el editor después de tu última lectura (--desde YYYY-MM-DD HH:MM:SS).
- Nunca cambia la URL con write(): usa update_field_translations (write falla por API al crear la redirección).
"""
import argparse, os, sys
from xml.dom import minidom
sys.path.insert(0, os.path.dirname(__file__))
from odoo_rpc import x, langs, backup

ap = argparse.ArgumentParser()
ap.add_argument('--key', required=True)
ap.add_argument('--nombre', required=True)
ap.add_argument('--url', required=True)
ap.add_argument('--arch-file', required=True)
ap.add_argument('--titulo'); ap.add_argument('--descripcion'); ap.add_argument('--og')
ap.add_argument('--publicar', action='store_true')
ap.add_argument('--desde', help='write_date que leíste; si la vista cambió después, se detiene')
ap.add_argument('--website', type=int, default=1)
a = ap.parse_args()

arch = open(a.arch_file).read()
minidom.parseString(arch.encode())  # lanza error si el XML no es válido
W = a.website
L = langs(W)

ids = x('ir.ui.view', 'search', [['key', '=', a.key], ['website_id', '=', W]])
if ids:
    vid = ids[0]
    v = x('ir.ui.view', 'read', [vid], fields=['inherit_id', 'website_id', 'write_date', 'page_ids'])[0]
    xmlid = x('ir.model.data', 'search_count', [['model', '=', 'ir.ui.view'], ['res_id', '=', vid]])
    if v['inherit_id'] or not v['website_id'] or xmlid:
        sys.exit(f'La vista {vid} es estándar o heredada: no se edita por API (regla de migración).')
    if a.desde and v['write_date'] > a.desde:
        sys.exit(f'La vista cambió en el editor ({v["write_date"]}). Vuelve a leerla y aplica tu cambio sobre esa versión.')
    prev = {l: x('ir.ui.view', 'read', [vid], fields=['arch_db'], context={'lang': l})[0]['arch_db'] for l in L}
    print('respaldo:', backup(f'vista_{vid}', prev))
else:
    if x('ir.ui.view', 'search_count', [['key', '=', a.key]]):
        sys.exit(f'Ya existe una vista estándar con la clave {a.key}. Usa otra clave (por ejemplo website.{a.url.strip("/")}-owd).')
    vid = x('ir.ui.view', 'create', {'name': a.nombre, 'type': 'qweb', 'key': a.key, 'website_id': W, 'arch_db': arch})
    print('vista creada', vid)

for l in L:
    x('ir.ui.view', 'write', [vid], {'arch_db': arch}, context={'lang': l})

pages = x('website.page', 'search', [['view_id', '=', vid], ['website_id', '=', W]])
if pages:
    pid = pages[0]
else:
    pid = x('website.page', 'create', {'name': a.nombre, 'url': a.url, 'view_id': vid, 'website_id': W,
                                       'is_published': bool(a.publicar), 'website_indexed': True})
    print('página creada', pid)
x('website.page', 'update_field_translations', [pid], 'url', {l: a.url for l in L})
vals = {'name': a.nombre}
if a.titulo: vals['website_meta_title'] = a.titulo
if a.descripcion: vals['website_meta_description'] = a.descripcion
if a.og: vals['website_meta_og_img'] = a.og
if a.publicar: vals['is_published'] = True
for l in L:
    x('website.page', 'write', [pid], vals, context={'lang': l})  # sin website_id en contexto: no crea copias
print(f'ok · vista {vid} · página {pid} · idiomas {", ".join(L)}')
