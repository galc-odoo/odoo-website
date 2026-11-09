"""Bloques nativos de Odoo para armar páginas propias (editables con el editor visual).

Genera HTML/QWeb con la estructura de snippets (section.s_text_block, o_colored_level,
oe_structure) y las clases .owd-* del CSS base. Ejemplo:

    from bloques import *
    arch = pagina('website.nosotros', [
        encabezado('Nosotros', ['La historia', 'detrás de la marca.'], 'Texto corto de apoyo.'),
        seccion('Historia', f'<div class="container">...</div>'),
        seccion('Siguiente', f'<div class="container">{siguiente("/servicios", "Siguiente", "Servicios")}</div>'),
    ], marca_img='/web/image/123-abc/logo_b.png')

Reglas que estos helpers ya respetan:
- Titulares de varias líneas en UN solo <span class="owd-ln"> con <br/> (el editor une spans iguales).
- Imágenes con alt, class="img img-fluid" y loading="lazy".
- Formularios s_website_form con campo oculto `name` y mensaje de éxito nativo.
"""
from html import escape


def seccion(nombre, cuerpo, cls=''):
    return (f'<section class="s_text_block o_colored_level {cls}" data-snippet="s_text_block" '
            f'data-name="{escape(nombre)}">{cuerpo}</section>')


def img(src, alt, style=''):
    st = f' style="{style}"' if style else ''
    return f'<img src="{src}" alt="{escape(alt)}" class="img img-fluid" loading="lazy"{st}/>'


def titular(lineas, tag='h1', extra=''):
    return f'<{tag} class="owd-display"{extra}><span class="owd-ln"><span>{"<br/>".join(lineas)}</span></span></{tag}>'


def encabezado(eyebrow, lineas, lead):
    return seccion('Encabezado', f'<div class="container owd-head"><p class="owd-eyebrow">{eyebrow}</p>'
                   f'<div class="owd-head-row">{titular(lineas)}<div class="owd-vr"></div>'
                   f'<p class="owd-lead">{lead}</p></div></div>')


def boton(texto, href, nueva=False):
    t = ' target="_blank" rel="noopener"' if nueva else ''
    return f'<a class="btn owd-btn" href="{href}"{t}>{texto} →</a>'


def siguiente(href, eyebrow, etiqueta, extra=''):
    return (f'<a class="owd-next" href="{href}"{extra}><span><span class="owd-eyebrow">{eyebrow}</span>'
            f'<strong>{etiqueta}</strong></span><span class="owd-circle">→</span></a>')


def marco(src, alt, cls='', style=''):
    """Foto con borde interior. cls: owd-wide (21:9), owd-shot (4:5), owd-par (parallax), owd-rv (aparición)."""
    return f'<div class="owd-frame {cls}">{img(src, alt, style)}</div>'


def tarjeta(href, etiqueta, src, alt, numeral, nombre, desc, style=''):
    return (f'<a class="owd-card owd-rv" href="{href}"><span class="owd-frame"><span class="owd-tag">{etiqueta}</span>'
            f'{img(src, alt, style)}</span><span class="owd-card-meta"><span><span class="owd-roman">{numeral}</span>'
            f'<h3>{nombre}</h3><p>{desc}</p></span><span class="owd-circle">→</span></span></a>')


def item_preview(nombre, sub, desc, color, tf):
    """Elemento de lista que acerca la foto al pasar el cursor. tf = salida de centrar_zoom.py."""
    return (f'<li><button type="button" class="owd-preview-item" data-tf="{tf}" data-desc="{escape(desc)}">'
            f'<span class="owd-sw" style="background:{color}"></span><strong>{nombre}</strong><em>{sub}</em></button></li>')


def grupo_preview(gid, titulo_pequeno, titulo, para, items, src, alt, caption, invertido=False):
    return (f'<div class="owd-preview{" owd-rev" if invertido else ""}" id="{gid}"><div>'
            f'<p class="owd-roman">{titulo_pequeno}</p><h3>{titulo}</h3><p class="owd-preview-for">{para}</p>'
            f'<ul class="owd-preview-list">{"".join(items)}</ul></div>'
            f'<figure class="owd-frame owd-preview-view owd-rv">{img(src, alt)}<figcaption><b>{titulo}</b>'
            f'<span>{caption}</span></figcaption></figure></div>')



