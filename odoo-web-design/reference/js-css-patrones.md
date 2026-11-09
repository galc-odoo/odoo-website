# CSS y JS: patrones seguros

Todo vive en el código personalizado del sitio (`custom_code_head` / `custom_code_footer`). Fuente local:
`odoo/sitio.css`, `odoo/sitio.js`, `odoo/footer.html`; se suben con `scripts/push_code.py`.

## Arranque de un proyecto
1. Copia `assets/base.css`, `assets/base.js` y `assets/footer.html` a `odoo/` del cliente.
2. Cambia los tokens de `:root` (paleta y fuentes) y los textos `{{…}}` del footer.
3. En `base.js` configura `PAGES` (páginas con transición), `WHATSAPP` (solo dígitos con lada, vacío para no mostrar el botón flotante) y `FLOAT_LABEL`.
4. En cada página propia pon `data-owd-mark="<url del monograma>"` en `#wrap` (lo hace `bloques.pagina()`).
5. Sube: `python scripts/push_code.py --cliente <slug> --css odoo/sitio.css --js odoo/sitio.js --footer odoo/footer.html --fonts "<familias de Google Fonts>"`.

## Alcance (para no afectar lo que no se pidió)
| Zona | Selector |
|---|---|
| Páginas propias | `.owd-site …` y `body:has(.owd-site) …` |
| Tienda (catálogo / producto / carrito y pago) | `body.o_website_sale_products`, `body.o_website_sale_product`, `body.o_website_sale_checkout` (todas: `body[class*="o_website_sale"]`) |
| Header en todo el sitio | `header …` (con cuidado: también es el de la Tienda) |
| Footer propio | `.owd-sitefooter …`; el de la plantilla: `footer#bottom{display:none!important}` |

## Animaciones sin JS (no ensucian el contenido)
```css
@supports (animation-timeline: view()){
  .owd-site .owd-rv{animation:owd-reveal linear both;animation-timeline:view();animation-range:entry 0% entry 70%}
  .owd-site .owd-par img{height:118%;animation:owd-par linear both;animation-timeline:view()}
}
@keyframes owd-reveal{from{opacity:.3;transform:translateY(34px)}to{opacity:1;transform:none}}
body.editor_enable .owd-site *{animation:none!important}
@media (prefers-reduced-motion:reduce){.owd-site *{animation:none!important;transition:none!important}}
```
El estado en reposo siempre es visible (nunca `opacity:0` esperando a un observer). Titulares que entran: `.owd-ln>span{animation:owd-rise 1.25s var(--owd-ease) both}` con `overflow:hidden` en `.owd-ln`.

## JS (`assets/base.js`)
- `editing()` = `body.editor_enable` o existe `.o_editable`. Todo se detiene en modo edición.
- **Cortinilla entre páginas**: intercepta clics a rutas de `PAGES`, muestra velo translúcido (`backdrop-filter: blur`) y el monograma que se llena de abajo hacia arriba con una línea de acento (1 s), guarda `sessionStorage['owd-tr']` y navega; la página nueva arranca con el monograma formado y se desvanece. Respeta `prefers-reduced-motion`, teclas modificadoras y `target=_blank`.
- **Vista previa en listas** (`.owd-dip-group`): al pasar el cursor/enfocar/tocar un `.owd-dip`, aplica a la foto `transform: data-tf` (centrado exacto) o, en datos viejos, `data-pos` + `data-org`. Restaura todo si se abre el editor.
- **Inclinación de tarjetas**: `perspective(1000px) rotateY/rotateX` ±4° según el cursor; se limpia al salir.
- **Botón flotante**: `<a class="owd-wa-float">` agregado a `body` (fuera del contenido editable), visible < 992 px; se quita si se abre el editor.

## Centrado del acercamiento
`python scripts/centrar_zoom.py --img foto.webp --puntos "0.20,0.52" "0.50,0.52" --escala 2.5 --caja 1`
Escala 2–2.5 para objetos de ~25 % del ancho; si el objeto queda pegado al borde, el script ajusta el centro y avisa. Baja la escala si la base del objeto queda tapada por el pie de foto.

