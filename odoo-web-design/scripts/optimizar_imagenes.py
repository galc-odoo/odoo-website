"""Comprime las imágenes pesadas de páginas propias sin cambiar su tamaño visible.

  python optimizar_imagenes.py --vistas 4031 4032 [--umbral-kb 350] [--calidad 86] [--max-ancho 2000] [--aplicar]

Para cada <img> de esas vistas cuyo adjunto pese más del umbral:
  1. Descarga el original, lo recodifica en WebP (misma resolución, o hasta --max-ancho) y lo sube como adjunto público opt_<nombre>.webp.
  2. Cambia src y src.translate al nuevo y quita srcset/srcset.translate (que apuntaban a variantes pesadas).
  3. Escribe la vista en todos los idiomas, con respaldo previo.
Sin --aplicar solo muestra el ahorro estimado. Requiere Pillow (pip install pillow).
"""
import argparse, base64, io, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from odoo_rpc import x, langs, backup
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('--vistas', nargs='+', type=int, required=True)
ap.add_argument('--umbral-kb', type=int, default=350)
ap.add_argument('--calidad', type=int, default=86)
ap.add_argument('--max-ancho', type=int, default=2000)
ap.add_argument('--aplicar', action='store_true')
a = ap.parse_args()
L = langs()
mapa = {}
for vid in a.vistas:
    arch = x('ir.ui.view', 'read', [vid], fields=['arch_db'], context={'lang': 'en_US'})[0]['arch_db']
    for src in re.findall(r'<img [^>]*?\ssrc="(/web/image/(\d+)[^"]*)"', arch):
        url, att = src[0], int(src[1])
        if url in mapa: continue
        info = x('ir.attachment', 'read', [att], fields=['file_size', 'name'])[0]
        if info['file_size'] < a.umbral_kb * 1024: continue
        raw = base64.b64decode(x('ir.attachment', 'read', [att], fields=['raw'])[0]['raw']['content'])
        im = Image.open(io.BytesIO(raw)).convert('RGB')
        if im.width > a.max_ancho:
            im = im.resize((a.max_ancho, round(im.height * a.max_ancho / im.width)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'WEBP', quality=a.calidad, method=6)
        print(f'{info["name"][:44]:44} {im.size} {info["file_size"]//1024} KB -> {len(b.getvalue())//1024} KB')
        if not a.aplicar: continue
        name = 'opt_' + re.sub(r'\.\w+$', '', urllib.parse.unquote(url.split('/')[-1].split('?')[0])) + '.webp'
        ex = x('ir.attachment', 'search', [['name', '=', name]])
        nid = ex[0] if ex else x('ir.attachment', 'create', {'name': name, 'raw': base64.b64encode(b.getvalue()).decode(),
                                                             'mimetype': 'image/webp', 'public': True, 'res_model': 'ir.ui.view', 'res_id': 0})
        mapa[url] = x('ir.attachment', 'read', [nid], fields=['image_src'])[0]['image_src']

if not a.aplicar:
    sys.exit('\nVista previa. Agrega --aplicar para subir y cambiar las imágenes.')

def fix(m):
    tag = m.group(0); s = re.search(r'\ssrc="([^"]+)"', tag).group(1)
    if s not in mapa: return tag
    n = mapa[s]
    tag = tag.replace(f' src="{s}"', f' src="{n}"', 1)
    tag = re.sub(r' src\.translate="[^"]*"', f' src.translate="{n}"', tag)
    return re.sub(r' srcset(\.translate)?="[^"]*"', '', tag)

for vid in a.vistas:
    prev = {l: x('ir.ui.view', 'read', [vid], fields=['arch_db'], context={'lang': l})[0]['arch_db'] for l in L}
    new = {l: re.sub(r'<img [^>]+>', fix, prev[l]) for l in L}
    if any(new[l] != prev[l] for l in L):
        backup(f'vista_{vid}_antes_opt', prev)
        for l in L: x('ir.ui.view', 'write', [vid], {'arch_db': new[l]}, context={'lang': l})
        print('vista actualizada', vid)
