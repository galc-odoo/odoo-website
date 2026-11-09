---
name: "odoo-web-design"
description: "Diseña y construye sitios web high end en Odoo vía API a partir de un PDF de concepto, imágenes, ligas de referencia e info del cliente: maqueta navegable, páginas con bloques nativos editables, diseño y JavaScript en el código personalizado del sitio (sin tocar plantillas, resistente a migraciones), estilo de Tienda, SEO, optimización de fotos y auditoría final. Úsalo para crear, rediseñar o mejorar un sitio web o la estética de una tienda en Odoo."
---

# Diseño web y e-commerce en Odoo

Flujo de 6 fases, siempre en orden: **Levantamiento → Diagnóstico → Brief y maqueta → Construcción → Tienda (si aplica) → Validación y entrega**. Una fase a la vez; al terminar cada una, resume en 2–3 líneas qué se hizo y qué sigue, y pide aprobación. **Nada se escribe en Odoo sin un "sí" explícito del consultor en esa fase.**

## Archivos del skill

| Archivo | Para qué |
|---|---|
| `reference/diseno.md` | Dirección visual high end, tokens, componentes probados, maqueta, fotos. Léelo en la Fase 2. |
| `reference/odoo-tecnico.md` | Trampas de Odoo 17–20 (traducciones, `src.translate`, copias por sitio, URLs, editor, formularios). Léelo antes de la Fase 3. |
| `reference/js-css-patrones.md` | Cómo arrancar el CSS/JS base, alcances, animaciones seguras, detalles finos. |
| `reference/entrega.md` | Checklist final, bitácora, guía para el cliente. |
| `scripts/odoo_rpc.py` | Conexión (credenciales por variables de entorno), idiomas activos, respaldos. |
| `scripts/push_code.py` | Sube CSS + JS + footer al código personalizado del sitio, con respaldo. |
| `scripts/bloques.py` | Helpers para armar páginas con bloques nativos (titulares, tarjetas, vistas previas, equipo/cofundadores, formularios). |
| `scripts/escribir_pagina.py` | Crea o actualiza una página propia en todos los idiomas, con protecciones. |
| `scripts/optimizar_imagenes.py` | Recomprime fotos pesadas y cambia `src`/`src.translate`. |
| `scripts/centrar_zoom.py` | Calcula el acercamiento centrado (`data-tf`) para vistas previas. |
| `scripts/auditar_sitio.py` | Auditoría pública: estado, SEO, alt, peso, enlaces rotos, restos de plantilla. |
| `assets/base.css`, `assets/base.js`, `assets/footer.html` | Plantillas base (paleta en tokens, prefijo `.owd-`). |

Trabaja en una carpeta por cliente: `levantamiento.md`, `diagnostico.md`, `maqueta/`, `odoo/` (`sitio.css`, `sitio.js`, `footer.html`, `paginas/*.xml` o `paginas.py`), `respaldo/`, `cambios.json`, `bitacora.md`.

## Regla principal · Dónde vive cada cambio (resistente a migraciones)

Las plantillas estándar y heredadas se reinician o se rompen al migrar. Por eso:

| Qué | Dónde va | Nunca |
|---|---|---|
| **Estilos** | `website.custom_code_head`, un bloque `<style id="odoo_web_design_<cliente>">` + `<link>` de Google Fonts (Sitio web → Configuración → Código personalizado) | `ir.asset`, SCSS en vistas, `style` repartidos en plantillas |
| **JavaScript** | `website.custom_code_footer`, un `<script id="odoo_web_design_<cliente>_js">` | Vistas heredadas, `ir.asset` JS, módulos |
| **Footer** | HTML propio en `custom_code_footer` (antes del script) + `footer#bottom{display:none}` | Reescribir `website.footer_custom` |
| **Header** | Opciones nativas (logo: `website.option_header_brand_logo`) + CSS. Botón de acción = `website.menu` con estilo de botón | Reescribir el `arch` del header o de `website.header_call_to_action` |
| **Páginas nuevas** | `website.page` + su vista propia con bloques nativos (`scripts/escribir_pagina.py`). **Única vista que se escribe por API.** | — |
| **Páginas estándar** (Contáctanos, Privacidad, Tienda, Carrito, Pago) | Solo CSS con su clase de `body`. Si necesitan otro contenido: página nueva (`/contacto`), **despublicar** la estándar y `website.rewrite` 301 | Escribir su `arch`, ni con copia por sitio |
| **Logo, favicon, datos** | Campos de `website` y `res.company` | Imágenes dentro de plantillas |