## Detalles que el cliente notó
- Acentos que chocan con el texto de arriba: deja `margin-bottom ≥ 22px` en el eyebrow y `line-height:1` + `padding-top:.08em` en titulares en mayúsculas.
- Títulos largos en columnas (UNAPOLOGETIC): baja `font-size` con `clamp` y revisa en 1440, 1024 y 375 px que ninguno pase la línea divisoria.
- Titulares en móvil: `font-size:min(12vw,58px)` para que palabras largas (EXPERIENCES.) quepan.
- El botón flotante no debe tapar el pie: `padding-bottom` en la barra final en móvil.
- Galerías: todas las fotos del mismo tamaño.
- Equipo: los cofundadores van debajo del fundador, con foto en el mismo formato 4:5 y marco (`bloques.equipo()`), centrada en la cara.
- Nada de elementos que sigan al cursor con texto ("Ver") ni fotos flotantes en listas si el cliente no los pide: se sienten como ruido.

## Componentes extra (ya en `assets/base.css` y `assets/base.js`)
- **Hero animado**: fotos adicionales dentro de `.owd-shot` con clase `img.owd-slide` (hasta 3). Se funden cada 6 s con acercamiento lento, solo CSS; en edición se ocultan y queda la primera. La foto principal lleva `loading="eager" fetchpriority="high"`.
- **Intro de primera visita**: el monograma se forma al abrir el sitio (una vez por sesión, `sessionStorage['owd-intro']`).
- **Cursor de marca**: anillo que crece sobre enlaces y muestra "Ver" sobre tarjetas y fotos de galería; solo con `hover:hover` y `pointer:fine`.
- **Botones magnéticos**: `.btn.owd-btn` y `.owd-circle` siguen un poco al cursor; el estilo se borra al salir.
- **Galería ampliada**: clic o Enter en una foto de `.owd-gallery` abre un visor con flechas, Esc y deslizar en móvil. Los atributos de accesibilidad que agrega a los marcos se quitan si se abre el editor.
- **Menú móvil a pantalla completa**: estiliza `#top_menu_collapse_mobile` (fondo de marca, opciones en display gigante que entran escalonadas, sin buscador).
- **Horarios** (`.owd-hours`), **preguntas frecuentes** con `<details>` (`.owd-faq`, sin JS), **paquetes** (`.owd-packs`/`.owd-pack` + `.owd-min`), **notas** (`.owd-note`) y **reseñas** (`.owd-reviews`).

