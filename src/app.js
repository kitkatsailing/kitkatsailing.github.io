(function(){
  "use strict";

  function $(s, r){ return (r || document).querySelector(s); }
  function $$(s, r){ return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s){ return String(s == null ? "" : s).replace(/[&<>"]/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }

  /* ============================================================
     FOTOS Y VISOR
     ============================================================ */
  function fsrc(k){ return FOTOS[k].src; }
  $$("[data-foto]").forEach(function(img){
    var k = img.getAttribute("data-foto"), f = FOTOS[k]; if(!f) return;
    img.src = fsrc(k); img.width = f.w; img.height = f.h;
  });
  $$("[data-foto-src]").forEach(function(s){ var k = s.getAttribute("data-foto-src"); if(FOTOS[k]) s.srcset = fsrc(k); else s.remove(); });
  $$("[data-foto-fig]").forEach(function(fig){
    var k = fig.getAttribute("data-foto-fig"), f = FOTOS[k]; if(!f){ fig.remove(); return; }
    fig.innerHTML = '<img loading="lazy" decoding="async" src="' + fsrc(k) + '" width="' + f.w + '" height="' + f.h + '" alt="' + esc(f.t) + '"><figcaption>' + esc(f.t) + '</figcaption>';
    fig.tabIndex = 0; fig.setAttribute("role", "button"); fig.setAttribute("aria-label", "Ver en grande: " + f.t);
  });
  /* una galería sin ninguna foto (p. ej. el spinnaker, hasta tener la foto) no deja un hueco */
  $$("[data-galeria]").forEach(function(g){ if(!$("[data-foto-fig]", g)) g.remove(); });

  var lb = null, lbList = [], lbIx = 0, lbPrevFocus = null;
  function abrirVisor(lista, ix){
    lbList = lista; lbIx = ix; lbPrevFocus = document.activeElement;
    lb = document.createElement("div");
    lb.className = "lb"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true"); lb.setAttribute("aria-label", "Foto en grande");
    lb.innerHTML = '<img alt=""><p></p><button class="x" type="button" aria-label="Cerrar">&#10005;</button>' +
      (lista.length > 1 ? '<button class="prev" type="button" aria-label="Anterior">&lsaquo;</button><button class="next" type="button" aria-label="Siguiente">&rsaquo;</button>' : '');
    document.body.appendChild(lb);
    pintarVisor();
    lb.addEventListener("click", function(e){
      if(e.target.closest(".x") || e.target === lb) cerrarVisor();
      else if(e.target.closest(".prev")) mover(-1);
      else if(e.target.closest(".next")) mover(1);
    });
    $(".x", lb).focus();
  }
  function pintarVisor(){ var k = lbList[lbIx]; $("img", lb).src = fsrc(k); $("img", lb).alt = FOTOS[k].t; $("p", lb).textContent = FOTOS[k].t; }
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
