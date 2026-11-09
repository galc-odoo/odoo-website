---
name: "odoo-web-design"
description: "Diseña, construye y valida el sitio web de cualquier cliente en Odoo 17–20 por API: pide accesos, contexto, maqueta en PDF e imágenes; muestra una vista previa en vivo sin tocar la base; recomienda transiciones, animaciones e interactivos según el giro; construye con bloques nativos y CSS/JS en el código personalizado del sitio (nunca en vistas); y al final recorre el sitio como usuario dando clic a todo frente al consultor. Úsalo para crear, rediseñar o mejorar un sitio web o la estética de una tienda en Odoo."
---

# Sitios web en Odoo: de la maqueta al recorrido como usuario

Herramienta para hacer **el sitio que sea** (restaurante, despacho, industria, estudio, tienda…), no para copiar uno anterior. El diseño sale de la información del cliente; los temas y bloques del skill son puntos de partida.

**Forma de trabajo:** 9 pasos en este orden. **Pide una sola cosa a la vez y espera la respuesta** antes de seguir. Al terminar cada paso di en 1–2 líneas qué se hizo y qué sigue. Quien usa el skill es el **diseñador** (consultor): él aprueba; nada se escribe en Odoo sin su "sí" explícito.

## Archivos

| Archivo | Para qué |
|---|---|
| `reference/diseno.md` | Cómo elegir dirección visual, tokens y oficio para que se vea *high end*. Paso 5. |
| `reference/componentes.md` | Catálogo de bloques y efectos: qué es, cuándo usarlo, función de `bloques.py` y módulo. Pasos 5–6. |
| `reference/odoo-tecnico.md` | Trampas de Odoo 17–20 (traducciones, copias por sitio, URLs, editor, SEO, carrito). Antes del paso 7. |
| `reference/js-css-patrones.md` | Reglas del CSS/JS: alcance, modo edición, rendimiento. Paso 7. |
| `reference/recorrido.md` | Protocolo del recorrido como usuario y del reporte. Paso 9. |
| `reference/entrega.md` | Bitácora, guía para el cliente, pendientes. |
| `assets/temas/*.json` | 5 direcciones de partida (editorial oscuro, minimal claro, corporativo, cálido artesanal, tecnológico oscuro). |
| `assets/css/*.css`, `assets/js/*.js` | Módulos: `nucleo`, `header-footer`, `tienda`, `contenido`, `efectos`, `interactivos`, `empaque`. Todo con variables del tema. |
| `assets/footer.html` | Footer propio con marcadores `{{…}}`. |
| `assets/revisar_pagina.js` | Revisión de una página en el navegador (contraste, fotos, desbordes, enlaces, restos de plantilla). |
| `scripts/odoo_rpc.py` | Conexión por variables de entorno, idiomas, respaldos. |
| `scripts/armar.py` | `marca.json` → `sitio.css` + `sitio.js` + fuentes, con revisión de contraste. |
| `scripts/vista_previa.py` | Vista previa local con estructura de Odoo, sin tocar la base. |
| `scripts/bloques.py` | Funciones para armar páginas con bloques nativos editables. |
| `scripts/escribir_pagina.py` | Crea o actualiza una página propia en todos los idiomas, con respaldo. |
| `scripts/push_code.py` | Sube CSS, JS y footer al código personalizado del sitio, con respaldo. |
| `scripts/optimizar_imagenes.py`, `centrar_zoom.py` | Fotos ligeras y acercamientos centrados. |
| `scripts/recorrido.py`, `auditar_sitio.py` | Rastreo del sitio publicado (páginas, enlaces, formularios) y auditoría SEO. |

Carpeta por cliente: `clientes/<cliente>/` con `levantamiento.md`, `diagnostico.md`, `maqueta/`, `odoo/` (`marca.json`, `footer.html`, `paginas.py`, `sitio.css`, `sitio.js`), `respaldo/`, `recorrido/`, `bitacora.md`. Nunca va al repositorio del skill.

