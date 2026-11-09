# Dirección de diseño y maqueta

Cómo llegar a un sitio que se sienta *high end* y no a una plantilla. Léelo en la Fase 2.

## 1. Leer el material del cliente

- **PDF o presentación de concepto**: extrae por página la estructura (secciones y orden), los titulares, los textos y las notas de interacción ("JS: stepper", "hover-to-dip", "reveal al scroll"). Renderiza las páginas a imagen (PyMuPDF: `page.get_pixmap(dpi=90)`) para verlas.
- **Fotos**: revisa resolución real. Un collage de 1400 px da recortes de ~480 px que se ven borrosos a pantalla completa. Busca primero si el cliente ya subió versiones en alta a Odoo (`ir.attachment` públicos con `create_uid` del usuario) y úsalas.
- **Logo**: si llega como imagen sobre fondo de color, sácalo a PNG transparente por luminancia (alfa = (lum − fondo)/(255 − fondo)) en blanco y en el color de marca. Guarda versiones: monograma (para transiciones y favicon), logotipo (header) y logotipo + claim (footer).

## 2. Sistema visual (tokens)

Define en el brief y luego en `:root` del CSS base:

| Token | Uso | Ejemplo BADDIE |
|---|---|---|
| `--owd-ink` | Fondo principal | #100506 (negro con sesgo vino) |
| `--owd-ink2` | Superficies, campos | #1A0A0B |
| `--owd-brand` | Footer, botón flotante, cortinilla | #4A060A |
| `--owd-light` | Texto y logo | #F3E8DC (crema) |
| `--owd-mute` | Texto secundario | #A8958A (contraste ≥ 4.5:1) |
| `--owd-accent` | Un solo detalle: numerales, subrayados, foco | #C9A77C (dorado suave) |
| `--owd-display` | Titulares | Bodoni Moda itálica, mayúsculas |
| `--owd-body` | Texto | Jost 300 |

Reglas de oficio:
- **Neutros con intención**: el negro y el gris llevan un sesgo hacia el color de marca; nunca gris puro.
- **Un solo acento** y usado con moderación. Nunca rojo saturado en links (al cliente no le gustó); los enlaces van en el tono claro con subrayado del acento al pasar el cursor.
- **Tipografía como protagonista**: titular serif itálico enorme (`clamp(58px, 9.4vw, 158px)`, `line-height:.86`, `letter-spacing:-.015em`) contra texto pequeño espaciado. Etiquetas en mayúsculas de 10–12 px con `letter-spacing:.3–.42em`.
- **Aire**: secciones con `padding-block: clamp(64px, 9vw, 140px)`, contenedor de 1440 px con gutter `clamp(16px, 5vw, 88px)`.
- **Filetes finos** (`1px` a 14 % de opacidad) en lugar de tarjetas con sombra. Fotos con **marco interior** (borde de 1 px a 10 px del canto).
- **Números romanos o numerales** solo cuando hay secuencia real (pilares, pasos).

## 3. Componentes probados (ya están en `assets/base.css`)

- **Encabezado de página** (`.owd-head`): eyebrow con filete de acento, titular gigante, línea vertical y texto de apoyo a la derecha.
- **Hero de inicio** (`.owd-hero`): titular de 3 líneas + foto vertical 4:5 con contador ("Detroit style — CDMX") y franja en movimiento (`.owd-marquee`).
- **Pilares** (`.owd-pillars`): 4 columnas con filetes; en móvil 2×2; títulos que caben (bajar tamaño, no cortar palabras).
- **Bloque dividido** (`.owd-split`): foto 5:6 + texto y botón.
- **Tarjetas de producto** (`.owd-card`): foto 3:4 con etiqueta (`.owd-tag`), acercamiento al pasar el cursor, inclinación sutil, nombre en display y flecha en círculo. Sin etiquetas extra sobre la foto (al cliente no le gustaron).
- **Lista con vista previa** (`.owd-dip-group`): lista grande a la izquierda y foto cuadrada que se acerca y centra el objeto elegido (`data-tf`, ver `scripts/centrar_zoom.py`). Grupos separados por tipo (por ejemplo, salados y dulces).
- **Pasos** (`.owd-how`): 4 columnas con ícono de línea, numeral en acento y texto; un solo botón de acción debajo.
- **Tipos de servicio** (`.owd-ev-types`), **formulario** a dos columnas (`.owd-ev-form`), **galería** de 3 fotos del mismo tamaño (`.owd-gallery`).
- **Siguiente página** (`.owd-next`): enlace enorme al final de cada página. Deja ≥ 22 px entre eyebrow y titular para que los acentos (É) no choquen.
- **Footer de marca**, **botón flotante** de WhatsApp en móvil, **cortinilla** con el monograma que se forma entre páginas.

## 4. Maqueta (artifact HTML)

1. Una página HTML con **cada página del sitio por separado** (enrutado por `#hash` y transición), no una sola página larga. Nombres de páginas en el idioma del cliente.
2. Imágenes embebidas como data URI (redimensionar a ≤ 1400 px), fuentes de Google Fonts, sin librerías.
3. Itera rápido: el cliente aprueba con capturas o comentarios puntuales ("quita las etiquetas", "separa los dips", "más high end").
4. Si el alcance es informativo, **nada de e-commerce** en la maqueta: sin cantidades, carrito ni resumen; solo pasos y un botón a WhatsApp.
5. "Más high end" suele significar: más aire, filetes en vez de cajas, un acento dorado discreto, marcos interiores en fotos, botones que se rellenan desde abajo, grano sutil, titulares más grandes y menos elementos por pantalla.
6. Formularios: el cliente prefiere los campos de texto nativos de Odoo (un solo paso) sobre selectores o formularios por pasos.

## 5. Fotos

- Formato por uso: hero 4:5, tarjetas 3:4, bloques 5:6, panorámicas 21:9 (4:3 en móvil), galería 4:5 todas iguales, retrato del fundador 4:5.
- Centrado: `object-fit: cover` + `object-position` hacia el sujeto. Para retratos horizontales en marco vertical, la persona al centro.
- Peso: WebP calidad 85–88; ideal < 300 KB por foto. Las fotos subidas desde el editor a veces pesan 700 KB–1 MB: usa `scripts/optimizar_imagenes.py`.
- Texto alternativo descriptivo en todas.