def equipo(personas, eyebrow='El equipo', titulo='Co-founders.'):
    """Cofundadores debajo del fundador. personas: [(nombre, rol, bio, src_foto, alt)]. Foto 4:5 con el mismo marco
    que la del fundador (src vacío = sin foto). Numerales i., ii., iii. en orden."""
    rom = ['i.', 'ii.', 'iii.', 'iv.', 'v.', 'vi.']
    cols = ''.join(
        f'<div class="owd-cofounder owd-rv">'
        + (f'<div class="owd-frame owd-founder owd-cofounder-photo">{img(src, alt)}</div>' if src else '')
        + f'<p class="owd-roman">{rom[i]}</p><h3>{n}</h3><p class="owd-role">{r}</p><p class="owd-bio">{b}</p></div>'
        for i, (n, r, b, src, alt) in enumerate(personas))
    return seccion('Equipo', f'<div class="container owd-section" style="padding-bottom:0"><p class="owd-eyebrow">{eyebrow}</p>'
                   f'<h2 class="owd-display" style="margin:22px 0 40px;font-size:clamp(40px,5vw,80px)">{titulo}</h2>'
                   f'<div class="owd-cofounders">{cols}</div></div>')



# ---------- Catálogo de bloques (ver reference/componentes.md) ----------
ROM = ['i.', 'ii.', 'iii.', 'iv.', 'v.', 'vi.', 'vii.', 'viii.']


def hero(eyebrow, lineas, lead, botones, src, alt, contador=('', ''), franja=None, fotos_extra=()):
    """Hero de inicio: titular de varias líneas, texto, botones y foto 4:5 (carga prioritaria).
    botones: [(texto, href)]. contador: dos textos cortos bajo la foto. franja: frases que corren abajo.
    fotos_extra: [(src, alt)] hasta 3 que se funden cada 6 s."""
    foto = (f'<img src="{src}" alt="{escape(alt)}" class="img img-fluid" loading="eager" fetchpriority="high"/>'
            + ''.join(f'<img src="{s}" alt="{escape(a)}" class="img img-fluid owd-slide" loading="lazy" decoding="async"/>' for s, a in fotos_extra))
    cont = (f'<div class="owd-counter"><span>{contador[0]}</span><i></i><span>{contador[1]}</span></div>' if any(contador) else '')
    fr = ''
    if franja:
        items = ''.join(f'<span>{t}</span><b>✦</b>' for t in franja) * 2
        fr = f'<div class="owd-marquee" aria-hidden="true"><div class="owd-marquee-track">{items}</div></div>'
    bts = ''.join(boton(t, h) for t, h in botones)
    return seccion('Hero', f'<div class="owd-hero"><div class="container"><div class="owd-hero-grid"><div>'
                   f'<p class="owd-eyebrow">{eyebrow}</p>{titular(lineas, extra=" style=\"margin-top:26px\"")}'
                   f'<div class="owd-hero-copy"><p class="owd-lead">{lead}</p><p class="owd-btns">{bts}</p></div></div>'
                   f'<div class="owd-frame owd-shot owd-par">{foto}{cont}</div></div></div>{fr}</div>')


def pilares(items):
    """3 o 4 ideas cortas en columnas con filetes. items: [(titulo, texto)]."""
    cols = ''.join(f'<div class="owd-pillar owd-rv"><p class="owd-roman">{ROM[i]}</p><h3>{t}</h3><p>{x}</p></div>'
                   for i, (t, x) in enumerate(items))
    return seccion('Pilares', f'<div class="container"><div class="owd-pillars">{cols}</div></div>')


def dividido(src, alt, eyebrow, titulo, lead, botones=()):
    """Foto 5:6 + texto con botón."""
    bts = ''.join(boton(t, h) for t, h in botones)
    return seccion(titulo, f'<div class="container owd-section"><div class="owd-split"><div class="owd-frame owd-rv">{img(src, alt)}</div>'
                   f'<div class="owd-split-txt owd-rv"><p class="owd-eyebrow">{eyebrow}</p><h2 class="owd-display">{titulo}</h2>'
                   f'<p class="owd-lead">{lead}</p><p>{bts}</p></div></div></div>')


