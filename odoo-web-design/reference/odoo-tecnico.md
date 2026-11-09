# Notas técnicas de Odoo (17–20) para sitios web por API

Problemas reales que aparecieron en proyectos y cómo evitarlos.

## Conexión y lectura
- JSON-RPC `/jsonrpc`. Un `execute_kw` sin `context.lang` trabaja en `en_US`, aunque el usuario esté en español.
- En Odoo 20 el binario de `ir.attachment` es `raw` (no `datas`) y se lee como `{'filename', 'content'(base64), 'size'}`. Al crear, `raw` acepta base64.
- `payment.provider` ya no tiene `state` en algunas versiones: lee `fields_get` antes de filtrar.
- Odoo Online responde 502 de vez en cuando: reintenta (ya lo hace `scripts/odoo_rpc.py`).
- Para listar imágenes del cliente: `ir.attachment` con `mimetype like image`, `create_uid = usuario`, `original_id = False`.

## Traducciones (la fuente de errores más común)
- `arch_db`, `website.page.url`, `website.menu.url`, `name` y los metadatos SEO son **traducibles**. Escribe el mismo valor en **todos** los idiomas activos; si no, un `write` en un idioma "sincroniza" términos y puede regresar contenido viejo en el otro.
- Las imágenes llevan `src` y una copia traducida `src.translate` (y `srcset.translate`). Al cambiar una foto por API cambia ambos; si no, la página en español sigue mostrando la foto anterior.
- Para cambiar URLs usa `update_field_translations([id], 'url', {lang: '/nueva'})`. Un `write({'url': …})` intenta crear la redirección con la petición web y falla por API (`'NoneType' object has no attribute 'session'`), a veces dejando la URL a medias (`/como-pedir-1`).
- Agrega `website.rewrite` (`redirect_type='301'`) de la URL anterior a la nueva. Las URLs van sin acentos.

## Copias por sitio (copy-on-write)
- Escribir en una vista o página **genérica** (`website_id = False`) con `context={'website_id': 1}` crea una copia del sitio. Eso aplica también a `website.page.write({'name': …})`: renombrar una página estándar con contexto de sitio crea copias de la página y de la vista, y además puede **renombrar la clave** de la vista (`website.contactus` → `website.contacto`).
- Para datos de páginas estándar (nombre, publicada, SEO) escribe **sin** `website_id` en el contexto.
- Una vista con XML ID (`ir.model.data`) o con `inherit_id` es de módulo: no se edita por API (regla de migración). `scripts/escribir_pagina.py` lo valida.
- Algunas vistas estándar tienen herencias que esperan elementos concretos (por ejemplo `website_crm.contactus_form` busca `t-set="contactus_form_values"` en Contáctanos). Otra razón para crear páginas nuevas en vez de reescribir las estándar.

## Páginas
- Crear página propia: `ir.ui.view` (`type='qweb'`, `key='website.<slug>'`, `website_id`, `arch_db`) + `website.page` (`url`, `view_id`, `website_id`, `is_published`). La plantilla llama a `website.layout`; la de inicio lleva `pageName.f="homepage"`.
- Odoo sirve primero una página **publicada** y solo después aplica `website.rewrite`. Para redirigir `/contactus` a `/contacto` hay que **despublicar** la estándar.
- `header_overlay` en la página hace el header flotante: deja `padding-top` (~110 px escritorio, 84 px móvil) en la primera sección con `#wrapwrap.o_header_overlay`.
- `footer_visible = False` **no quita** el HTML del footer en Odoo 20. El footer de la plantilla sigue en el código aunque se oculte con CSS: limpia sus textos de ejemplo (correo y teléfono falsos) una vez desde el editor o elige una plantilla de footer sin datos de ejemplo.

## Editor visual
- El editor **une elementos contiguos iguales** al guardar: `<span class="ln"><span>A</span></span><span class="ln"><span>B</span></span>` termina como `AB`. Los titulares de varias líneas van en un solo span con `<br/>`.
- El editor puede escapar dos veces los `&` (`&amp;amp;`). Búscalos y corrígelos al releer.
- El cliente edita al mismo tiempo que tú: un guardado en el editor sobrescribe tu cambio por API (y viceversa). Relee `arch_db` y `write_date` antes de cada escritura y cambia solo lo pedido.
- En modo edición: `body.editor_enable` y `.o_editable`. El JS propio no corre ahí y no modifica `#wrap`, `header` ni `footer`.

