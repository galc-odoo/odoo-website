# Catálogo de bloques y efectos

Todo usa las variables del tema (`marca.json`), así que se ve bien en claro y en oscuro. Elige por lo que el negocio necesita contar, no por llenar. Para verlos todos juntos con un tema: `python scripts/vista_previa.py --marca assets/temas/<tema>.json`.

## Bloques de página (`scripts/bloques.py`, módulo `nucleo` salvo que se indique)

| Bloque | Función | Cuándo usarlo |
|---|---|---|
| Hero de inicio | `hero()` | Primera pantalla: titular de 2–3 líneas, texto, 1–2 botones, foto 4:5 con contador y franja opcional; hasta 3 fotos que se funden. |
| Encabezado de página | `encabezado()` | Inicio de cada página interior. |
| Pilares | `pilares()` | 3–4 valores o diferenciadores en columnas. |
| Bloque dividido | `dividido()` | Foto + texto + botón: presentar un producto, servicio o idea. |
| Panorámica | `panoramica()` | Foto 21:9 con parallax entre secciones. |
| Tarjetas | `tarjetas()` + `tarjeta()` | 3 productos, servicios o casos, con acercamiento e inclinación al pasar el cursor. |
| Lista con vista previa | `grupo_preview()` + `item_preview()` | Variantes en una sola foto (sabores, acabados, modelos): la foto se acerca al elegido. `centrar_zoom.py` calcula el acercamiento. |
| Pasos | `pasos()` | Cómo comprar, cotizar o trabajar con ellos (3–4 pasos con ícono). |
| Tipos de servicio | `tipos()` | 4 modalidades (eventos, industrias, planes) con ícono. |
| Formulario | `formulario()` + `campo()` + `bloque_formulario()` | Contacto, cotización, eventos: formulario nativo de Odoo hacia `crm.lead` u otro modelo. |
| Galería | `galeria()` | 3 fotos iguales; con `efectos`, clic para ampliar. |
| Fundador | `fundador()` | Historia en primera persona con retrato y firma. |
| Equipo | `equipo()` (módulo `contenido`) | Cofundadores o equipo con foto en el mismo formato. |
| Frase | `frase()` | Cita grande de marca. |
| Siguiente página | `siguiente()` | Cierre de cada página hacia la siguiente. |
| Horarios | `horarios()` (`contenido`) | Horario, entregas, zona. |
| Preguntas frecuentes | `preguntas()` (`contenido`) | Dudas reales; devuelve también el JSON-LD `FAQPage`. |
| Paquetes | `paquetes()` (`contenido`) | Formatos o planes con viñetas y mínimo. |
| Notas | `notas()` (`contenido`) | Alérgenos, garantías, cuidados. |
| Reseñas | `resenas()` (`contenido`) | Solo reales; sin ellas queda oculta con marcadores. |
| Aviso legal | clases `.owd-legal` | Aviso de privacidad por secciones. |

## Efectos (módulo `efectos`)

- **Transición entre páginas** (núcleo): velo y el monograma que se forma; `OWD_CONFIG.paginas` lista las rutas. En navegadores con View Transitions se usa la transición nativa.
- **Intro de primera visita**: el monograma al abrir el sitio, una vez por sesión.
- **Botones magnéticos**: siguen un poco al cursor.
- **Galería ampliada**: visor con flechas, Esc y deslizar.
- **Menú móvil a pantalla completa** con opciones grandes que entran escalonadas.
- **Cursor de marca** (desactivado por defecto: `OWD_CONFIG.cursor = true` solo si el diseñador lo pide).
- En todos los bloques: aparición al hacer scroll y parallax solo con CSS, botones que se rellenan desde abajo.

## Interactivos (módulo `interactivos`)

| Interactivo | Marca en la página | Configuración | Ideal para |
|---|---|---|---|
| Abierto ahora | `.owd-open` con `.owd-open-yes` / `.owd-open-no` | `OWD_CONFIG.horario = {zona, dias, desde, hasta}` | Restaurantes, tiendas, consultorios. |
| Franja que reacciona | `.owd-marquee` (del hero) | — | Marcas con frases cortas. |
| Carrete horizontal | `.owd-reel` > `.owd-reel-stage` > `.owd-reel-track` | — | Portafolio, eventos, proyectos. |
| Test "¿Qué … eres?" | `[data-owd-quiz]` + botón `[data-owd-quiz-start]` | `OWD_CONFIG.quiz = {marca, ruta, preguntas, resultados}` | Productos con personalidad; el resultado es siempre un producto principal con su foto y botón de acción. |
| Lista explora | `.owd-explore` | — | Índices de categorías. |

## Empaque (módulo `empaque`, solo si el producto llega en caja)

- **Caja que se abre con el scroll** (`.owd-unbox`): a partir de una foto cenital del empaque abierto, base y tapa en capas.
- **Diseña tu caja** (`[data-owd-boxlab]`): caja 3D con la frase del cliente, giro con arrastre y botón que pasa la frase al formulario (`OWD_CONFIG.formulario`).
Toma las proporciones de fotos reales del empaque.

## Ideas por giro (para el paso 6)

| Giro | Ideas que sorprenden |
|---|---|
| Restaurante, café, comida | Abierto ahora, lista con vista previa por sabor, test de producto, caja que se abre, pedido por WhatsApp con mensaje armado. |
| Servicios profesionales, B2B | Pasos del servicio, tipos con ícono, carrete de casos, formulario de cotización con campos según servicio, cifras que cuentan al aparecer. |
| Moda, joyería, diseño | Hero con fotos que se funden, galería ampliada, tarjetas con inclinación, transición con monograma. |
| Eventos, turismo | Carrete horizontal, paquetes, diseña tu caja o tu invitación, formulario con fecha y número de invitados. |
| Tecnología | Hero con titular grande, pasos, preguntas frecuentes, comparador de planes (a la medida). |

Lo que no está en el catálogo se diseña a la medida siguiendo `js-css-patrones.md` y, si sirve para otros clientes, se agrega aquí y a los módulos con un Pull Request.
