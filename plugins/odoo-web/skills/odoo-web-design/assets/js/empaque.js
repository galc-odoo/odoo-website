/* odoo_web_design · empaque: caja que se abre con el scroll y "diseña tu caja" · no corre en modo edición y no guarda cambios en el contenido. Configuración: window.OWD_CONFIG */
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

    var site=document.querySelector('.owd-site');if(!site||editing())return;

    /* La caja que se abre con el scroll */
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

    /* Diseña tu caja */
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
      if(go)go.addEventListener('click',function(e){e.preventDefault();var v=(inp.value||'').trim();var ta=site.querySelector((CFG.formulario||'#owd_form')+' textarea[name="description"]');if(ta){ta.value='Caja de invitados con el slogan: «'+(v||slTxt)+'»'+(H.classList.contains('owd-box-serif')?' (letra itálica)':'')+'. ';}var f=site.querySelector(CFG.formulario||'#owd_form');if(f){f.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});setTimeout(function(){var n=f.querySelector('input:not([type=hidden])');if(n)n.focus({preventScroll:true})},700)}});
    }
  });
})();
