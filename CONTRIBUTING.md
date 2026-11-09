# Cómo proponer mejoras

1. **Tu rama**: clona el repo y trabaja en una rama con tu usuario de GitHub (`git checkout -b <usuario>`). Antes de cada mejora: actualiza tu rama con lo último de `main`.
2. **Prueba** con `claude --plugin-dir plugins/odoo-web` en un sitio real o de prueba.
3. **Qué subir**
   - Trampas nuevas de Odoo → `reference/odoo-tecnico.md` (qué pasó y cómo evitarlo).
   - Bloques nuevos → función en `scripts/bloques.py`, estilos en el módulo que corresponda de `assets/css/` y una fila en `reference/componentes.md`.
   - Efectos e interactivos → `assets/css/` + `assets/js/` del mismo módulo, configurables con `OWD_CONFIG`, sin correr en modo edición.
   - Temas nuevos → `assets/temas/<nombre>.json` que pase la revisión de contraste de `armar.py`.
   - Cambios en el orden o las reglas → `SKILL.md` y, si aplica, `reference/recorrido.md` o `entrega.md`.
4. **Reglas del código**: prefijo `.owd-`; colores, fuentes, radios y espaciado solo con las variables del tema (ver `reference/js-css-patrones.md`); nada de colores fijos de un cliente. Antes del PR revisa la vista previa con un tema claro y uno oscuro, en 1440 y 375 px, y que `owdRevisar()` no marque problemas.
5. **Qué no subir**: API keys, contraseñas, URLs o nombres de bases de clientes, fotos de clientes, respaldos o datos personales.
6. **Pull Request** a `main` con qué cambia, por qué (qué problema real resolvió) y capturas si es visual. galc-odoo lo revisa; al aprobarse, llega a todos con `claude plugin marketplace update odoo-website`.
