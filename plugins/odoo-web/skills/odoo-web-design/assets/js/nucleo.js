/* odoo_web_design · núcleo: transición, botón flotante, vista previa, inclinación · no corre en modo edición y no guarda cambios en el contenido. Configuración: window.OWD_CONFIG */
(function(){
  var CFG=window.OWD_CONFIG||{};
  var PAGES=CFG.paginas||['/'];
  var WHATSAPP=CFG.whatsapp||'';
  var FLOAT_LABEL=CFG.botonFlotante||'Escríbenos';
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function editing(){return document.body.classList.contains('editor_enable')||!!document.querySelector('.o_editable, .o_we_website_top_actions')}
  function onReady(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn)}

  onReady(function(){
    var site=document.querySelector('.owd-site');
    var logoB=(site&&site.getAttribute('data-owd-mark'))||'';

    /* Transición entre páginas: velo + el monograma que se forma */
    var cur=null;
    function curtain(){
      if(cur)return cur;
      cur=document.createElement('div');cur.className='owd-curtain';cur.setAttribute('aria-hidden','true');
      cur.innerHTML='<div class="owd-mark"><img class="owd-ghost" alt="" src="'+logoB+'"><img class="owd-ink" alt="" src="'+logoB+'"><span class="owd-glow"></span></div>';
      document.body.appendChild(cur);return cur;
    }
    var flag=false;try{flag=sessionStorage.getItem('owd-tr')==='1';sessionStorage.removeItem('owd-tr')}catch(e){}
    if(flag&&logoB&&!reduce&&!editing()){var c=curtain();c.className='owd-curtain owd-full';requestAnimationFrame(function(){requestAnimationFrame(function(){c.className='owd-curtain owd-out';setTimeout(function(){c.className='owd-curtain'},750)})})}
    window.addEventListener('pageshow',function(e){if(e.persisted&&cur)cur.className='owd-curtain'});
    document.addEventListener('click',function(e){
      if('onpagereveal' in window)return;
      if(!site||!logoB||reduce||editing()||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
      var a=e.target.closest&&e.target.closest('a[href]');if(!a||a.target==='_blank'||a.hasAttribute('download'))return;
      var u;try{u=new URL(a.getAttribute('href'),location.href)}catch(err){return}
      if(u.origin!==location.origin)return;
      var path=decodeURI(u.pathname).replace(/\/$/,'')||'/';
      if(PAGES.indexOf(path)<0||(path===((decodeURI(location.pathname).replace(/\/$/,''))||'/')&&u.hash))return;
      e.preventDefault();
      try{sessionStorage.setItem('owd-tr','1')}catch(err){}
      var c=curtain();c.className='owd-curtain';void c.offsetWidth;c.className='owd-curtain owd-in';
      setTimeout(function(){location.href=u.href},1050);
    },true);

    if(!site)return;

    /* Botón flotante en celular (fuera del contenido editable): WhatsApp si hay número, si no OWD_CONFIG.botonFlotanteUrl; sin ninguno no aparece */
    var FLOAT_URL=WHATSAPP?'https://wa.me/'+WHATSAPP:(CFG.botonFlotanteUrl||'');
    if(FLOAT_URL&&!editing()&&!document.querySelector('.owd-wa-float')){
      var wa=document.createElement('a');wa.className='owd-wa-float';wa.href=FLOAT_URL;if(/^https?:/.test(FLOAT_URL)){wa.target='_blank';wa.rel='noopener'}wa.setAttribute('aria-label',FLOAT_LABEL);
      wa.innerHTML='<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M6 26l1.6-5A11 11 0 1 1 11 24.5z"/></svg><span>'+FLOAT_LABEL+'</span>';
      document.body.appendChild(wa);
      new MutationObserver(function(){if(editing())wa.remove()}).observe(document.body,{attributes:true,attributeFilter:['class']});
    }

    /* Lista con vista previa: la foto se acerca al elemento elegido */
    site.querySelectorAll('.owd-preview').forEach(function(g){
      var img=g.querySelector('.owd-preview-view img'),cap=g.querySelector('.owd-preview-view figcaption'),btns=g.querySelectorAll('.owd-preview-item');
      if(!img||!cap)return;
      var base=cap.innerHTML;
      function on(b){
        if(editing())return;
        btns.forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});
        var tf=b.getAttribute('data-tf');
        if(tf){img.style.objectPosition='50% 50%';img.style.transformOrigin='50% 50%';img.style.transform=tf}
        else{img.style.objectPosition=b.getAttribute('data-pos')||'50% 50%';img.style.transformOrigin=b.getAttribute('data-org')||'50% 50%';img.style.transform='scale(2.1)'}
        var n=b.querySelector('strong'),s=b.querySelector('em');
        cap.innerHTML='<b>'+(n?n.textContent:'')+' · '+(s?s.textContent:'')+'</b><span>'+(b.getAttribute('data-desc')||'')+'</span>';
      }
      btns.forEach(function(b){['mouseenter','focus','click'].forEach(function(ev){b.addEventListener(ev,function(){on(b)})})});
      g.addEventListener('mouseleave',function(){if(editing())return});
      /* Al entrar al modo edición se restaura el estado original */
      new MutationObserver(function(){if(editing()){img.removeAttribute('style');cap.innerHTML=base;btns.forEach(function(x){x.removeAttribute('aria-pressed')})}}).observe(document.body,{attributes:true,attributeFilter:['class']});
    });

    /* Inclinación sutil de tarjetas */
    if(!reduce&&matchMedia('(hover:hover)').matches){
      site.querySelectorAll('.owd-card').forEach(function(c){
        var f=c.querySelector('.owd-frame');if(!f)return;
        c.addEventListener('mousemove',function(e){if(editing()){f.style.transform='';return}var r=f.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;f.style.transition='transform .7s cubic-bezier(.16,.84,.24,1)';f.style.transform='perspective(1000px) rotateY('+(x*4)+'deg) rotateX('+(-y*4)+'deg)'});
        c.addEventListener('mouseleave',function(){f.style.transform='';f.style.transition=''});
      });
    }
  });
})();
