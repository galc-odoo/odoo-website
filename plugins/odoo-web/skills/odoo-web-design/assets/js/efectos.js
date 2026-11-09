/* odoo_web_design · efectos: intro, cursor (opcional), botones magnéticos, galería ampliada · no corre en modo edición y no guarda cambios en el contenido. Configuración: window.OWD_CONFIG */
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches;
  var CFG=window.OWD_CONFIG||{};
  function editing(){return document.body.classList.contains('editor_enable')||!!document.querySelector('.o_editable, .o_we_website_top_actions')}
  function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn)}
  ready(function(){
    var site=document.querySelector('.owd-site');if(!site||editing())return;
    var added=[];function add(el){document.body.appendChild(el);added.push(el);return el}
    var touched=[];
    new MutationObserver(function(){if(editing()){added.forEach(function(el){el.remove()});touched.forEach(function(el){['tabindex','role','aria-label','style'].forEach(function(a){el.removeAttribute(a)})})}}).observe(document.body,{attributes:true,attributeFilter:['class']});

    /* Intro de primera visita: el monograma se forma en el centro (una vez por sesión) */
    var mark=site.getAttribute('data-owd-mark');var seen=true;try{seen=sessionStorage.getItem('owd-intro')==='1';sessionStorage.setItem('owd-intro','1')}catch(e){}
    var fromNav=false;try{fromNav=document.querySelector('.owd-curtain.owd-full,.owd-curtain.owd-out')!==null}catch(e){}
    if(!seen&&!fromNav&&mark&&!reduce){
      var c=document.querySelector('.owd-curtain');
      if(!c){c=document.createElement('div');c.className='owd-curtain';c.setAttribute('aria-hidden','true');c.innerHTML='<div class="owd-mark"><img class="owd-ghost" alt="" src="'+mark+'"><img class="owd-ink" alt="" src="'+mark+'"><span class="owd-glow"></span></div>';add(c)}
      c.style.background=getComputedStyle(document.documentElement).getPropertyValue('--owd-bg')||'#000';c.className='owd-curtain owd-in';
      setTimeout(function(){c.className='owd-curtain owd-out';setTimeout(function(){c.className='owd-curtain';c.style.background=''},750)},1250);
    }

    /* Cursor de marca */
    if(CFG.cursor&&fine&&!reduce){
      var cur=add(document.createElement('div'));cur.className='owd-cursor';cur.setAttribute('aria-hidden','true');cur.innerHTML='<span>Ver</span>';
      var tx=0,ty=0,cx=0,cy=0,raf=null;
      function loop(){cx+=(tx-cx)*.2;cy+=(ty-cy)*.2;cur.style.transform='translate('+cx+'px,'+cy+'px)';raf=(Math.abs(tx-cx)+Math.abs(ty-cy)>.2)?requestAnimationFrame(loop):null}
      document.addEventListener('mousemove',function(e){tx=e.clientX;ty=e.clientY;cur.classList.add('is-on');if(!raf)raf=requestAnimationFrame(loop);
        var t=e.target.closest?e.target:null;var view=t&&t.closest('.owd-card,.owd-gallery .owd-frame');var link=t&&t.closest('a,button,summary,label,.btn');
        cur.classList.toggle('is-view',!!view);cur.classList.toggle('is-link',!view&&!!link)},{passive:true});
      document.addEventListener('mouseleave',function(){cur.classList.remove('is-on')});
    }

    /* Botones magnéticos */
    if(fine&&!reduce){
      site.querySelectorAll('.btn.owd-btn,.owd-circle').forEach(function(b){
        b.addEventListener('mousemove',function(e){if(editing())return;var r=b.getBoundingClientRect(),x=e.clientX-r.left-r.width/2,y=e.clientY-r.top-r.height/2;b.style.transition='transform .25s';b.style.transform='translate('+(x*.18)+'px,'+(y*.28)+'px)'});
        b.addEventListener('mouseleave',function(){b.style.transition='transform .6s cubic-bezier(.16,.84,.24,1)';b.style.transform='';setTimeout(function(){b.removeAttribute('style')},650)});
      });
    }

    /* Vista ampliada de la galería */
    var imgs=[].slice.call(site.querySelectorAll('.owd-gallery img, .owd-reel img'));
    if(imgs.length){
      var lb=add(document.createElement('div'));lb.className='owd-lightbox';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','Galería');
      lb.innerHTML='<img alt=""><button type="button" class="owd-lb-close" aria-label="Cerrar">×</button><button type="button" class="owd-lb-prev" aria-label="Anterior">‹</button><button type="button" class="owd-lb-next" aria-label="Siguiente">›</button><div class="owd-lb-count"></div>';
      var big=lb.querySelector('img'),cnt=lb.querySelector('.owd-lb-count'),i=0,last=null;
      function show(n){i=(n+imgs.length)%imgs.length;var s=imgs[i];big.src=s.currentSrc||s.src;big.alt=s.alt||'';cnt.textContent=(i+1)+' / '+imgs.length}
      function open(n){last=document.activeElement;show(n);lb.classList.add('is-open');document.documentElement.style.overflow='hidden';lb.querySelector('.owd-lb-close').focus()}
      function close(){lb.classList.remove('is-open');document.documentElement.style.overflow='';if(last)last.focus()}
      imgs.forEach(function(im,n){var f=im.closest('.owd-frame');touched.push(f);f.setAttribute('tabindex','0');f.setAttribute('role','button');f.setAttribute('aria-label','Ver foto: '+(im.alt||''));
        f.addEventListener('click',function(){if(!editing())open(n)});f.addEventListener('keydown',function(e){if((e.key==='Enter'||e.key===' ')&&!editing()){e.preventDefault();open(n)}})});
      lb.querySelector('.owd-lb-close').addEventListener('click',close);
      lb.querySelector('.owd-lb-prev').addEventListener('click',function(){show(i-1)});
      lb.querySelector('.owd-lb-next').addEventListener('click',function(){show(i+1)});
      lb.addEventListener('click',function(e){if(e.target===lb)close()});
      document.addEventListener('keydown',function(e){if(!lb.classList.contains('is-open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
      var sx=null;lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});lb.addEventListener('touchend',function(e){if(sx===null)return;var d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>40)show(i+(d<0?1:-1));sx=null});
    }
  });
})();