## Regla principal · dónde vive cada cambio

Las plantillas estándar y heredadas se reinician o se rompen al migrar. Por mantenimiento, **todo el código va en un solo lugar**:

| Qué | Dónde | Nunca |
|---|---|---|
| CSS | `website.custom_code_head` (Sitio web ‣ Configuración ‣ Código personalizado), un `<style id="odoo_web_design_<cliente>">` | Vistas, `ir.asset`, `style` repartidos |
| JavaScript | `website.custom_code_footer`, un `<script id="odoo_web_design_<cliente>_js">` | Vistas heredadas, módulos |
| Footer | HTML propio en `custom_code_footer` + `footer#bottom{display:none}` | Reescribir el footer de la plantilla |
| Header | Opciones nativas + CSS; botón de acción = `website.menu` | Reescribir el `arch` del header |
| Páginas nuevas | `website.page` + vista propia con bloques nativos (**única vista que se escribe por API**) | — |
| Páginas estándar (Tienda, Carrito, Pago, Contáctanos) | Solo CSS por su clase de `body`; si necesitan otro contenido, página nueva + despublicar + 301 | Escribir su `arch` |

Prohibido escribir `arch`/`arch_db` en vistas con XML ID, con `inherit_id` o sin `website_id`. Si algo **solo** se logra tocando una plantilla, dilo y ofrece la alternativa con CSS/JS/menú.

## Paso 1 · Accesos de la base (API RPC)

Pide URL, base, usuario y API key (Ajustes ‣ Usuarios ‣ Seguridad de la cuenta ‣ Claves API) y si es **prueba o producción** (en producción recomienda una copia; si siguen ahí, las páginas nuevas se crean sin publicar). Guarda la llave solo en un archivo `chmod 600` (`ODOO_KEY_FILE`), nunca en el chat ni en entregables.
Con `scripts/odoo_rpc.py` haz el diagnóstico **en solo lectura** y resúmelo en `diagnostico.md`: versión, idiomas activos, módulos (`website_sale`, `website_crm`…), dominio y si robots bloquea, tema y header, páginas y menús, código personalizado actual, vistas estándar ya modificadas, imágenes subidas, compañía, productos y pagos si hay tienda. Si el sitio está publicado, corre `scripts/recorrido.py` como línea base.

## Paso 2 · Contexto del cliente

Pide en texto libre: qué hace, a quién le vende, propuesta de valor, **acción principal** del sitio (pedir por WhatsApp, cotizar, comprar, agendar, llamar) y máx. 2 secundarias, datos de contacto confirmados, redes, idioma(s), tono. Si hay tienda o no. Guarda en `levantamiento.md`.

## Paso 3 · Maqueta en PDF

Pide el PDF con **todas las páginas** y, si las tiene en mente, las modificaciones con JS y CSS que le gustaría ver (transiciones, efectos al pasar el cursor, cosas que se mueven). Si no hay maqueta, ofrece armar el mapa del sitio con el catálogo de `reference/componentes.md`. Lee el PDF página por página (renderízalo a imagen) y extrae estructura, textos y notas de interacción.

## Paso 4 · Imágenes principales

Pide logos (monograma, logotipo, logotipo con claim) y las fotos principales **solo como referencia**: el diseñador puede cambiarlas después. Revisa resolución; prepara logos transparentes y recortes.

## Paso 5 · Análisis y vista previa en vivo (sin tocar la base)