1. Prohibido por API `write`/`create` de `arch`/`arch_db` en vistas con XML ID, con `inherit_id` o sin `website_id`. Activar o desactivar vistas de opción sí se permite (es lo que hace el editor) y se anota en la bitácora.
2. Si algo **solo** se logra tocando una plantilla, dilo, ofrece la alternativa con CSS/JS/menú y espera la decisión.
3. Todo el CSS con alcance (`.owd-site`, `body[class*="o_website_sale"]`…). El JS nunca modifica `#wrap`, `header` ni `footer`, solo agrega a `body`, y no corre en modo edición.
4. Animaciones de aparición y *parallax* en CSS (`animation-timeline: view()`), no en JS.

## Fase 0 · Levantamiento

Pide lo que falte (AskUserQuestion o texto). Sin los puntos con * no se avanza:

1. *Accesos: URL, base, usuario y API key (Ajustes → Usuarios → Seguridad de la cuenta → Claves API). ¿**Prueba o producción**? Si es producción, recomienda duplicar; si siguen en producción, las páginas nuevas se crean **sin publicar** y se publica con el consultor.
2. *Alcance: solo sitio informativo, o sitio + tienda.
3. *Empresa: nombre, giro, propuesta de valor, público, productos/servicios, **WhatsApp confirmado**, correo, dirección que se puede mostrar, redes, logos (monograma, logotipo, claim), idioma.
4. *Objetivo: 1 acción principal (pedir por WhatsApp, cotizar, comprar, agendar) y máx. 2 secundarias.
5. PDF de concepto, imágenes y ligas de referencia (qué le gusta de cada una).
6. Páginas deseadas y comportamientos especiales (transiciones, vistas previas, formularios). Nombres de páginas y menús en el idioma del cliente.

Guarda en `levantamiento.md`. Credenciales solo en variables de entorno (`ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_KEY` o `ODOO_KEY_FILE` con chmod 600); nunca en el chat ni en entregables.

## Fase 1 · Diagnóstico (solo lectura)

Con `scripts/odoo_rpc.py` levanta y resume en `diagnostico.md`:
- Versión y plataforma; **idiomas activos**; módulos (`website`, `website_sale`, `website_crm`, `theme_*`…).
- Sitio: dominio, tema, logo, favicon, `custom_code_head/footer` actuales, header (plantilla y opciones activas), si el header es *overlay*.
- Páginas (`website.page`: url, publicada, vista, `write_date`), menús, y **vistas estándar ya modificadas o copiadas por sitio** (riesgo de migración).
- Imágenes del cliente ya subidas (`ir.attachment` públicos del usuario) con su resolución.
- Compañía, productos (con/sin foto, precio, descripción, publicados), categorías públicas, pagos y envíos si hay tienda.
- Si el sitio ya está publicado, corre `scripts/auditar_sitio.py` para tener la línea base.

Presenta un resumen corto con números y una recomendación.

## Fase 2 · Brief y maqueta

Sigue `reference/diseno.md`:
1. Lee el PDF/imágenes (renderiza páginas a imagen), extrae estructura, textos y notas de interacción. Prepara logos transparentes y recortes de fotos.
2. **Brief** (Doc): objetivo, público, acción principal, tokens de color y tipografía, tono, mapa del sitio, secciones por página, interacciones.
3. **Maqueta** (artifact HTML) con cada página por separado y transición entre ellas. Itera con el consultor hasta aprobar. Se replica el estilo de las referencias, nunca su identidad (logos, textos, fotos ajenas).

## Fase 3 · Construcción (con aprobación)

Antes de escribir, muestra la lista exacta de cambios indicando en qué fila de la Regla principal cae cada uno, y espera el "sí". Respalda todo en `respaldo/` (los scripts lo hacen solos).

