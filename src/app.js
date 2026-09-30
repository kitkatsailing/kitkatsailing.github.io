(function(){
  "use strict";

  function $(s, r){ return (r || document).querySelector(s); }
  function $$(s, r){ return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s){ return String(s == null ? "" : s).replace(/[&<>"]/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }

  /* ============================================================
     FOTOS Y VISOR
     ============================================================ */
  /* ============================================================
     IDIOMA (lo elige el script del <head>; el botón lo cambia y lo recuerda)
     ============================================================ */
  function lang(){ return document.documentElement.getAttribute("data-lang") === "en" ? "en" : "es"; }
  function epi(k){ return lang() === "en" ? (FOTOS[k].en || FOTOS[k].t) : FOTOS[k].t; }
  function textos(){
    $$("[data-foto-fig]").forEach(function(fig){
      var k = fig.getAttribute("data-foto-fig"), t = epi(k);
      $("img", fig).alt = t; $("figcaption", fig).textContent = t;
      fig.setAttribute("aria-label", (lang() === "en" ? "View larger: " : "Ver en grande: ") + t);
    });
    var hero = $("[data-foto]"); if(hero && FOTOS.portada) hero.alt = epi("portada");
    $(".tabs").setAttribute("aria-label", lang() === "en" ? "Sections" : "Secciones");
  }
  $("#langBtn").addEventListener("click", function(){
    var l = lang() === "en" ? "es" : "en";
    document.documentElement.setAttribute("data-lang", l); document.documentElement.lang = l;
    try{ localStorage.setItem("kitkat.lang", l); }catch(e){}
    textos(); pintarVisitas();
  });

  /* contador de visitas al pie (GoatCounter, código pacaca). Si no responde, no se muestra nada. */
  var visitas = null;
  function pintarVisitas(){
    var el = $("#visitas"); if(visitas == null || !el) return;
    var en = lang() === "en";
    el.textContent = visitas.toLocaleString(en ? "en-GB" : "es-UY") + (en ? (visitas === 1 ? " visit" : " visits") : (visitas === 1 ? " visita" : " visitas"));
    el.hidden = false;
  }
  if(location.protocol === "https:" && window.fetch){
    fetch("https://pacaca.goatcounter.com/counter/TOTAL.json").then(function(r){ return r.ok ? r.json() : null; }).then(function(j){
      var n = j && parseInt(String(j.count).replace(/\D/g, ""), 10);
      if(n >= 0){ visitas = n; pintarVisitas(); }
    }).catch(function(){});
  }

  function fsrc(k){ return FOTOS[k].src; }
  $$("[data-foto]").forEach(function(img){
    var k = img.getAttribute("data-foto"), f = FOTOS[k]; if(!f) return;
    img.src = fsrc(k); img.width = f.w; img.height = f.h;
  });
  $$("[data-foto-src]").forEach(function(s){ var k = s.getAttribute("data-foto-src"); if(FOTOS[k]) s.srcset = fsrc(k); else s.remove(); });
  $$("[data-foto-fig]").forEach(function(fig){
    var k = fig.getAttribute("data-foto-fig"), f = FOTOS[k]; if(!f){ fig.remove(); return; }
    fig.innerHTML = '<img loading="lazy" decoding="async" src="' + fsrc(k) + '" width="' + f.w + '" height="' + f.h + '" alt=""><figcaption></figcaption>';
    fig.tabIndex = 0; fig.setAttribute("role", "button");
  });
  textos();
  /* una galería sin ninguna foto (p. ej. el spinnaker, hasta tener la foto) no deja un hueco */
  $$("[data-galeria]").forEach(function(g){ if(!$("[data-foto-fig]", g)) g.remove(); });

  var lb = null, lbList = [], lbIx = 0, lbPrevFocus = null;
  function abrirVisor(lista, ix){
    lbList = lista; lbIx = ix; lbPrevFocus = document.activeElement;
    lb = document.createElement("div");
    var en = lang() === "en";
    lb.className = "lb"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true"); lb.setAttribute("aria-label", en ? "Photo" : "Foto en grande");
    lb.innerHTML = '<img alt=""><p></p><button class="x" type="button" aria-label="' + (en ? "Close" : "Cerrar") + '">&#10005;</button>' +
      (lista.length > 1 ? '<button class="prev" type="button" aria-label="' + (en ? "Previous" : "Anterior") + '">&lsaquo;</button><button class="next" type="button" aria-label="' + (en ? "Next" : "Siguiente") + '">&rsaquo;</button>' : '');
    document.body.appendChild(lb);
    pintarVisor();
    lb.addEventListener("click", function(e){
      if(e.target.closest(".x") || e.target === lb) cerrarVisor();
      else if(e.target.closest(".prev")) mover(-1);
      else if(e.target.closest(".next")) mover(1);
    });
    $(".x", lb).focus();
  }
  function pintarVisor(){ var k = lbList[lbIx]; $("img", lb).src = fsrc(k); $("img", lb).alt = epi(k); $("p", lb).textContent = epi(k); }
  function mover(d){ lbIx = (lbIx + d + lbList.length) % lbList.length; pintarVisor(); }
  function cerrarVisor(){ if(lb){ lb.remove(); lb = null; if(lbPrevFocus) lbPrevFocus.focus(); } }
  document.addEventListener("keydown", function(e){
    if(!lb) return;
    if(e.key === "Escape") cerrarVisor();
    if(e.key === "ArrowRight") mover(1);
    if(e.key === "ArrowLeft") mover(-1);
  });
  $$("[data-galeria]").forEach(function(g){
    var figs = $$("[data-foto-fig]", g), keys = figs.map(function(f){ return f.getAttribute("data-foto-fig"); });
    figs.forEach(function(f, i){
      f.addEventListener("click", function(){ abrirVisor(keys, i); });
      f.addEventListener("keydown", function(e){ if(e.key === "Enter" || e.key === " "){ e.preventDefault(); abrirVisor(keys, i); } });
    });
  });
})();
