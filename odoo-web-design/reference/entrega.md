# Validación y entrega

## Checklist antes de decir "listo"
Corre `python scripts/auditar_sitio.py <url> / /pagina1 /pagina2 …` y revisa en el navegador (escritorio 1440, tablet 1024, móvil 375):

- [ ] Cada página responde 200; las URLs viejas redirigen (301) a las nuevas.
- [ ] Un `h1` por página; titulares de varias líneas siguen separados (el editor no los unió).
- [ ] Sin scroll horizontal en móvil (`scrollWidth == innerWidth`); titulares y títulos de columnas caben.
- [ ] El header (flotante o no) no tapa el inicio del contenido; logo visible.
- [ ] Imágenes cargan, con alt, bien centradas en su recuadro; peso por página razonable (< 1.5 MB).
- [ ] Interacciones: transición entre páginas, vistas previas, botón flotante, menú móvil; consola sin errores; nada corre en modo edición.
- [ ] Formularios: estructura nativa, modelo correcto, mensaje de éxito. Envío real solo en prueba o por el consultor.
- [ ] SEO: título y descripción propios (no "Esta es la página principal…"), imagen al compartir por página.
- [ ] Sin restos de plantilla visibles ni en el código (correos `yourcompany.example.com`, teléfonos 555, "Lorem").
- [ ] Tienda (si aplica): carrito, dirección, facturación y pago legibles en escritorio y móvil; cotización de prueba cancelada.
- [ ] Sin `&amp;nbsp;` ni `&amp;amp;` visibles (el editor los escapa dos veces).
- [ ] Footer con datos reales, sin colores que no sean de la paleta.
- [ ] **Nota de migración**: ninguna plantilla estándar o heredada con `arch` modificado; las copias por sitio de plantillas estándar están archivadas.

## Bitácora de cambios (plantilla)
| Fecha | Qué | Modelo | ID | Dónde vive | Cómo revertir |
|---|---|---|---|---|---|
| AAAA-MM-DD | CSS y JS del sitio | website | 1 | custom_code_head / custom_code_footer | respaldo/…custom_code….json |
| | Página Nosotros | ir.ui.view + website.page | 4031 / 7 | vista propia | respaldo/…vista_4031….json |
| | Botón WhatsApp | website.menu | 13 | registro | borrar el menú |
| | Logo del header | ir.ui.view (opción) | 4025 | active=True | active=False |
| | Redirección | website.rewrite | 2 | registro | borrar |

## Guía corta para el cliente
1. **Editar textos e imágenes**: Sitio web → Editar → clic en el texto o la foto. Guardar.
2. **No editar los titulares grandes** desde el editor si tienen varias líneas; pídelo al consultor.
3. **Colores, tipografías y animaciones**: viven en Sitio web → Configuración → Código personalizado. Cambiarlos con cuidado (o pedirlo).
4. **Agregar productos a la tienda**: Ventas → Productos → nuevo, con foto (mín. 1000 px), precio, descripción y "Publicado".
5. **Mientras el consultor trabaja por API, no tengas la misma página abierta en el editor**: un guardado sobrescribe al otro.

## Pendientes típicos del cliente
Fotos finales en alta, foto del fundador o equipo, número de WhatsApp confirmado, redes sociales, dirección para el aviso de privacidad (revisión legal), llaves de pago, dominio.
