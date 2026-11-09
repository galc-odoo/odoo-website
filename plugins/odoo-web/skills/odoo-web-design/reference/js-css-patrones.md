# CSS y JS: patrones seguros

Todo vive en el código personalizado del sitio (`custom_code_head` / `custom_code_footer`). Nunca en vistas.

## Flujo de código

1. Copia el tema más cercano de `assets/temas/` a `clientes/<cliente>/odoo/marca.json` y ajústalo (ver `diseno.md`). Copia `assets/footer.html` y reemplaza los `{{…}}`.
2. `python scripts/armar.py --marca odoo/marca.json` → `odoo/sitio.css` (variables `:root` + módulos), `odoo/sitio.js` (`window.OWD_CONFIG` + módulos) y `odoo/fuentes.txt`.
3. Revisa con `vista_previa.py`. Al aprobarse: `python scripts/push_code.py --cliente <slug> --css odoo/sitio.css --js odoo/sitio.js --footer odoo/footer.html --fonts "$(cat odoo/fuentes.txt)"` (primero con `--dry-run`).
4. Cada cambio posterior: se edita `marca.json`, el módulo o `css_extra`, se vuelve a armar y se sube el bloque completo. Nunca se edita el CSS a mano dentro de Odoo, para que el código fuente y lo publicado no se separen.

## Módulos

| Módulo | Contenido |
|---|---|
| `nucleo` | Tipografía, botones, secciones, bloques de página, vista previa, transición entre páginas, aviso legal. |
| `header-footer` | Footer propio, botón de acción del header, botón flotante. |
| `tienda` | Catálogo, ficha, carrito y pago con los colores del tema. |
| `contenido` | Horarios, preguntas, paquetes, notas, reseñas, equipo. |
| `efectos` | Intro, botones magnéticos, galería ampliada, menú móvil a pantalla completa, cursor opcional. |
| `interactivos` | Abierto ahora, franja, carrete, test, lista explora, View Transitions. |
| `empaque` | Caja que se abre y "diseña tu caja". |

**Reglas para escribir CSS nuevo** (en un módulo o en `css_extra`): colores solo con variables (`--owd-bg`, `--owd-surface`, `--owd-text`, `--owd-mute`, `--owd-accent`, `--owd-on-accent`, `--owd-brand`, `--owd-on-brand`, `--owd-accent-on-brand`, `--owd-rule`) y transparencias con `color-mix(in srgb, var(--owd-text) 20%, transparent)`; títulos con `--owd-display`, `--owd-display-style`, `--owd-display-case`, `--owd-display-weight`; etiquetas con `calc(.3em * var(--owd-track))` y `--owd-label-case`; radios con `--owd-radius`, `--owd-pill`, `--owd-btn-radius`. Sobre el color de marca (footer, menú móvil, botón flotante) el texto es `--owd-on-brand`, nunca `--owd-text`. Prueba siempre con un tema claro y uno oscuro.

## Alcance (para no afectar lo que no se pidió)

| Zona | Selector |
|---|---|
| Páginas propias | `.owd-site …` y `body:has(.owd-site) …` |
| Tienda | `body.o_website_sale_products`, `body.o_website_sale_product`, `body.o_website_sale_checkout` (todas: `body[class*="o_website_sale"]`) |
| Header | `header …` (también es el de la Tienda) |
| Footer propio | `.owd-sitefooter …`; el de la plantilla: `footer#bottom{display:none!important}` |

## Animaciones sin JS

```css
@supports (animation-timeline: view()){
  .owd-site .owd-rv{animation:owd-reveal linear both;animation-timeline:view();animation-range:entry 0% entry 70%}
}
body.editor_enable .owd-site *{animation:none!important}
@media (prefers-reduced-motion:reduce){.owd-site *{animation:none!important;transition:none!important}}
```
El estado en reposo siempre es visible (nunca `opacity:0` esperando a un observer).

## JS

- Configuración solo en `OWD_CONFIG` (lo escribe `armar.py` desde `marca.json`): `paginas`, `whatsapp`, `botonFlotante`, `botonFlotanteUrl`, `cursor`, `horario`, `formulario`, `quiz`.
- `editing()` = `body.editor_enable` o existe `.o_editable`. Nada corre en modo edición; lo que se agregó se quita y lo que se cambió se restaura al abrir el editor (MutationObserver sobre la clase de `body`).
- El JS nunca modifica `#wrap`, `header` ni `footer`: solo agrega elementos a `body`.
- Atributos de datos en QWeb siempre con valor (`data-owd-quiz="1"`): sin valor el XML no es válido.
- Secciones fijas (`position:sticky`) necesitan que ningún contenedor tenga `overflow:hidden`; usa `overflow-x:clip`. Odoo agrega pseudo-elementos en `.container`: en rejillas, coloca cada hijo con `grid-column/grid-row` explícitos.

## Rendimiento

- **Nunca** cambies variables o clases en `<html>` en cada cuadro (recalcula el estilo de toda la página): ponlas en el elemento de la sección y límpialas al abrir el editor.
- Actualiza solo si el valor cambió y la sección está cerca de la pantalla; un solo `requestAnimationFrame` por evento de scroll.
- Ciclos continuos solo con el elemento visible (`IntersectionObserver`) y la pestaña activa.
- Anima solo `transform` y `opacity`; barras con `scaleX`; sin `mix-blend-mode` en elementos que se transforman.

## Detalles que los clientes notaron

- Acentos que chocan con la línea de arriba: `margin-bottom ≥ 22px` en el eyebrow y `line-height:1` + `padding-top:.08em` en titulares en mayúsculas.
- Títulos largos en columnas: baja `font-size` con `clamp` y revisa en 1440, 1024 y 375 px. En móvil `font-size:min(12vw,58px)`.
- El botón flotante no tapa el pie: `padding-bottom` extra en móvil.
- Galerías y retratos del mismo tamaño; equipo con el mismo formato que el fundador.
- Sin etiquetas sobre las fotos de producto, sin cursores con texto ni fotos flotantes si no los piden.
- Enlaces nunca en rojo saturado.

## Acercamiento centrado

`python scripts/centrar_zoom.py --img foto.webp --puntos "0.20,0.52" "0.50,0.52" --escala 2.5 --caja 1` → `data-tf` para `item_preview()`.

## Caja que se abre (módulo `empaque`)

Una sola foto cenital del empaque abierto, en alta (≥ 300 px de ancho del empaque en el original; ×2 con Lanczos), cortada en **base** y **tapa** justo en el borde de la tapa (la franja de sombra va con la tapa). La tapa se desliza con `--owd-u` (0→1); horizontal en escritorio, vertical en móvil. No fijes la sección: la página sigue de largo (progreso = (0.98·alto − top)/(0.62·alto)). "Diseña tu caja": proporciones reales del empaque y la frase donde va en el empaque real.

## Carrito y pago (módulo `tienda`)

El tema pinta `.card-body` claro y las celdas de tabla con `box-shadow` (`--bs-table-bg`); en un sitio oscuro el resumen queda ilegible. El módulo ya lo corrige: tarjetas con `--owd-surface`, tabla transparente, `.text-muted`/`small`/`.o_portal_address` con `!important`, "Eliminar" y "Guardar para después" como enlaces, cantidad en una píldora, insignias con contorno, barra fija de móvil (`.o_mobile_summary.bg-body`), botones de factura de México (`/shop/l10n_mx_invoicing_info`, `.btn-check`). Pruébalo en el recorrido hasta el pago sin pagar y cancela la cotización.
