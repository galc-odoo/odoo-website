/* odoo_web_design.<cliente> · interacciones del sitio. No corre en modo edición y no guarda cambios en el contenido. */
(function(){
  /* CONFIGURA */
  var PAGES=['/','/nosotros','/servicios','/contacto'];
  var WHATSAPP='5215500000000';
  var FLOAT_LABEL='Pedir';
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function editing(){return document.body.classList.contains('editor_enable')||!!document.querySelector('.o_editable, .o_we_website_top_actions')}
  function onReady(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn)}

  onReady(function(){
    var site=document.querySelector('.owd-site');
    var logoB=(site&&site.getAttribute('data-owd-mark'))||'';

    /* Transición entre páginas: velo + la B que se forma */
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

    /* Botón flotante de WhatsApp (fuera del contenido editable) */
    if(!editing()&&!document.querySelector('.owd-wa-float')){
      var wa=document.createElement('a');wa.className='owd-wa-float';wa.href='https://wa.me/'+WHATSAPP;wa.target='_blank';wa.rel='noopener';wa.setAttribute('aria-label','Pedir por WhatsApp');
      wa.innerHTML='<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M6 26l1.6-5A11 11 0 1 1 11 24.5z"/></svg><span>'+FLOAT_LABEL+'</span>';
      document.body.appendChild(wa);
      new MutationObserver(function(){if(editing())wa.remove()}).observe(document.body,{attributes:true,attributeFilter:['class']});
    }

    /* Vista previa de dips */
    site.querySelectorAll('.owd-dip-group').forEach(function(g){
      var img=g.querySelector('.owd-dip-view img'),cap=g.querySelector('.owd-dip-view figcaption'),btns=g.querySelectorAll('.owd-dip');
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

/* ===================== Bloque 2 · efecto wow ===================== */
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches;
  function editing(){return document.body.classList.contains('editor_enable')||!!document.querySelector('.o_editable, .o_we_website_top_actions')}
  function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn)}
  ready(function(){
    var site=document.querySelector('.owd-site');if(!site||editing())return;
    var added=[];function add(el){document.body.appendChild(el);added.push(el);return el}
    var touched=[];
    new MutationObserver(function(){if(editing()){added.forEach(function(el){el.remove()});touched.forEach(function(el){['tabindex','role','aria-label','style'].forEach(function(a){el.removeAttribute(a)})})}}).observe(document.body,{attributes:true,attributeFilter:['class']});

    /* Intro de primera visita: la B se forma en el centro (una vez por sesión) */
    var mark=site.getAttribute('data-owd-mark');var seen=true;try{seen=sessionStorage.getItem('owd-intro')==='1';sessionStorage.setItem('owd-intro','1')}catch(e){}
    var fromNav=false;try{fromNav=document.querySelector('.owd-curtain.owd-full,.owd-curtain.owd-out')!==null}catch(e){}
    if(!seen&&!fromNav&&mark&&!reduce){
      var c=document.querySelector('.owd-curtain');
      if(!c){c=document.createElement('div');c.className='owd-curtain';c.setAttribute('aria-hidden','true');c.innerHTML='<div class="owd-mark"><img class="owd-ghost" alt="" src="'+mark+'"><img class="owd-ink" alt="" src="'+mark+'"><span class="owd-glow"></span></div>';add(c)}
      c.style.background=getComputedStyle(document.documentElement).getPropertyValue('--owd-ink')||'#000';c.className='owd-curtain owd-in';
      setTimeout(function(){c.className='owd-curtain owd-out';setTimeout(function(){c.className='owd-curtain';c.style.background=''},750)},1250);
    }

    /* Cursor de marca */
    if(fine&&!reduce){
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

/* ===================== Interactivos "no manches" ===================== */
(function(){
  var H=document.documentElement;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches;
  var WA='https://wa.me/'+(window.OWD_WHATSAPP||'5215500000000'); /* CONFIGURA */
  function editing(){return document.body.classList.contains('editor_enable')||!!document.querySelector('.o_editable, .o_we_website_top_actions')}
  function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn)}
  var restores=[];function onEdit(fn){restores.push(fn)}
  ready(function(){
    new MutationObserver(function(){if(editing()){restores.forEach(function(f){try{f()}catch(e){}});restores=[]}}).observe(document.body,{attributes:true,attributeFilter:['class']});

    /* 4 · Abierto ahora (hora de CDMX, lunes a domingo 8:00–16:00) */
    function openState(){
      try{var p=new Intl.DateTimeFormat('en-GB',{timeZone:'America/Mexico_City',hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date()).split(':');var m=(+p[0])*60+(+p[1]);var open=m>=480&&m<960;
        H.classList.toggle('owd-open-now',open);H.classList.toggle('owd-closed',!open)}catch(e){}
    }
    openState();setInterval(openState,60000);

    var site=document.querySelector('.owd-site');if(!site||editing())return;

    /* 7 · Franja que reacciona al scroll */
    var track=site.querySelector('.owd-marquee-track');
    if(track&&!reduce){
      H.classList.add('owd-mq-js');onEdit(function(){H.classList.remove('owd-mq-js');track.style.removeProperty('transform')});
      var x=0,dir=-1,lastY=scrollY,vel=0,half=0,vis=false,running=false;
      function measure(){half=track.scrollWidth/2}measure();addEventListener('resize',measure);
      addEventListener('scroll',function(){var y=scrollY,d=y-lastY;lastY=y;if(d)dir=d>0?-1:1;vel=Math.min(Math.abs(d),80)},{passive:true});
      function tick(){if(!vis||document.hidden||!H.classList.contains('owd-mq-js')){running=false;return}x+=dir*(0.6+vel*0.35);vel*=0.9;if(half){if(x<=-half)x+=half;if(x>0)x-=half}track.style.transform='translate3d('+x.toFixed(1)+'px,0,0)';requestAnimationFrame(tick)}
      function start(){if(!running){running=true;requestAnimationFrame(tick)}}
      new IntersectionObserver(function(es){vis=es[0].isIntersecting;if(vis)start()}).observe(track);
      document.addEventListener('visibilitychange',function(){if(!document.hidden&&vis)start()});
    }

    /* 2 · La caja que se abre con el scroll */
    var ub=site.querySelector('.owd-unbox');
    if(ub&&!reduce){
      H.classList.add('owd-unbox-js');onEdit(function(){H.classList.remove('owd-unbox-js');ub.classList.remove('owd-u1','owd-u2','owd-u3');ub.style.removeProperty('--owd-u')});
      var step=ub.querySelector('.owd-unbox-step'),stepTxt=step?step.textContent:'';onEdit(function(){if(step)step.textContent=stepTxt});
      var lastO=-1,lastS='',pending=false;
      function u(){pending=false;var bx=[].slice.call(ub.querySelectorAll('.owd-unbox-box')).filter(function(e){return e.offsetParent})[0]||ub;var r=bx.getBoundingClientRect();
        if(r.top>innerHeight*1.2||r.bottom<-innerHeight*.2)return;
        var o=Math.min(1,Math.max(0,(innerHeight*0.98-r.top)/(innerHeight*0.62)));o=Math.round(o*400)/400;
        if(o!==lastO){lastO=o;ub.style.setProperty('--owd-u',o);ub.classList.toggle('owd-u1',o>.05);ub.classList.toggle('owd-u2',o>.35);ub.classList.toggle('owd-u3',o>.65);
          var t=o<.05?'Cerrada':(o<.98?'Abriendo…':'Too good to behave');if(step&&t!==lastS){lastS=t;step.textContent=t}}}
      addEventListener('scroll',function(){if(!pending){pending=true;requestAnimationFrame(u)}},{passive:true});addEventListener('resize',u);u();
    }

    /* 5 · Carrete horizontal de Eventos */
    var reel=site.querySelector('.owd-reel');
    if(reel){
      var rt=reel.querySelector('.owd-reel-track'),rc=reel.querySelector('.owd-reel-count'),rcTxt=rc?rc.textContent:'';
      var mq=matchMedia('(max-width:991px),(prefers-reduced-motion:reduce)');
      onEdit(function(){reel.style.removeProperty('height');rt.style.removeProperty('transform');if(rc)rc.textContent=rcTxt});
      var extra=0,lastX=null,lastC='';
      function size(){if(mq.matches){reel.style.removeProperty('height');rt.style.removeProperty('transform');return}extra=Math.max(0,rt.scrollWidth-innerWidth+80);reel.style.height=(innerHeight+extra)+'px';pos()}
      function pos(){if(mq.matches)return;var r=reel.getBoundingClientRect();if(r.top>innerHeight||r.bottom<0)return;var total=r.height-innerHeight,p=Math.min(1,Math.max(0,-r.top/(total||1)));var xx=Math.round(-p*extra);
        if(xx!==lastX){lastX=xx;rt.style.transform='translate3d('+xx+'px,0,0)'}
        if(rc){var n=rt.children.length,i=Math.min(n,1+Math.round(p*(n-1)));var c=String(i).padStart(2,'0')+' / '+String(n).padStart(2,'0');if(c!==lastC){lastC=c;rc.textContent=c}}}
      var rp=false;
      addEventListener('scroll',function(){if(!rp){rp=true;requestAnimationFrame(function(){rp=false;pos()})}},{passive:true});addEventListener('resize',size);
      if(document.readyState==='complete')size();else addEventListener('load',size);size();
    }

    /* 3 · Test "¿Qué <producto> eres?": el resultado siempre es uno de los productos principales, con su foto */
    var quiz=site.querySelector('[data-owd-quiz]');
    if(quiz){
      var original=quiz.innerHTML;onEdit(function(){quiz.innerHTML=original});
      /* CONFIGURA: marca, ruta para compartir, preguntas (cada opción suma a un resultado) y resultados con foto */
      var BRAND='Marca',SHARE_PATH='/productos';
      var Q=[{q:'¿Tu energía hoy?',o:[['Fuego total','a'],['Elegante y segura','b'],['Siempre con un giro','c']]},
             {q:'¿Cómo te gusta el sabor?',o:[['Clásico','a'],['Fresco','b'],['Dulce','c']]},
             {q:'¿Tu plan perfecto?',o:[['Fiesta','a'],['Cita','b'],['Noche de pelis','c']]}];
      var R={a:{name:'Producto A',c:'#B5321C',img:'',t:'Directo y con carácter.'},
             b:{name:'Producto B',c:'#5E7A3A',img:'',t:'Elegante y seguro.'},
             c:{name:'Producto C',c:'#8B4A2B',img:'',t:'Siempre con un giro.'}};
      var ans=[];
      function bar(i){return '<div class="owd-quiz-bar">'+Q.map(function(_,k){return '<i class="'+(k<=i?'on':'')+'"></i>'}).join('')+'</div>'}
      function ask(i){quiz.innerHTML=bar(i)+'<p class="owd-roman">Pregunta '+(i+1)+' de '+Q.length+'</p><p class="owd-quiz-q">'+Q[i].q+'</p><div class="owd-quiz-opts">'+Q[i].o.map(function(o){return '<button type="button" data-v="'+o[1]+'">'+o[0]+'</button>'}).join('')+'</div>';
        quiz.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){ans.push(b.getAttribute('data-v'));if(ans.length<Q.length)ask(ans.length);else result()})});quiz.querySelector('button').focus({preventScroll:true})}
      function result(){var c={};ans.forEach(function(a){c[a]=(c[a]||0)+1});var k=Object.keys(c).sort(function(a,b){return c[b]-c[a]})[0];if(c[k]===1)k=ans[ans.length-1];var r=R[k];
        var msg='Hola '+BRAND+', hice el test: soy '+r.name+'. Quiero pedirla.';
        quiz.innerHTML='<div class="owd-quiz-res"><div class="owd-quiz-dot'+(r.img?' owd-quiz-photo':'')+'" style="background:'+r.c+'">'+(r.img?'<img alt="'+r.name+'" src="'+r.img+'">':'')+'</div><div><p class="owd-roman">Tu match '+BRAND+'</p><h3>Eres '+r.name+'</h3><p>'+r.t+'</p><div class="owd-quiz-acts"><a class="btn owd-btn" target="_blank" rel="noopener" href="'+WA+'?text='+encodeURIComponent(msg)+'">Pídela por WhatsApp →</a><button type="button" class="btn owd-btn" data-share>Compartir mi resultado</button><button type="button" class="btn owd-btn" data-again>Otra vez</button></div><p class="owd-quiz-msg" aria-live="polite"></p></div></div>';
        var share='Soy '+r.name+' en '+BRAND+'. ¿Tú cuál eres? '+location.origin+SHARE_PATH;
        quiz.querySelector('[data-share]').addEventListener('click',function(){var m=quiz.querySelector('.owd-quiz-msg');if(navigator.share){navigator.share({text:share}).catch(function(){})}else if(navigator.clipboard){navigator.clipboard.writeText(share).then(function(){m.textContent='Copiado. Pégalo en tus historias.'}).catch(function(){m.textContent=share})}else{m.textContent=share}});
        quiz.querySelector('[data-again]').addEventListener('click',function(){ans=[];ask(0)})}
      Object.keys(R).forEach(function(k){if(R[k].img){var im=new Image();im.src=R[k].img}});
      var start=quiz.querySelector('[data-owd-quiz-start]');if(start)start.addEventListener('click',function(){ans=[];ask(0)});
    }

    /* 1 · Diseña tu caja */
    var lab=site.querySelector('[data-owd-boxlab]');
    if(lab){
      var inp=lab.querySelector('input'),sl=lab.querySelector('.owd-box .owd-slogan'),slTxt=sl?sl.textContent:'',chips=lab.querySelectorAll('.owd-chips button'),scene=lab.querySelector('.owd-box-scene'),go=lab.querySelector('[data-owd-boxlab-go]');
      onEdit(function(){if(sl)sl.textContent=slTxt;H.classList.remove('owd-box-serif');boxEl&&boxEl.removeAttribute('style');chips.forEach(function(c){c.removeAttribute('aria-pressed')})});
      function upd(){var v=(inp.value||'').trim();sl.textContent=v||slTxt}
      inp.addEventListener('input',upd);
      chips.forEach(function(c){c.addEventListener('click',function(){chips.forEach(function(o){o.setAttribute('aria-pressed',String(o===c))});H.classList.toggle('owd-box-serif',c.getAttribute('data-style')==='serif')})});
      var by=-24,bx=0,drag=null;
      var boxEl=lab.querySelector('.owd-box');function setR(){boxEl.style.setProperty('--by',by+'deg');boxEl.style.setProperty('--bx',bx+'deg')}setR();
      scene.addEventListener('pointerdown',function(e){drag={x:e.clientX,y:e.clientY,by:by,bx:bx};scene.setPointerCapture(e.pointerId)});
      scene.addEventListener('pointermove',function(e){if(!drag)return;by=drag.by+(e.clientX-drag.x)*.4;bx=Math.max(-30,Math.min(30,drag.bx-(e.clientY-drag.y)*.25));setR()});
      scene.addEventListener('pointerup',function(){drag=null});scene.addEventListener('pointercancel',function(){drag=null});
      if(go)go.addEventListener('click',function(e){e.preventDefault();var v=(inp.value||'').trim();var ta=site.querySelector('#owd_eventos_form textarea[name="description"]');if(ta){ta.value='Caja de invitados con el slogan: «'+(v||slTxt)+'»'+(H.classList.contains('owd-box-serif')?' (letra itálica)':'')+'. ';}var f=site.querySelector('#owd_eventos_form');if(f){f.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});setTimeout(function(){var n=f.querySelector('input:not([type=hidden])');if(n)n.focus({preventScroll:true})},700)}});
    }
  });
})();