1. Elige con el diseñador la dirección: parte del tema de `assets/temas/` más cercano al giro y ajústalo a la marca en `odoo/marca.json` (colores, fuentes, títulos en itálica o mayúsculas, radios, espaciado, módulos). `scripts/armar.py` revisa el contraste y se detiene si algo no se lee.
2. Arma las páginas en `odoo/paginas.py` (`PAGINAS = {'/': [...], '/nosotros': [...]}`) con `scripts/bloques.py`, con los textos reales del cliente.
3. Genera la vista previa (`scripts/vista_previa.py --marca … --paginas …`), sírvela con el servidor de vista previa del entorno y **ábrela en la ventana del navegador al lado** del chat. Ve enseñando cada página conforme queda, en escritorio y celular. Corre `owdRevisar()` (`assets/revisar_pagina.js`) en cada página antes de mostrarla.
4. Itera hasta que el diseñador apruebe. Aquí **nada** se escribe en Odoo.

## Paso 6 · Recomendaciones para que se vea pulcro y fuera de lo común

Propón 4–6 ideas concretas para **este** negocio, con dónde irían y por qué, elegidas de `reference/componentes.md` (sección Efectos e Interactivos) o diseñadas a la medida: transición entre páginas con el monograma, botones que se rellenan o siguen al cursor, fotos que se acercan al elemento elegido, galería ampliada, franja que reacciona al scroll, carrete horizontal, test "¿qué … eres?" con resultado y botón de acción, horario "abierto ahora", caja o producto que se abre con el scroll, calculadoras o formularios con lógica según el giro. Muéstralas en la vista previa y deja que el diseñador elija. Nada de efectos que estorben (cursores con texto, fotos flotantes) si no los pide. Cuida rendimiento (ver `js-css-patrones.md`).

## Paso 7 · Construcción en la base (con aprobación)

Pide permiso explícito para modificar la base del cliente, con la **lista exacta** de cambios y en qué fila de la Regla principal cae cada uno. Con el "sí":
1. Identidad: logo y favicon del sitio; imágenes como adjuntos públicos WebP.
2. Código: `armar.py` → `push_code.py` (CSS y JS al **editor de código personalizado**; reemplaza el bloque completo y respalda).
3. Páginas con `escribir_pagina.py` (todos los idiomas, respaldo, relee antes de escribir: el cliente puede estar editando). En producción, sin publicar.
4. Menús y URLs en el idioma del cliente, sin acentos, con 301 desde las anteriores; header y footer; formularios nativos (`crm.lead` u otro modelo acordado); SEO por página, `alt` en fotos, robots, llms.txt y datos estructurados.
5. Tienda (si aplica): solo estética con el módulo `tienda`; productos, precios y pagos no se tocan sin pedirlo.

## Paso 8 · Revisión del diseñador

Pide al diseñador que revise el sitio en Odoo (escritorio y celular, y en el editor). Haz los cambios que pida, uno por uno, mostrando el resultado, hasta que diga que todo está correcto.

## Paso 9 · Recorrido como usuario

Cuando el diseñador confirme, **pide permiso para entrar como usuario** a validar. Sigue `reference/recorrido.md`: rastreo con `scripts/recorrido.py`, y en la ventana del navegador al lado, sin sesión, **da clic a todo mientras el diseñador mira**: menú, cada botón y enlace, formularios (validación; envío real solo con permiso), menú del celular, transiciones y Atrás, tienda hasta el pago sin pagar. Revisa que todo haga sentido, que los colores combinen en todos los bloques, que se lea bien y que la experiencia sea agradable. Corrige lo que encuentres (con aprobación si toca la base), vuelve a verificar y entrega `recorrido/reporte.md` con capturas.

## Reglas generales

- Un paso a la vez; nunca pidas todo junto.
- Base de prueba primero; producción solo con aprobación y respaldo.
- Nunca imprimas la API key ni envíes datos del cliente a servicios no pedidos.
- Respeta lo que el cliente cambia en el editor; cambia solo lo pedido.
- Replica el estilo de las referencias, nunca su identidad (logos, textos, fotos ajenas). Reseñas solo reales.
- Todo lo creado lleva `odoo_web_design.<cliente>` o el prefijo `<cliente>_` para no duplicarlo.
- Si algo no se puede sin desarrollo, dilo y ofrece la alternativa más cercana.
