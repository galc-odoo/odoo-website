"""Calcula el data-tf para acercar y CENTRAR un objeto de una foto al pasar el cursor.

  python centrar_zoom.py --img dips.webp --puntos "0.20,0.52" "0.50,0.52" "0.80,0.52" [--escala 2.5] [--caja 1]

--puntos: centro de cada objeto como fracción (x,y) de la foto (0 a 1). Mira la foto (Read) y estima
          el centro del objeto (no del borde superior); verifica después en el navegador.
--caja:   proporción ancho/alto del recuadro donde se muestra (1 = cuadrado, 0.8 = 4:5).
Salida: un data-tf por punto, listo para bloques.item_preview(). Si el objeto está muy cerca del
borde, el centro se ajusta para no mostrar zonas vacías y la escala sugerida se reporta.

Fórmula: con object-fit:cover y transform-origin al centro, `scale(s) translate(tx,ty)` mueve el
punto p al centro si tx=(0.5-p)*100% (en coordenadas del recuadro), limitado a [0.5/s, 1-0.5/s].
"""
import argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('--img', required=True)
ap.add_argument('--puntos', nargs='*', default=[])
ap.add_argument('--escala', type=float, default=2.4)
ap.add_argument('--caja', type=float, default=1.0)
a = ap.parse_args()
im = Image.open(a.img).convert('RGB'); W, H = im.size
ar_img, ar_box = W / H, a.caja
# fracción visible de la foto dentro del recuadro (object-fit: cover, centrado)
vis_w = min(1, ar_box / ar_img); vis_h = min(1, ar_img / ar_box)
off_x = (1 - vis_w) / 2; off_y = (1 - vis_h) / 2

pts = [tuple(map(float, p.split(','))) for p in a.puntos]
s = a.escala; lo, hi = 0.5 / s, 1 - 0.5 / s
for px, py in pts:
    bx = (px - off_x) / vis_w; by = (py - off_y) / vis_h   # punto en coordenadas del recuadro
    cx = min(max(bx, lo), hi); cy = min(max(by, lo), hi)
    nota = '' if (cx, cy) == (bx, by) else '  (ajustado al borde; sube la escala para centrarlo exacto)'
    print(f'({px:.2f},{py:.2f}) -> data-tf="scale({s:g}) translate({(0.5-cx)*100:.1f}%,{(0.5-cy)*100:.1f}%)"{nota}')