def panoramica(src, alt, despues=''):
    """Foto 21:9 (4:3 en móvil) con parallax. despues: HTML extra (por ejemplo siguiente())."""
    return seccion('Foto', f'<div class="container">{marco(src, alt, "owd-wide owd-par owd-rv")}{despues}</div>')


def tarjetas(cards):
    """Rejilla de 3 tarjetas. cards: salidas de tarjeta()."""
    return seccion('Tarjetas', f'<div class="container owd-section"><div class="owd-cards">{"".join(cards)}</div></div>')


ICONOS = {  # trazos de 32×32 para pasos y tipos (stroke, sin relleno)
    'mensaje': '<path d="M6 26l1.6-5A11 11 0 1 1 11 24.5z"/>',
    'calendario': '<rect x="5" y="7" width="22" height="20"/><path d="M5 13h22M11 4v5M21 4v5"/>',
    'lista': '<path d="M11 9h15M11 16h15M11 23h15"/><circle cx="6" cy="9" r="1"/><circle cx="6" cy="16" r="1"/><circle cx="6" cy="23" r="1"/>',
    'entrega': '<path d="M3 9h16v13H3zM19 13h6l4 4v5h-10z"/><circle cx="9" cy="24" r="2.5"/><circle cx="24" cy="24" r="2.5"/>',
    'estrella': '<path d="M16 3l3 9.5 10 .3-8 6 3 9.7-8-5.8-8 5.8 3-9.7-8-6 10-.3z"/>',
    'personas': '<circle cx="11" cy="11" r="4"/><circle cx="22" cy="11" r="4"/><path d="M3 27c0-4.4 3.6-8 8-8s8 3.6 8 8M19 19c4.4 0 8 3.6 8 8"/>',
    'check': '<circle cx="16" cy="16" r="12"/><path d="M10 16.5l4 4 8-9"/>',
    'rayo': '<path d="M18 3L6 18h9l-1 11 12-16h-9z"/>',
}


def icono(nombre_o_trazo):
    t = ICONOS.get(nombre_o_trazo, nombre_o_trazo)
    return f'<svg class="owd-ico" viewBox="0 0 32 32" aria-hidden="true">{t}</svg>'


def pasos(items, nota='', botones=()):
    """Cómo funciona: 3–4 pasos numerados. items: [(icono, titulo, texto)] (icono = nombre de ICONOS o trazo SVG)."""
    li = ''.join(f'<li class="owd-rv">{icono(ic)}<span class="owd-k">{i + 1:02d}</span><h4>{t}</h4><p>{x}</p></li>'
                 for i, (ic, t, x) in enumerate(items))
    bts = ''.join(boton(t, h, nueva=h.startswith('http')) for t, h in botones)
    cta = f'<div class="owd-how-cta owd-rv"><p>{nota}</p><p>{bts}</p></div>' if (nota or bts) else ''
    return seccion('Pasos', f'<div class="container"><ol class="owd-how">{li}</ol>{cta}</div>')


def tipos(items, src='', alt=''):
    """Tipos de servicio en 4 columnas con ícono, opcionalmente bajo una foto panorámica. items: [(icono, titulo, texto)]."""
    foto = marco(src, alt, 'owd-wide owd-par owd-rv') if src else ''
    cols = ''.join(f'<div class="owd-rv">{icono(ic)}<h4>{t}</h4><p>{x}</p></div>' for ic, t, x in items)
    return seccion('Tipos', f'<div class="container">{foto}<div class="owd-types">{cols}</div></div>')


def bloque_formulario(eyebrow, titulo, lead, form_html):
    """Texto a la izquierda y formulario nativo (salida de formulario()) a la derecha."""
    return seccion('Formulario', f'<div class="container owd-section"><div class="owd-form-split"><div><p class="owd-eyebrow">{eyebrow}</p>'
                   f'<h2 class="owd-display">{titulo}</h2><p class="owd-lead">{lead}</p></div><div>{form_html}</div></div></div>')


