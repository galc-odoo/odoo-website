/* odoo_web_design · interactivos: abierto ahora, franja, carrete, test · no corre en modo edición y no guarda cambios en el contenido. Configuración: window.OWD_CONFIG */
(function(){
  var H=document.documentElement;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches;
  var CFG=window.OWD_CONFIG||{};
  var WA='https://wa.me/'+(CFG.whatsapp||'');
  function editing(){return document.body.classList.contains('editor_enable')||!!document.querySelector('.o_editable, .o_we_website_top_actions')}
  function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn)}
  var restores=[];function onEdit(fn){restores.push(fn)}
  ready(function(){
    new MutationObserver(function(){if(editing()){restores.forEach(function(f){try{f()}catch(e){}});restores=[]}}).observe(document.body,{attributes:true,attributeFilter:['class']});

    /* Abierto ahora: OWD_CONFIG.horario = {zona:'America/Mexico_City', dias:[1,2,3,4,5], desde:'09:00', hasta:'18:00'} (0 = domingo) */
    var HR=CFG.horario;
    function hm(t){var p=String(t).split(':');return (+p[0])*60+(+(p[1]||0))}
    function openState(){
      try{var parts=new Intl.DateTimeFormat('en-US',{timeZone:HR.zona||'America/Mexico_City',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date());
        var g=function(t){return (parts.filter(function(x){return x.type===t})[0]||{}).value};var d=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(g('weekday'));var m=(+g('hour')%24)*60+(+g('minute'));
        var open=(HR.dias||[0,1,2,3,4,5,6]).indexOf(d)>=0&&m>=hm(HR.desde||'09:00')&&m<hm(HR.hasta||'18:00');
        H.classList.toggle('owd-open-now',open);H.classList.toggle('owd-closed',!open)}catch(e){}
    }
    if(HR){openState();setInterval(openState,60000)}

    var site=document.querySelector('.owd-site');if(!site||editing())return;

    /* Franja que reacciona al scroll */
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

    /* Carrete horizontal */
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

    /* Test "¿Qué <producto> eres?": el resultado siempre es uno de los productos principales, con su foto */
    var quiz=site.querySelector('[data-owd-quiz]');
    if(quiz&&(CFG.quiz||{}).preguntas){
      var original=quiz.innerHTML;onEdit(function(){quiz.innerHTML=original});
      /* OWD_CONFIG.quiz = {marca, ruta, preguntas:[{q, o:[[texto, clave]]}], resultados:{clave:{name, c, img, t}}} */
      var QZ=CFG.quiz||{};var BRAND=QZ.marca||'',SHARE_PATH=QZ.ruta||location.pathname;var Q=QZ.preguntas||[];var R=QZ.resultados||{};
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

  });
})();