## Header, footer y menús
- Opciones del header = vistas de opción del sitio que se activan o desactivan (`website.option_header_brand_logo`, `website.header_call_to_action`, `website.template_header_*`). Activarlas está permitido; reescribir su `arch` no.
- El logo del header viene de `website.logo`; el favicon de `website.favicon` (usa el monograma sobre el color de marca).
- Un botón de acción en el header = `website.menu` (registro) con `url` externa y `new_window=True`, con estilo de botón por CSS (`header a.nav-link[href^="https://wa.me"]`). Para llevarlo a la derecha: `#top_menu{flex:1 1 auto}` y `margin-left:auto` en su `li`.
- `custom_code_footer` se imprime justo después de `#wrapwrap` (dentro de `body`), en el servidor: el footer propio va ahí como HTML. `custom_code_head` va al final de `<head>`.
- Ocultar en páginas propias buscador, lista de deseos e "Inicia sesión" con `body:has(.owd-site) header …{display:none}` (la Tienda los conserva).

## Formularios
- `s_website_form` con `data-model_name="crm.lead"` crea oportunidades. Campo oculto `name` (requerido por el modelo). Campos del modelo: `contact_name`, `phone`, `email_from`, `description`. Los campos propios (`s_website_form_custom`) se agregan solos a la descripción.
- `data-success-mode="message"` + bloque `.s_website_form_end_message.d-none` después del `</form>`.
- `crm.lead` debe tener `website_form_access` (lo activa `website_crm`).
- Probar el envío solo en base de prueba o pedir al consultor que lo haga.

## Navegador y verificación
- Si el panel del navegador está oculto (`document.hidden`), las imágenes `loading="lazy"` no cargan: no es un error del sitio. Para medir, fuerza `img.loading='eager'` o usa `scripts/auditar_sitio.py`.
- Las vistas no publicadas solo se ven con sesión; sin sesión dan 404. Revisa antes de publicar con el consultor.
- En producción, agrega al carrito solo con permiso del consultor (como visitante, sin pagar) y cancela después la cotización que se crea (`sale.order` → `action_cancel`).

## SEO para buscadores e IAs
- **Dominio**: si `website.domain` tiene un dominio que todavía no apunta a Odoo, Odoo sirve `robots.txt` con `Disallow: /` en el subdominio `.odoo.com` y todos los canónicos apuntan al dominio muerto: el sitio no se indexa en ningún lado. Revísalo en el diagnóstico (`curl` al dominio y a `/robots.txt`). Solución: conectar el DNS (CNAME al subdominio de Odoo y agregar el dominio en odoo.com/my/databases) o quitar el dominio del sitio mientras tanto.
- `website.robots_txt` guarda las reglas propias; solo se publican cuando el dominio es indexable. Incluye permisos explícitos para rastreadores de IA (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended, Bingbot, meta-externalagent, CCBot) y bloquea `/web/`, `/my/`, carrito y pago.
- **llms.txt / llms-full.txt** en Odoo Online: crea un `ir.attachment` binario público con `url='/llms.txt'` y `mimetype='text/plain'`; Odoo lo sirve en esa ruta. Formato: título, resumen en cita, lista de páginas con enlaces absolutos y "Datos clave" (horario, zona, contacto, mínimos, alérgenos).
- **Datos estructurados**: Odoo ya publica `Organization`. Agrega en `custom_code_head` un `@graph` con `Restaurant`/`LocalBusiness` (horario, zona, teléfono, menú, fundador) y `WebSite`; el `FAQPage` va dentro de la vista de la página que tiene las preguntas, fuera de `#wrap`.
- `website.name` define el sufijo de los títulos ("… | Marca"); cambia ese campo y no el de la compañía (que sale en facturas). `website.social_default_image` es la imagen al compartir de páginas sin una propia (tienda, productos).
- SEO de productos: `website_meta_title`/`website_meta_description` en `product.template` (todos los idiomas).
- Las páginas genéricas de Odoo en inglés (`/contactus-thank-you`, `/your-task-has-been-submitted`) se despublican si el sitio no las usa.

## Reseñas
Nunca publiques reseñas inventadas como si fueran de clientes (engaño al consumidor, PROFECO). Deja la sección diseñada con la clase `.owd-pending` (oculta al público, visible con borde punteado en el editor) y textos "[Reseña real pendiente]" hasta tener reseñas reales.