def galeria(fotos, despues=''):
    """3 fotos 4:5 del mismo tamaño; clic = vista ampliada (módulo efectos). fotos: [(src, alt)]."""
    fr = ''.join(f'<div class="owd-frame owd-rv">{img(s, a)}</div>' for s, a in fotos)
    return seccion('Galería', f'<div class="container"><div class="owd-gallery">{fr}</div>{despues}</div>')


def fundador(src, alt, parrafos, nombre, rol):
    """Retrato 4:5 + historia en primera persona con capitular y firma."""
    ps = ''.join(f'<p{" class=\"owd-dropcap\"" if i == 0 else ""}>{p}</p>' for i, p in enumerate(parrafos))
    return seccion('Historia', f'<div class="container"><div class="owd-about"><div class="owd-frame owd-founder owd-rv">{img(src, alt)}</div>'
                   f'<div class="owd-about-txt owd-rv">{ps}<div><p class="owd-sig">{nombre}</p><p class="owd-sig-role">{escape(rol)}</p></div></div></div></div>')


def frase(texto, autor=''):
    """Cita grande de marca."""
    by = f'<p class="owd-pull-by">{autor}</p>' if autor else ''
    return seccion('Frase', f'<div class="container owd-section"><p class="owd-pull owd-rv">{texto}</p>{by}</div>')


def titulo_seccion(eyebrow, titulo):
    return f'<p class="owd-eyebrow">{eyebrow}</p><h2 class="owd-display" style="margin:22px 0 48px">{titulo}</h2>'


# --- módulo contenido ---
def horarios(eyebrow, titulo, items):
    """items: [(titulo, dato_grande, texto)] · 3 columnas."""
    cols = ''.join(f'<div class="owd-rv"><p class="owd-roman">{ROM[i]}</p><h4>{t}</h4><p class="owd-big">{g}</p><p>{x}</p></div>'
                   for i, (t, g, x) in enumerate(items))
    return seccion('Horarios', f'<div class="container owd-section">{titulo_seccion(eyebrow, titulo)}<div class="owd-hours">{cols}</div></div>')


def preguntas(eyebrow, titulo, faq):
    """Preguntas frecuentes con <details> (sin JS). faq: [(pregunta, respuesta)].
    Devuelve (html, json_ld): agrega json_ld a la vista FUERA de #wrap como <script type="application/ld+json">."""
    import json
    det = ''.join(f'<details><summary>{q}</summary><div><p>{r}</p></div></details>' for q, r in faq)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]}, ensure_ascii=False)
    return seccion('Preguntas', f'<div class="container owd-section">{titulo_seccion(eyebrow, titulo)}<div class="owd-faq">{det}</div></div>'), ld


def paquetes(eyebrow, titulo, items, minimo=''):
    """items: [(nombre, texto, [viñetas])]. minimo: texto como 'Pedido mínimo <strong>100</strong> piezas'."""
    cols = ''.join(f'<div class="owd-pack owd-rv"><p class="owd-roman">{ROM[i]}</p><h3>{n}</h3><p>{t}</p>'
                   f'<ul>{"".join(f"<li>{v}</li>" for v in vs)}</ul></div>' for i, (n, t, vs) in enumerate(items))
    mn = f'<p class="owd-min">{minimo}</p>' if minimo else ''
    return seccion('Paquetes', f'<div class="container owd-section">{titulo_seccion(eyebrow, titulo)}<div class="owd-packs">{cols}</div>{mn}</div>')


def notas(items):
    """Avisos cortos (alérgenos, garantía, cuidados). items: [(titulo, texto)]."""
    return seccion('Información', '<div class="container">' + ''.join(
        f'<div class="owd-note"{" style=\"margin-top:14px\"" if i else ""}><b>{t}</b><p>{x}</p></div>' for i, (t, x) in enumerate(items)) + '</div>')


