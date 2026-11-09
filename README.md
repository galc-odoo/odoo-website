# odoo-website · skill `odoo-web-design`

Skill de Claude para diseñar y construir sitios web *high end* en **Odoo 17–20** por API: maqueta, páginas con bloques nativos editables, CSS y JavaScript en el **código personalizado del sitio** (sin tocar plantillas, resistente a migraciones), estética de Tienda, carrito y pago, SEO para buscadores e IAs, optimización de fotos y auditoría final.

## Contenido

```
odoo-web-design/
├── SKILL.md                 # Flujo de 6 fases y reglas (empieza aquí)
├── reference/
│   ├── diseno.md            # Dirección visual, tokens, maqueta, fotos
│   ├── odoo-tecnico.md      # Trampas de Odoo: traducciones, copias por sitio, editor, SEO, carrito
│   ├── js-css-patrones.md   # CSS/JS base, interactivos, rendimiento, tienda oscura
│   └── entrega.md           # Checklist, bitácora y guía para el cliente
├── scripts/                 # odoo_rpc, push_code, bloques, escribir_pagina, optimizar_imagenes, centrar_zoom, auditar_sitio
└── assets/                  # base.css, base.js, footer.html (prefijo .owd-, paleta en tokens)
docs/
└── Guia rapida - instalar skill odoo-web-design.pdf
```

## Instalar

**Claude (app de escritorio o claude.ai):** comprime la carpeta `odoo-web-design/` en un `.zip` y súbelo en *Ajustes → Capacidades → Skills → Subir skill*. Pasos con imágenes en `docs/`.

```bash
cd odoo-website && zip -r odoo-web-design.zip odoo-web-design -x "*.DS_Store"
```

**Claude Code:** copia la carpeta a tus skills personales.

```bash
cp -R odoo-web-design ~/.claude/skills/
```

Después pide algo como: *"Usa odoo-web-design para rediseñar el sitio de <cliente>"*.

## Regla principal

| Qué | Dónde vive |
|---|---|
| Estilos | `website.custom_code_head` (`<style id="odoo_web_design_<cliente>">`) |
| JavaScript y footer propio | `website.custom_code_footer` |
| Páginas nuevas | `website.page` + vista propia con bloques nativos (única vista que se escribe por API) |
| Páginas estándar (Tienda, Carrito, Pago, Contáctanos) | Solo CSS con su clase de `body` |
| Plantillas estándar o heredadas | **Nunca** se editan por API |

## Seguridad

- La API key de Odoo va en variables de entorno (`ODOO_KEY`) o en un archivo con `chmod 600` (`ODOO_KEY_FILE`). **Nunca** en el repositorio, en el chat ni en entregables.
- No subas carpetas de clientes (`clientes/`, `respaldo/`): tienen datos y respaldos de bases reales. El `.gitignore` ya las excluye.
- Nada se escribe en Odoo sin el "sí" del consultor en cada fase.

## Cómo colaborar (consultores)

Ver [CONTRIBUTING.md](CONTRIBUTING.md). Resumen: cada consultor trabaja en **su propia branch**, prueba el cambio en un sitio real o de prueba y abre un Pull Request hacia `main`.
