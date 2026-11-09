# Validación y entrega

## Antes de decir "listo"
La validación completa es el **recorrido como usuario** (`recorrido.md`, paso 9). Además confirma:
- [ ] **Nota de migración**: ninguna plantilla estándar o heredada con `arch` modificado; copias por sitio de plantillas estándar archivadas; todo el CSS y JS en el código personalizado.
- [ ] `odoo/marca.json`, `paginas.py`, `footer.html` y el `sitio.css`/`sitio.js` publicados están en la carpeta del cliente (son la fuente para cualquier cambio futuro).
- [ ] SEO: título y descripción propios por página, imagen al compartir, robots indexable con el dominio real, llms.txt.
- [ ] Datos de prueba limpios (cotizaciones canceladas, contactos y oportunidades de prueba archivados).

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
