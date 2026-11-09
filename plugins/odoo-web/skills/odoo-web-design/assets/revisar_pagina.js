/* odoo_web_design · revisión de una página como la ve un visitante.
   Se ejecuta en el navegador (herramienta de JavaScript del navegador) en cada página y en cada ancho
   (1440, 1024, 375). No cambia nada de la página. Devuelve un objeto con los problemas encontrados.
   Uso: pega el archivo completo y al final llama  owdRevisar()  (o  await owdRevisar({esperar:1500}) ). */
async function owdRevisar(op) {
  op = op || {};
  var esperar = op.esperar == null ? 800 : op.esperar;
  /* fuerza la carga de imágenes diferidas (en un panel oculto no cargan solas) */
  document.querySelectorAll('img[loading="lazy"]').forEach(function (i) { i.loading = 'eager'; });
  await new Promise(function (r) { setTimeout(r, esperar); });
  await Promise.all([].slice.call(document.images).map(function (i) {
    return i.complete ? 0 : new Promise(function (r) { i.onload = i.onerror = r; setTimeout(r, 4000); });
  }));
  /* las animaciones de aparición dejan el texto semitransparente hasta que se hace scroll: se pausan
     solo durante la revisión para medir el estado final (se quita al terminar) */
  var pausa = document.createElement('style'); pausa.id = 'owd-revision';
  pausa.textContent = '*,*::before,*::after{animation:none!important;transition:none!important}';
  document.head.appendChild(pausa);
  try { return revisar(); } finally { pausa.remove(); }

  function revisar() {

  var W = innerWidth, P = { url: location.pathname + location.search, ancho: W, problemas: [], avisos: [], enlaces: [], botones: [] };
  function prob(tipo, el, detalle) { P.problemas.push({ tipo: tipo, donde: ruta(el), detalle: detalle }); }
  function aviso(tipo, el, detalle) { P.avisos.push({ tipo: tipo, donde: ruta(el), detalle: detalle }); }
  function ruta(el) {
    if (!el || !el.tagName) return '';
    var s = el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.classList.length ? '.' + [].slice.call(el.classList, 0, 2).join('.') : '');
    var t = (el.innerText || el.alt || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 50);
    return s + (t ? ' «' + t + '»' : '');
  }
  function visible(el) {
    var r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    if (!(r.width > 0 && r.height > 0) || cs.visibility === 'hidden' || cs.display === 'none') return false;
    for (var e = el; e && e.nodeType === 1; e = e.parentElement) if (+getComputedStyle(e).opacity < 0.05) return false;   /* capas cerradas (visor, menú) */
    return true;
  }
  var enEditor = document.body.classList.contains('editor_enable');
  if (enEditor) P.avisos.push({ tipo: 'editor', detalle: 'La página está en modo edición: revisa como visitante.' });

  /* 1 · desborde horizontal */
  var sw = document.documentElement.scrollWidth;
  if (sw > W + 1) {
    var anchos = [].slice.call(document.querySelectorAll('body *')).filter(function (e) {
      var r = e.getBoundingClientRect(); if (!(r.right > W + 1 && r.width > 0) || getComputedStyle(e).position === 'fixed') return false;
      for (var a = e.parentElement; a && a !== document.body; a = a.parentElement) { var o = getComputedStyle(a).overflowX; if (o === 'hidden' || o === 'clip' || o === 'auto' || o === 'scroll') return false; }
      return true;
    }).slice(0, 5);
    prob('desborde-horizontal', anchos[0], 'La página mide ' + sw + ' px en una pantalla de ' + W + ' px: ' + anchos.map(ruta).join(' | '));
  }

  /* 2 · imágenes */
  [].slice.call(document.images).forEach(function (i) {
    if (!visible(i) && !i.closest('.owd-slide')) return;
    if (!i.complete || i.naturalWidth === 0) prob('imagen-rota', i, i.currentSrc || i.src);
    if (i.alt == null || (i.getAttribute('alt') === null)) prob('imagen-sin-alt', i, i.src.slice(-60));
    var r = i.getBoundingClientRect(), dpr = devicePixelRatio || 1, cs = getComputedStyle(i);
    if (i.naturalWidth && r.width > 0 && i.naturalWidth < r.width * Math.min(dpr, 2) * 0.75 && r.width > 200)
      aviso('imagen-baja-resolucion', i, i.naturalWidth + ' px reales para ' + Math.round(r.width) + ' px en pantalla');
    if (i.naturalWidth && cs.objectFit === 'fill' && r.height > 0) {
      var d = (i.naturalWidth / i.naturalHeight) / (r.width / r.height);
      if (d > 1.08 || d < 0.92) prob('imagen-deformada', i, 'proporción real ' + (i.naturalWidth / i.naturalHeight).toFixed(2) + ' vs ' + (r.width / r.height).toFixed(2));
    }
  });

  /* 3 · contraste de texto (WCAG) */
  function rgba(c) {
    var m = c.match(/[\d.]+/g); if (!m) return [0, 0, 0, 0]; m = m.map(Number);
    if (/^color\(srgb/.test(c)) m = [m[0] * 255, m[1] * 255, m[2] * 255, m.length > 3 ? m[3] : 1];   /* color-mix() da color(srgb r g b / a) */
    return m.length === 3 ? m.concat([1]) : m;
  }
  function lum(c) { return c.slice(0, 3).map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }).reduce(function (a, v, k) { return a + v * [0.2126, 0.7152, 0.0722][k]; }, 0); }
  function sobre(fg, bg) { var a = fg[3]; return [0, 1, 2].map(function (k) { return fg[k] * a + bg[k] * (1 - a); }).concat([1]); }
  function fondo(el) {
    var capas = [];
    for (var e = el; e && e.nodeType === 1; e = e.parentElement) {
      var cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && !/gradient/.test(cs.backgroundImage)) return null;   /* texto sobre foto: revisar a ojo */
      var b = rgba(cs.backgroundColor); if (b[3] > 0) { capas.push(b); if (b[3] >= 1) break; }
    }
    var base = [255, 255, 255, 1];
    for (var k = capas.length - 1; k >= 0; k--) base = sobre(capas[k], base);
    return base;
  }
  var vistos = 0, malos = 0;
  [].slice.call(document.querySelectorAll('h1,h2,h3,h4,h5,h6,p,li,a,button,label,span,small,strong,em,td,th,dt,dd,summary,figcaption,blockquote,cite,input,textarea,select')).forEach(function (el) {
    if (malos > 25) return;
    var txt = [].slice.call(el.childNodes).filter(function (n) { return n.nodeType === 3 && n.textContent.trim(); }).length || /INPUT|TEXTAREA|SELECT/.test(el.tagName);
    if (!txt || !visible(el)) return;
    var cs = getComputedStyle(el), bg = fondo(el); if (!bg) return;
    var fg = sobre(rgba(cs.color), bg); fg[3] = 1;
    var op = 1; for (var e = el; e && e.nodeType === 1; e = e.parentElement) op *= +getComputedStyle(e).opacity;
    if (op < 1) fg = [0, 1, 2].map(function (k) { return fg[k] * op + bg[k] * (1 - op); });
    var L1 = lum(fg), L2 = lum(bg), cr = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    var px = parseFloat(cs.fontSize), grande = px >= 24 || (px >= 18.66 && +cs.fontWeight >= 700);
    vistos++;
    if (cr < (grande ? 3 : 4.5)) { malos++; prob('contraste', el, cr.toFixed(2) + ':1 (' + cs.color + ' sobre rgb(' + bg.slice(0, 3).map(Math.round) + '), ' + px + ' px)'); }
  });
  P.textos_revisados = vistos;

  /* 4 · enlaces y botones (inventario para el recorrido de clics) */
  var vistosHref = {};
  [].slice.call(document.querySelectorAll('a[href], a:not([href]), button, [role="button"], summary, input[type=submit]')).forEach(function (el) {
    if (!visible(el) || el.closest('.o_we_website_top_actions, .o_main_navbar')) return;
    var nombre = (el.innerText || el.getAttribute('aria-label') || el.title || (el.querySelector('img') || {}).alt || '').trim().replace(/\s+/g, ' ');
    if (!nombre) prob('control-sin-nombre', el, 'Botón o enlace sin texto ni aria-label (lectores de pantalla y SEO).');
    var r = el.getBoundingClientRect();
    if (W < 768 && (r.height < 32 || r.width < 32) && !el.closest('p,li,td') ) aviso('objetivo-pequeno', el, Math.round(r.width) + '×' + Math.round(r.height) + ' px (mínimo cómodo 44×44 en celular)');
    if (el.tagName === 'A') {
      var h = el.getAttribute('href');
      if (h == null || h === '' || h === '#' || /^javascript:/i.test(h)) {
        if (!el.matches('[data-bs-toggle], .s_website_form_send, [role="button"], .dropdown-toggle')) prob('enlace-vacio', el, 'href="' + (h || '') + '"');
        return;
      }
      if (/\{\{|example\.com|yourcompany|tu-?dominio/i.test(h)) prob('enlace-de-plantilla', el, h);
      var u; try { u = new URL(h, location.href); } catch (e) { prob('enlace-invalido', el, h); return; }
      var interno = u.origin === location.origin;
      if (!interno && el.target === '_blank' && !/noopener|noreferrer/.test(el.rel)) aviso('blank-sin-noopener', el, h);
      var clave = u.href.split('#')[0] + '|' + nombre;
      if (vistosHref[clave]) return; vistosHref[clave] = 1;
      P.enlaces.push({ texto: nombre.slice(0, 60), href: u.protocol.startsWith('http') ? (interno ? u.pathname + u.search + u.hash : u.href) : h, interno: interno, nueva: el.target === '_blank', zona: el.closest('header') ? 'header' : el.closest('footer, .owd-sitefooter') ? 'footer' : 'contenido' });
    } else {
      P.botones.push({ texto: nombre.slice(0, 60), tipo: el.tagName.toLowerCase() + (el.type ? ':' + el.type : ''), zona: el.closest('header') ? 'header' : el.closest('form') ? 'formulario' : 'contenido' });
    }
  });

  /* 5 · títulos, SEO básico y restos de plantilla */
  var h1 = [].slice.call(document.querySelectorAll('h1')).filter(visible);
  if (h1.length !== 1) prob('h1', h1[1] || document.body, h1.length + ' títulos h1 visibles (debe haber 1)');
  var md = document.querySelector('meta[name="description"]');
  if (!md || !md.content || /Esta es la|This is the|Lorem/i.test(md.content)) prob('meta-descripcion', document.head, md ? md.content.slice(0, 80) : 'falta');
  if (!document.title || /^(Home|Inicio)$/i.test(document.title.split('|')[0].trim())) aviso('titulo', document.head, document.title);
  var texto = document.body.innerText;
  [[/&nbsp;|&amp;|&lt;|&gt;/, 'entidad HTML visible (el editor la escapó dos veces)'], [/lorem ipsum/i, 'texto de relleno'],
   [/yourcompany|example\.com|info@tu|555[-\s]?555/i, 'dato de plantilla'], [/\{\{[^}]+\}\}/, 'marcador sin reemplazar'],
   [/\[Reseña real pendiente\]/, 'reseña pendiente visible al público']].forEach(function (x) {
    var m = texto.match(x[0]); if (m) prob('resto-de-plantilla', document.body, x[1] + ': «' + texto.substr(Math.max(0, m.index - 30), 80).replace(/\s+/g, ' ') + '»');
  });

  /* 6 · texto cortado y elementos tapados por el header fijo */
  [].slice.call(document.querySelectorAll('#wrap h1, #wrap h2, #wrap h3, #wrap p, #wrap .btn')).forEach(function (el) {
    if (!visible(el)) return;
    var cs = getComputedStyle(el);
    if ((cs.overflow === 'hidden' || cs.overflowX === 'hidden' || cs.textOverflow === 'ellipsis') && el.scrollWidth > el.clientWidth + 2) prob('texto-cortado', el, el.scrollWidth + ' > ' + el.clientWidth + ' px');
  });
  var hd = document.querySelector('header#top, header'), primero = document.querySelector('#wrap h1, #wrap section');
  if (hd && primero && scrollY === 0) {
    var hr = hd.getBoundingClientRect(), pr = primero.getBoundingClientRect(), hp = getComputedStyle(hd).position;
    if ((hp === 'fixed' || hp === 'absolute' || hp === 'sticky') && pr.top < hr.bottom - 4 && primero.tagName === 'H1') prob('header-tapa-contenido', primero, 'El header termina en ' + Math.round(hr.bottom) + ' px y el titular empieza en ' + Math.round(pr.top) + ' px');
  }

  /* 7 · formularios */
  P.formularios = [].slice.call(document.querySelectorAll('form')).filter(visible).map(function (f) {
    var campos = [].slice.call(f.querySelectorAll('input:not([type=hidden]),textarea,select'));
    campos.forEach(function (c) {
      var lab = c.id && document.querySelector('label[for="' + c.id + '"]');
      if (!lab && !c.getAttribute('aria-label') && !c.placeholder) prob('campo-sin-etiqueta', c, c.name);
    });
    return { id: f.id, modelo: f.getAttribute('data-model_name') || f.action, campos: campos.map(function (c) { return c.name + (c.required ? '*' : ''); }) };
  });

  P.resumen = P.problemas.length ? P.problemas.length + ' problema(s), ' + P.avisos.length + ' aviso(s)' : 'Sin problemas (' + P.avisos.length + ' aviso(s))';
  return P;
  }
}
