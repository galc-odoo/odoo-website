# Cómo colaborar

1. **Clona** y crea tu branch con tu nombre y el tema:
   ```bash
   git clone https://github.com/galc-odoo/odoo-website.git
   cd odoo-website
   git checkout -b <tu-nombre>/<tema>      # ej. ana/tienda-clara
   ```
2. **Instala tu versión** en Claude (ver README) y úsala con un cliente o una base de prueba.
3. **Qué sí subir**
   - Trampas nuevas de Odoo → `reference/odoo-tecnico.md` (qué pasó y cómo evitarlo).
   - Patrones de CSS/JS probados → `assets/base.css` / `assets/base.js`, **genéricos**: prefijo `.owd-`, colores con los tokens de `:root` (`--owd-ink`, `--owd-light`, `--owd-accent`…), nada del cliente.
   - Lo que un cliente pidió o rechazó y vale para todos → `reference/diseno.md` o `js-css-patrones.md` ("Detalles que el cliente notó").
   - Scripts nuevos → `scripts/`, credenciales siempre por variables de entorno.
4. **Qué no subir**: API keys, URLs o nombres de bases de clientes, fotos de clientes, respaldos, cotizaciones o datos personales.
5. **Antes del PR**
   - Probado en escritorio (1440 px) y móvil (375 px), consola sin errores y nada corre en modo edición.
   - Si cambias un flujo, actualiza `SKILL.md` y el checklist de `reference/entrega.md`.
   - Mensaje de commit en español y en presente: "Agrega estilo de carrito para tiendas claras".
6. **Pull Request** hacia `main` con: qué cambia, por qué (qué problema real resolvió) y capturas si es visual.

`main` siempre debe tener una versión instalable del skill.
