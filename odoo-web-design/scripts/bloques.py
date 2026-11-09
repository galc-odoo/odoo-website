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
    return (f'<li><button type="button" class="owd-dip" data-tf="{tf}" data-desc="{escape(desc)}">'
            f'<span class="owd-sw" style="background:{color}"></span><strong>{nombre}</strong><em>{sub}</em></button></li>')


def grupo_preview(gid, titulo_pequeno, titulo, para, items, src, alt, caption, invertido=False):
    return (f'<div class="owd-dip-group{" owd-rev" if invertido else ""}" id="{gid}"><div>'
            f'<p class="owd-roman">{titulo_pequeno}</p><h3>{titulo}</h3><p class="owd-dip-for">{para}</p>'
            f'<ul class="owd-dip-list">{"".join(items)}</ul></div>'
            f'<figure class="owd-frame owd-dip-view owd-rv">{img(src, alt)}<figcaption><b>{titulo}</b>'
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
