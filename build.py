"""Arma index.html (la web pública del Kitkat) a partir de src/.

    src/pagina.html  textos, estructura y estilos
    src/plano.svg    el plano vélico del cutter
    src/app.js       fotos y visor
    fotos/fotos.js   lo genera fotos.py

Uso:  python build.py      (si cambiaste la selección de fotos, antes: python fotos.py)
Publicar: git add -A && git commit && git push  (GitHub Pages sirve la rama main)
"""
import io, os, re, sys

URL = "https://reinamartin-ai.github.io/kitkat/"
IG_USER = "kitkatsailing"
ICONO_IG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
            '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/>'
            '<circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>')

AQUI = os.path.dirname(os.path.abspath(__file__))
def leer(*p): return io.open(os.path.join(AQUI, *p), encoding="utf-8").read()

html = leer("src", "pagina.html")
for marca, contenido in (("<!--SVG-->", leer("src", "plano.svg")),
                         ("<!--FOTOS-->", leer("fotos", "fotos.js")),
                         ("<!--APP-->", leer("src", "app.js"))):
    if html.count(marca) != 1: sys.exit("falta la marca " + marca)
    html = html.replace(marca, contenido)
for marca, valor in (("<!--IGDM-->", "https://ig.me/m/" + IG_USER),
                     ("<!--IG-->", "https://www.instagram.com/" + IG_USER + "/"),
                     ("<!--IGUSER-->", IG_USER),
                     ("<!--ICONO-->", ICONO_IG),
                     ("<!--URL-->", URL)):
    html = html.replace(marca, valor)
if re.search(r"<!--[A-Z]+-->", html): sys.exit("quedó una marca sin reemplazar")
io.open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8", newline="\n").write(html)

fotos = [f for f in os.listdir(os.path.join(AQUI, "fotos")) if f.endswith(".jpg")]
print("index.html: %d KB, %d fotos" % (len(html.encode("utf-8")) // 1024, len(fotos)))
