"""Sube el CSS, el JS y el footer al código personalizado del sitio (no son vistas).

  python push_code.py --cliente acme --css odoo/sitio.css --js odoo/sitio.js \
      --footer odoo/footer.html [--fonts "$(cat odoo/fuentes.txt)"] \
      [--website 1] [--dry-run]

- custom_code_head  = <link> de Google Fonts + <style id="odoo_web_design_<cliente>">CSS</style>
- custom_code_footer = footer HTML + <script id="odoo_web_design_<cliente>_js">JS</script>
Siempre reemplaza el bloque completo (nunca concatena) y respalda lo anterior en respaldo/.
"""
import argparse, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))

ap = argparse.ArgumentParser()
ap.add_argument('--cliente', required=True)
ap.add_argument('--css', required=True)
ap.add_argument('--js')
ap.add_argument('--footer')
ap.add_argument('--fonts', default='')
ap.add_argument('--website', type=int, default=1)
ap.add_argument('--dry-run', action='store_true')
a = ap.parse_args()

tag = f'odoo_web_design.{a.cliente}'
css = open(a.css).read()
head = f'<!-- {tag} -->\n'
if a.fonts:
    head += ('<link rel="preconnect" href="https://fonts.googleapis.com"/>\n'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>\n'
             f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={html.escape(a.fonts)}&amp;display=swap"/>\n')
head += f'<style id="odoo_web_design_{a.cliente}">\n{css}\n</style>'
foot = f'<!-- {tag} -->\n'
if a.footer:
    foot += open(a.footer).read() + '\n'
if a.js:
    foot += f'<script id="odoo_web_design_{a.cliente}_js">\n{open(a.js).read()}\n</script>'

if '</style' in css.lower():
    sys.exit('El CSS no debe contener </style>.')
if a.js and '</script' in open(a.js).read().lower():
    sys.exit('El JS no debe contener </script>.')

if a.dry_run:
    print(head[:400], '\n...\n', foot[:400]); sys.exit()

from odoo_rpc import x, backup
prev = x('website', 'read', [a.website], fields=['custom_code_head', 'custom_code_footer'])[0]
print('respaldo:', backup(f'custom_code_{a.cliente}', prev))
x('website', 'write', [a.website], {'custom_code_head': head, 'custom_code_footer': foot})
print(f'ok · head {len(head)//1024} KB · footer {len(foot)//1024} KB')
