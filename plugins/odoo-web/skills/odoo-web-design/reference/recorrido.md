# Recorrido como usuario (paso 9)

Objetivo: comprobar, como lo haría un cliente real, que **todo hace sentido**: cada clic lleva a donde dice, los colores combinan en todos los bloques, todo se lee, nada se rompe en celular y la experiencia es agradable. El diseñador lo ve en la ventana del navegador al lado mientras das los clics.

Empieza solo cuando el diseñador dijo que el sitio está correcto (paso 8) y te dio permiso de entrar como usuario.

## 1 · Rastreo (automático, sin navegador)

```
python scripts/recorrido.py https://cliente.odoo.com --salida clientes/<cliente>/recorrido [--incluir-tienda]
```
Descubre las páginas (sitemap, menú, footer, enlaces internos), prueba todos los enlaces una vez y deja `inventario.json` y `reporte.md` con una casilla por página, por clic del contenido y por formulario. Los enlaces del header y del footer se reportan una sola vez para todo el sitio. Redes sociales que bloquean robots (403/429) se revisan a mano.

## 2 · Recorrido en el navegador (frente al diseñador)

Usa el navegador del entorno **sin sesión iniciada** (si el consultor tiene sesión en ese panel, abre una pestaña privada o pídele permiso para revisar desde el sitio publicado; nunca cierres su sesión). Ve contando en el chat qué haces en cada clic, en una línea.

Por cada página del inventario, en **1440 px** y después en **375 px** (celular):
1. Abre la página desde el menú (no escribiendo la URL), espera a que cargue y toma una captura.
2. Pega `assets/revisar_pagina.js` en la herramienta de JavaScript y corre `await owdRevisar()`. Revisa `problemas` (contraste, imagen rota o deformada, desborde horizontal, enlace vacío o de plantilla, h1, meta descripción, restos como `&amp;nbsp;` o `{{…}}`, header que tapa el titular, texto cortado, campo sin etiqueta) y `avisos` (fotos de baja resolución, botones pequeños en celular). La revisión pausa las animaciones solo mientras mide.
3. Lee la consola: sin errores.
4. Recorre la página de arriba abajo con scroll real: las animaciones de entrada terminan, nada parpadea ni se traba, los bloques seguidos no "brincan" de color (fondos y textos del mismo tema; tarjetas y bloques con el mismo estilo).
5. **Da clic a cada botón y enlace del contenido** de la lista del inventario: confirma que llega a la página o sección correcta, que el texto del botón describe a dónde lleva, que WhatsApp abre con el número y mensaje correctos en pestaña nueva, y regresa con **Atrás** (la transición no debe dejar la pantalla tapada).
6. Interactivos: pasa el cursor y da clic en cada uno (vista previa, galería ampliada con flechas y Esc, test completo hasta el resultado y sus botones, carrete, caja). En celular, con toques y deslizando.
7. Formularios: envíalo vacío para ver la validación y los mensajes; con datos de prueba **solo con permiso** (crea un registro real, por ejemplo una oportunidad en CRM, que después se archiva).

Una vez para todo el sitio:
- Menú completo en orden; logo lleva al inicio; menú del celular abre, navega y cierra.
- Footer: cada enlace, correo y teléfono.
- Una URL inventada (`/no-existe`) muestra la página 404 del sitio con salida al inicio.
- Tienda (si aplica, con permiso): catálogo → producto → agregar → carrito (cantidad, eliminar) → dirección con datos de prueba → facturación → pago **sin pagar**. Después cancela la cotización que se crea (`sale.order` → `action_cancel`) y avisa del contacto de prueba.
- Velocidad percibida: la primera pantalla aparece rápido; ninguna foto pesa más de ~400 KB (`auditar_sitio.py`).

## 3 · Corregir y volver a verificar

Anota cada hallazgo en la tabla de `reporte.md` (página, ancho, qué vio el usuario, causa, corrección). Lo que se arregla en el código personalizado o en una página propia se corrige con aprobación del diseñador si toca la base; lo que depende del cliente (pagos, dominio, textos legales, fotos) va a pendientes. Después de corregir, **repite** la revisión de esa página y marca "Verificado".

## 4 · Entrega del recorrido

Mensaje corto al diseñador con: páginas recorridas, clics probados, hallazgos encontrados y corregidos, pendientes del cliente, y el `reporte.md` con capturas de escritorio y celular de cada página.

## Qué cuenta como "experiencia agradable"

- Una sola acción principal clara en cada página y siempre a la vista en celular.
- Textos cortos, legibles (contraste ≥ 4.5:1) y con jerarquía: un titular, apoyo, botón.
- Animaciones que acompañan (aparecen al hacer scroll, botones que responden) y nunca estorban ni hacen esperar.
- Ninguna sorpresa: nada se abre solo, nada tapa el contenido, ningún clic lleva a una página vacía o en otro idioma.
