# odoo-website · skill `odoo-web-design`

Skill de Claude para hacer **el sitio web que sea** en Odoo 17–20, de la maqueta al recorrido como usuario:

1. Accesos de la base (API RPC) y diagnóstico en solo lectura.
2. Contexto del cliente.
3. Maqueta en PDF con todas las páginas y los efectos JS/CSS deseados.
4. Imágenes principales (solo referencia).
5. Vista previa en vivo en una ventana al lado, **sin tocar la base**.
6. Recomendaciones de transiciones, animaciones e interactivos según el giro.
7. Construcción en Odoo con aprobación: páginas con bloques nativos y **todo el CSS/JS en el código personalizado del sitio, nunca en vistas**.
8. Revisión del diseñador y ajustes.
9. Recorrido como usuario: da clic a todo frente al diseñador y entrega un reporte.

Guía con imágenes: [`docs/Guia - skill odoo-web-design.pdf`](docs/). Descripción del caso para tareas: `docs/Caso - skill odoo-web-design.html`.

## Instalar (diseñadores web, desde el chat de Claude, pestaña Code)

El repositorio es público: no necesitas cuenta de GitHub para usarlo. Pega en Claude:

```
Instala la skill de sitios web de Odoo del repositorio https://github.com/galc-odoo/odoo-website.
Hazlo tú, sin pedirme comandos: ejecuta claude plugin marketplace add galc-odoo/odoo-website
y claude plugin install odoo-web@odoo-website, y dime que reinicie la sesión.
```
Para proponer mejoras sí necesitas cuenta de GitHub y la invitación de galc-odoo (ver CONTRIBUTING.md).
Actualizar: `claude plugin marketplace update odoo-website`.

## Estructura

```
.claude-plugin/marketplace.json
plugins/odoo-web/
├── .claude-plugin/plugin.json
└── skills/odoo-web-design/
    ├── SKILL.md                    # los 9 pasos y las reglas (empieza aquí)
    ├── reference/                  # diseño, componentes, trampas de Odoo, CSS/JS, recorrido, entrega
    ├── assets/temas/*.json         # 5 direcciones de partida → marca.json del cliente
    ├── assets/css/, assets/js/     # módulos con variables del tema
    ├── assets/revisar_pagina.js    # revisión de cada página en el navegador
    ├── assets/footer.html
    └── scripts/                    # armar, vista_previa, bloques, escribir_pagina, push_code, recorrido…
```

## Probar cambios sin instalar

```bash
claude --plugin-dir plugins/odoo-web
```
Vista previa de todos los bloques con un tema:
```bash
python plugins/odoo-web/skills/odoo-web-design/scripts/vista_previa.py --marca plugins/odoo-web/skills/odoo-web-design/assets/temas/corporativo.json --salida /tmp/vista.html
```

## Seguridad

- La API key va en `ODOO_KEY_FILE` (archivo `chmod 600`) o `ODOO_KEY`; nunca en el repositorio, el chat ni entregables.
- Las carpetas de clientes (`clientes/`, `respaldo/`, `recorrido/`) no se suben: el `.gitignore` las excluye.

Cómo proponer mejoras: [CONTRIBUTING.md](CONTRIBUTING.md).