def resenas(eyebrow, titulo, items=None):
    """Reseñas REALES: items [(texto, autor)]. Sin items deja la sección oculta (.owd-pending) con marcadores."""
    pend = items is None
    items = items or [('[Reseña real pendiente]', 'Nombre · Servicio')] * 3
    cols = ''.join(f'<div class="owd-review"><blockquote>{t}</blockquote><cite>{a}</cite></div>' for t, a in items)
    return seccion('Reseñas', f'<div class="container owd-section">{titulo_seccion(eyebrow, titulo)}<div class="owd-reviews">{cols}</div></div>',
                   cls='owd-pending' if pend else '')


def campo(fid, etiqueta, name, custom=True, requerido=True, tipo='text', ph='', textarea=False, col='col-lg-6'):
    cls = f'mb-3 {col} s_website_form_field' + (' s_website_form_custom' if custom else '') + \
          (' s_website_form_required' if requerido else '')
    if not custom and requerido:
        cls += ' s_website_form_model_required'
    mark = '<span class="s_website_form_mark"> *</span>' if requerido else ''
    req = ' required="1"' if requerido else ''
    dtype = 'text' if textarea else {'email': 'email', 'tel': 'tel'}.get(tipo, 'char')
    ctrl = (f'<textarea id="{fid}" class="form-control s_website_form_input" name="{name}" rows="4" placeholder="{ph}"{req}></textarea>'
            if textarea else
            f'<input id="{fid}" type="{tipo}" class="form-control s_website_form_input" name="{name}" placeholder="{ph}"{req}/>')
    return (f'<div class="{cls}" data-type="{dtype}" data-name="Field"><label class="s_website_form_label" for="{fid}">'
            f'<span class="s_website_form_label_content">{etiqueta}</span>{mark}</label>{ctrl}</div>')


def formulario(form_id, modelo, titulo_registro, campos, boton_txt, exito_titulo, exito_txt):
    """Formulario nativo. Para crm.lead los campos del modelo son contact_name, phone, email_from, description;
    los campos propios (custom=True) se agregan solos a la descripción de la oportunidad."""
    oculto = ('<div class="mb-3 col-12 s_website_form_field s_website_form_dnone" data-name="Field"><div class="row s_col_no_resize s_col_no_bgcolor">'
              '<label class="col-form-label col-sm-auto s_website_form_label"><span class="s_website_form_label_content"></span></label>'
              f'<div class="col-sm"><input type="hidden" class="form-control s_website_form_input" name="name" value="{escape(titulo_registro)}"/></div></div></div>')
    return (f'<section class="s_website_form o_colored_level" data-vcss="001" data-snippet="s_website_form" data-name="Formulario"><div class="container-fluid">'
            f'<form id="{form_id}" action="/website/form/" method="post" enctype="multipart/form-data" class="o_mark_required" data-mark="*" '
            f'data-model_name="{modelo}" data-success-mode="message" data-success-page="">'
            f'<div class="s_website_form_rows row s_col_no_bgcolor">{oculto}{"".join(campos)}'
            '<div class="mb-0 py-2 col-12 s_website_form_submit s_website_form_no_submit_label" data-name="Submit Button"><div class="s_website_form_label"></div>'
            f'<span id="s_website_form_result"></span><a href="#" role="button" class="btn owd-btn s_website_form_send">{boton_txt} →</a></div>'
            '</div></form>'
            '<div class="s_website_form_end_message d-none"><div class="oe_structure"><section class="s_text_block o_colored_level" data-snippet="s_text_block" data-name="Text">'
            f'<div class="container"><h3 class="owd-display" style="font-size:52px">{exito_titulo}</h3><p class="owd-mute">{exito_txt}</p></div></section></div></div>'
            '</div></section>')


def pagina(key, secciones, marca_img='', page_name=None, homepage=False):
    """Arch completo de una página propia. marca_img = la B/monograma para la transición entre páginas."""
    extra = ' pageName.f="homepage"' if homepage else ''
    wrap = f'<div id="wrap" class="oe_structure owd-site" data-owd-mark="{marca_img}">{"".join(secciones)}</div>'
    return f'<t t-name="{key}"><t t-call="website.layout"{extra}>{wrap}</t></t>'