## Interactivos de alto impacto (ya en `assets/`)
Todos guardan su estado en clases o variables de `<html>` (no en el contenido editable) y restauran todo al abrir el editor.
- **Caja que se abre con el scroll** (`.owd-unbox` > `.owd-unbox-stage` > copia + `.owd-unbox-box.owd-unbox-h` y `.owd-unbox-v`): sección fija de ~280vh. Se arma con **una sola foto del empaque abierto** (cenital, recortada sin fondo): se corta en dos capas, la **base** (bandeja con producto) y la **tapa**, justo en el borde de la tapa (mide la fila exacta: la franja oscura debajo es sombra). Con `--owd-u` (0→1) la tapa se desliza (`translate` de ~85 % de su largo) y descubre el producto; en escritorio va horizontal (capas rotadas 90°) y centrada, en móvil vertical con la base fija, como una secuencia de fotos real. No mezcles fotogramas distintos con fundidos: si las tapas no miden igual, la caja "brinca". Usa la foto de **mayor resolución** (el empaque debe medir ≥ 300 px de ancho en el original; escala ×2 con Lanczos + enfoque suave) y pon la franja de sombra bajo la tapa en la capa de la tapa para que se mueva con ella. Recorta la base con `clip-path` para que no asome por encima de la tapa cerrada. Por defecto **no fijes la sección** (`position:sticky`): el cliente prefiere que la página siga de largo y la caja se abra mientras cruza la pantalla (progreso = (0.98·alto − top)/(0.62·alto)). `html.owd-u1/u2/u3` encienden los titulares.
- **Diseña tu caja** (`[data-owd-boxlab]`): caja 3D en CSS (6 caras). **Toma las proporciones de fotos reales del empaque** (BADDIE: largo 3.3 : ancho 1 : alto 0.5 → `--d:.30w`, `--h:.15w`) y pon logo y frase donde van en el empaque real (arriba, la frase bajo el logo, `.owd-slogan`). Acabado de lujo: degradado con luz en la tapa, bordes con brillo (`inset` claros), textura de papel (ruido SVG en `::after`), lados más oscuros y sombra difusa en el piso; arrastrar para girar (`--by/--bx` en `<html>`), estilo de letra con `html.owd-box-serif`, botón que pasa la frase al formulario del evento.
- **Test "¿Qué … eres?"** (`[data-owd-quiz]` con botón `[data-owd-quiz-start]`): 3 preguntas, resultado con foto del producto en el círculo (`.owd-quiz-photo`), frase, botón de WhatsApp con el mensaje ya escrito y compartir (Web Share o copiar). Configura `BRAND`, `SHARE_PATH`, `Q` y `R` en el JS. **El resultado siempre es uno de los productos principales** (no un complemento como una salsa); la foto es un recorte cuadrado del producto (`img`).
- **Abierto ahora** (`.owd-open` con `.owd-open-yes` / `.owd-open-no`): `html.owd-open-now` o `html.owd-closed` según la hora de la ciudad (Intl, zona horaria); también pinta un punto en el botón de WhatsApp del header.
- **Carrete horizontal** (`.owd-reel` > `.owd-reel-stage` > `.owd-reel-track` con `.owd-frame`): fijo en escritorio, el scroll vertical lo recorre de lado; en móvil, deslizar con *scroll-snap*.
- **Franja que reacciona** (`html.owd-mq-js` + `--owd-mq`): acelera con la velocidad del scroll y cambia de dirección.
- **Lista con foto flotante** (`.owd-explore a[data-owd-img]`): una foto sigue al cursor al pasar por cada enlace.
- **Transiciones de cine**: `@view-transition{navigation:auto}` + `view-transition-name` en header, titular y una foto compartida (`.owd-vt-pizza`). Si el navegador las soporta (`'onpagereveal' in window`), la cortinilla del monograma se omite.
- Atributos de datos en QWeb siempre con valor (`data-owd-quiz="1"`): sin valor el XML no es válido.
- Las secciones fijas (`position:sticky`) necesitan que ningún contenedor tenga `overflow:hidden`; usa `overflow-x:clip`. Odoo agrega pseudo-elementos en `.container`: en rejillas, coloca cada hijo con `grid-column/grid-row` explícitos.

## Rendimiento (el cliente notó que el sitio "se trababa")
- **Nunca** cambies variables CSS o clases en `<html>` en cada cuadro: obliga a recalcular el estilo de toda la página ~60 veces por segundo. Pon la variable o clase **en el elemento de la sección** (`section.style.setProperty('--owd-u', …)`, `track.style.transform = …`) y límpialo al abrir el editor.
- Actualiza solo si el valor cambió (redondea, guarda el último) y solo si la sección está cerca de la pantalla; usa un solo `requestAnimationFrame` por evento de scroll.
- Ciclos continuos (franja en movimiento) solo cuando el elemento es visible (`IntersectionObserver`) y la pestaña está activa. Nada de giros automáticos infinitos.
- Anima solo `transform` y `opacity`. Las barras de progreso con `scaleX`, no con `width`; sin `box-shadow` animado en ciclo.
- Evita `mix-blend-mode` en elementos que se transforman (texturas en caras 3D): usa opacidad baja normal.

## Carrito y proceso de pago (tema oscuro)
El tema pinta `.card-body` con fondo claro semitransparente y las celdas de tabla con `box-shadow` (`--bs-table-bg`): en un sitio oscuro el resumen queda con texto del mismo color que el fondo. Con alcance `body[class*="o_website_sale"]`:
- Tarjetas oscuras y `.card-body` transparente; `--bs-table-bg`/`--bs-table-color` transparentes/claros.
- `.text-muted`, `small`, `.o_portal_address` con `!important` (Odoo las oscurece dentro de tarjetas).
- `.js_delete_product.btn-link` y "Guardar para después" como enlaces sin recuadro; `.css_quantity` como una sola píldora.
- Insignias (`.badge`, incluso `text-bg-info`) con borde de acento, sin azul.
- Móvil: `.o_mobile_summary.bg-body` (barra fija de abajo) también en fondo oscuro.
- Paso de factura de México: `/shop/l10n_mx_invoicing_info` (botones `.btn-check`).
Prueba con un producto en el carrito como visitante y cancela después la cotización que se crea.
