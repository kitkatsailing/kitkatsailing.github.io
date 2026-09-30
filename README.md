# Kitkat

La web pública del velero Kitkat, en español e inglés (según el idioma del navegador, con botón para cambiarlo),
por Instagram ([@kitkatsailing](https://www.instagram.com/kitkatsailing/)).

Publicada en https://kitkatsailing.github.io/

## Cómo se edita

| Archivo | Qué tiene |
|---|---|
| `src/pagina.html` | Textos, estructura y estilos |
| `src/plano.svg` | El plano vélico del cutter |
| `src/app.js` | Fotos y visor |
| `fotos.py` | Qué fotos usa la página y sus epígrafes |
| `build.py` | La URL y el usuario de Instagram |

    python fotos.py     # solo si cambia la selección de fotos (les borra el GPS y los metadatos)
    python build.py     # arma index.html

## Lo que nunca se publica

Matrícula, certificado, documentos, apellidos, datos de contacto personales, fotos con caras.
La exportación de Instagram (`instagram/`) queda fuera del repositorio.
