# Dirección de diseño

Cómo llegar a un sitio que se sienta hecho a la medida y no a una plantilla, para cualquier giro. Pasos 3 a 6.

## 1. Leer el material del cliente

- **Maqueta en PDF**: renderiza cada página a imagen (PyMuPDF `page.get_pixmap(dpi=90)`) y extrae por página: secciones y orden, titulares, textos, notas de interacción ("al pasar el cursor…", "se abre al hacer scroll"). Lo que pida con JS/CSS se mapea al catálogo (`componentes.md`) o se diseña a la medida.
- **Imágenes** (solo referencia): revisa la resolución real. Busca si el cliente ya subió versiones en alta a Odoo (`ir.attachment` públicos del usuario).
- **Logo**: si llega sobre fondo de color, sácalo a PNG transparente por luminancia, en claro y en el color de marca. Versiones: monograma (transición, favicon), logotipo (header), logotipo con claim (footer).
- **Referencias por liga**: toma estructura, ritmo y tipo de interacción; nunca logos, textos ni fotos ajenas.

## 2. Elegir la dirección (tema)

Parte del tema más cercano y ajústalo a la marca. Nunca copies los colores de otro cliente.

| Tema | Para | Rasgos |
|---|---|---|
| `editorial-oscuro` | Lujo, gastronomía de autor, moda, hoteles | Fondo casi negro con sesgo de marca, serif itálica en mayúsculas, acento dorado, mucho aire. |
| `minimal-claro` | Estudios, arquitectura, galerías, marcas de autor | Blanco cálido, serif fina sin mayúsculas, filetes, cero adornos. |
| `corporativo` | B2B, industria, despachos, salud | Blanco, sans firme, azul de confianza, radios suaves, etiquetas sin mayúsculas. |
| `calido-artesanal` | Cafés, panaderías, natural, bienestar | Crema, serif con carácter en itálica, terracota, píldoras. |
| `tecnologico-oscuro` | Software, startups, fintech | Fondo azul noche, grotesca, acento eléctrico, radios medianos. |

`marca.json`:
```json
{
  "cliente": "acme", "marca": "ACME", "modo": "claro",
  "colores": {"bg": "#FFFFFF", "text": "#0E1B2C", "mute": "#4B5767", "accent": "#0B63C1", "brand": "#0E1B2C", "on_brand": "#FFFFFF"},
  "fuentes": {"display": "\"Manrope\",system-ui,sans-serif", "body": "\"Inter\",system-ui,sans-serif", "google": "Manrope:wght@500;700&family=Inter:wght@300;400;500"},
  "estilo": {"titular_italica": false, "titular_mayusculas": false, "titular_peso": 700, "radio": "8px", "pildora": "8px",
             "boton_radio": "8px", "espaciado": 0.3, "etiquetas_mayusculas": false, "filete": 12},
  "modulos": ["nucleo", "header-footer", "contenido", "efectos"],
  "js": {"paginas": ["/", "/nosotros", "/servicios", "/contacto"], "whatsapp": "5215500000000", "botonFlotante": "Escríbenos",
         "botonFlotanteUrl": "/contacto", "cursor": false, "horario": null, "formulario": "#owd_form"}
}
```
Opcionales en `colores`: `surface`, `surface2`, `brand2`, `brand_dark`, `on_accent`, `accent_on_brand`, `ok`, `error` (si faltan, `armar.py` los calcula). `css_extra` apunta a un CSS propio del cliente que se agrega al final.

`armar.py` revisa el contraste: texto, texto secundario, texto sobre la marca y sobre el acento ≥ 4.5:1; acento sobre fondo ≥ 3:1. Si falla, ajusta el color; no lo fuerces.

## 3. Oficio (lo que hace que se vea *high end*)

- **Neutros con intención**: el fondo y los grises llevan un sesgo hacia el color de marca; nunca gris puro.
- **Un solo acento**, con moderación: numerales, subrayados, foco. Enlaces en el color del texto con subrayado de acento al pasar el cursor (nunca rojo saturado).
- **Tipografía como protagonista**: titular grande (`clamp`) contra texto pequeño con buen interlineado; etiquetas cortas con espaciado.
- **Aire**: secciones con `padding-block: clamp(64px, 9vw, 140px)`, contenedor de 1440 px y margen lateral `clamp(16px, 5vw, 88px)`.
- **Filetes finos** en lugar de tarjetas con sombra; fotos con marco interior.
- **Menos elementos por pantalla**; una acción principal visible.
- Numerales o romanos solo cuando hay secuencia real.
- Fotos por uso: hero 4:5, tarjetas 3:4, bloque dividido 5:6, panorámica 21:9 (4:3 en móvil), galería 4:5 iguales, retratos 4:5. WebP 85, ideal < 300 KB; `optimizar_imagenes.py` para las pesadas.

## 4. Vista previa (en lugar de una maqueta aparte)

- Las páginas se arman una vez en `odoo/paginas.py` con `bloques.py` y se ven con `vista_previa.py`: lo que el diseñador aprueba es exactamente lo que se sube a Odoo.
- Cada página por separado, con los textos reales del cliente. Revisa en 1440 y 375 px y corre `owdRevisar()` antes de enseñarla.
- Si el alcance es informativo, nada de comercio electrónico (cantidades, carrito) en las páginas: un botón a la acción principal.
- Formularios: campos de texto nativos de Odoo en un solo paso.
- "Más high end" suele significar: más aire, filetes en vez de cajas, titulares más grandes, menos elementos, un acento discreto, fotos con marco y botones que responden.