1. **Identidad**: `website.logo` (logotipo claro sin fondo), `website.favicon` (monograma sobre color de marca), imágenes como adjuntos públicos (`res_model='ir.ui.view'`, `public=True`, nombre `<cliente>_…`, WebP ~85).
2. **Código del sitio**: copia `assets/` a `odoo/`, ajusta tokens, footer y configuración del JS, y sube con `scripts/push_code.py`. Cada actualización reemplaza el bloque completo.
3. **Header**: plantilla nativa más cercana, logo por opción, botón de acción como `website.menu`, ocultar buscador/lista de deseos/inicio de sesión en páginas informativas con CSS.
4. **Páginas**: arma el `arch` con `scripts/bloques.py` y escríbelo con `scripts/escribir_pagina.py` (todos los idiomas, protecciones, respaldo). Titulares multilínea con `<br/>` en un solo span. Relee antes de cada cambio: el cliente puede estar editando. Si la base es de producción, crea sin `--publicar` y publica al final con el consultor (avisa que los botones a páginas sin publicar dan 404).
5. **URLs y menús**: en el idioma del cliente, sin acentos; URL con `update_field_translations`; `website.rewrite` 301 desde la anterior.
6. **Formularios** en páginas propias con `bloques.formulario()` hacia `crm.lead` (o el modelo acordado).
7. **Páginas estándar**: estilo con CSS; si requieren otro contenido, página nueva + despublicar + 301 (escribe nombre/publicación de la estándar **sin** contexto de sitio).
8. **SEO** por página (título, descripción, imagen al compartir) en todos los idiomas; `alt` en todas las imágenes. Optimiza fotos pesadas con `scripts/optimizar_imagenes.py`.
9. **JS a la medida** solo si no hay opción nativa; patrones en `reference/js-css-patrones.md`. En Odoo Online avisa que el código propio puede requerir ajuste en actualizaciones.

No instales módulos ni temas sin aprobación; no toques nada fuera del `website_id` acordado.

## Fase 4 · Tienda (solo si el alcance lo incluye)

1. Instalar `website_sale` (y `website_sale_stock`) solo con confirmación.
2. Categorías públicas, selección de productos con el consultor (`is_published`, `public_categ_ids`, imagen ≥ 1000 px, descripción, precio, atributos). Nunca inventes precios ni datos técnicos; reporta lo que falta.
3. Listas de precios, impuestos mostrados, moneda; pagos y envíos (las llaves de pago las configura el cliente).
4. Ajustes de tienda con opciones nativas (checkout invitado, stock, wishlist, términos).
5. **Estética de la Tienda solo con CSS** (ya incluida en `assets/base.css`): catálogo `body.o_website_sale_products`, ficha `body.o_website_sale_product`, carrito y pago `body.o_website_sale_checkout`. Titular display, categorías como píldoras, tarjetas con marco y acercamiento, precio en acento, botón principal claro sobre oscuro.
6. **Carrito y pago en sitio oscuro** (bloque "tienda oscura" de `assets/base.css`): el tema deja el resumen con texto del mismo color que el fondo y los botones Eliminar / Guardar para después con recuadro. Resumen oscuro con total en acento, enlaces sin recuadro, cantidad en una píldora, insignias con contorno, opciones en acento y la barra fija de móvil (`.o_mobile_summary`) oscura. Revisa los 4 pasos: Orden → Dirección → Facturación (México: `/shop/l10n_mx_invoicing_info`) → Pago, en 1440 y 375 px.
7. **Prueba del proceso**: con permiso del consultor, agrega un producto como visitante, llena la dirección con datos de prueba (`Prueba <cliente>`, `prueba@example.com`) y llega hasta Pago **sin pagar**. Al terminar, cancela la cotización que se crea (`sale.order` → `action_cancel`) y avisa del contacto de prueba para borrarlo. Si sale "No hay métodos de pago disponibles", el cliente debe activar un proveedor de pago (no captures llaves).
8. Carga por lotes, IDs en `cambios.json`.

## Fase 5 · Validación y entrega

Sigue `reference/entrega.md`: auditoría con `scripts/auditar_sitio.py`, revisión en 1440/1024/375 px con capturas, interacciones y consola, formularios, SEO, peso, restos de plantilla y **nota de migración** (ninguna plantilla modificada). Entrega bitácora, guía corta para el cliente y pendientes.

## Reglas generales

- Base de prueba primero; producción solo con aprobación y sobre respaldo.
- Nunca imprimas la API key; nunca envíes datos del cliente a servicios no pedidos.
- Respeta lo que el cliente cambia en el editor (nombres, fotos, textos): cambia solo lo pedido.
- Todo lo creado se identifica con `odoo_web_design.<cliente>` o el prefijo `<cliente>_` para no duplicarlo si se vuelve a correr.
- Lo que viva en un módulo propio (Odoo.sh / on-premise) se le deja al desarrollador con la especificación.
- Si algo no se puede sin desarrollo o sin tocar una plantilla, dilo y ofrece la alternativa nativa o con CSS/JS más cercana.
