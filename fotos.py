"""Prepara las fotos de la web pública a partir de la carpeta General (y, si está, de la
exportación de Instagram en instagram/).

Reduce cada foto, la gira según su orientación y la guarda como JPEG SIN metadatos:
no queda fecha, modelo de teléfono ni ubicación GPS. Escribe fotos/fotos.js con
los epígrafes y las medidas, que usa la página.
Una foto cuyo archivo no existe se saltea (y la página no muestra su lugar).
Para cambiar la selección, editar FOTOS y volver a correr:  python fotos.py
"""
import json, os
from PIL import Image, ImageOps
import pillow_heif
pillow_heif.register_heif_opener()

AQUI = os.path.dirname(os.path.abspath(__file__))
GENERAL = os.path.join(os.path.expanduser("~"), "Desktop", "Motor Velero kitkat", "General",
                       "Fotos-20260918T172928Z-1-001")
IG = os.path.join(AQUI, "instagram")          # la exportación de Instagram (no se sube)
F = "Fotos-20260918T173034Z-1-001/Fotos/"
RB = F + "20230113-14 Riachuelo  - Buceo/"
P1 = F + "Fotos primera dueña/"               # fotos de Sylvia (Peter y Sylvia)
P2 = F + "Fotos dueños anteriores/"           # fotos que compartieron Sean y Debie
SALIDA = os.path.join(AQUI, "fotos")

# clave: (archivo relativo a GENERAL, o "ig:<ruta dentro de instagram/>", lado mayor en px, epígrafe)
# Solo fotos del barco: ninguna con caras de la familia ni de terceros.
FOTOS = {
 # portada
 "portada":      (RB + "IMG_7166.HEIC", 2200, "Fondeado, enero de 2023"),
 "portada-alta": (RB + "20230114_135210.jpg", 1500, "Fondeado, enero de 2023"),
 # navegando
 "nav-mayor":    (RB + "a97b4cb1-2f9b-4a94-a78b-9411b93a9d5c.JPG", 1500, "La mayor roja al atardecer"),
 "nav-yankee":   (RB + "520bd900-14a1-4800-8593-a214731f9069.JPG", 1500, "Yankee y mayor, rumbo al sol"),
 "nav-velas":    (RB + "IMG_7156.HEIC", 1500, "Desde el pie del palo"),
 "nav-orejas":   (RB + "20230114_051948.jpg", 1500, "A orejas de burro, al amanecer"),
 "nav-botavara": (RB + "20230114_054432.jpg", 1500, "La botavara y el sol que sale"),
 "nav-ocaso":    (RB + "98674839-55f9-4de7-aa8d-9dcdabdf62b8.JPG", 1500, "Cae el sol sobre el Río de la Plata"),
 "nav-costado":  (RB + "Copia de IMG_0264.HEIC", 1500, "Por la banda, a la puesta"),
 "nav-casa":     (RB + "Copia de IMG_0269.HEIC", 1500, "La casilla con la última luz"),
 "nav-cubierta": (RB + "1bd28468-d2fb-4e3e-8808-11fab378a7a7.JPG", 1500, "Cubierta al atardecer"),
 "nav-proa":     (RB + "20230114_134804.jpg", 1600, "La proa y la ciudad"),
 # el spinnaker asimétrico con el dibujo de Sylvia: sale de la exportación de Instagram
 # (post del 17/03/2023). Completar la ruta cuando esté la carpeta instagram/.
 "spi":          ("ig:", 1600, "El spinnaker asimétrico, con el dibujo de Sylvia"),
 # a bordo
 "salon":        ("Fotos/salon 2.jpeg", 1400, "El salón de cubierta"),
 "navegacion":   (F + "Varios/PHOTO-2022-10-25-11-12-05(2).jpg", 1400, "Mesa de navegación y tablero"),
 "cocina":       (F + "Varios/PHOTO-2022-10-25-11-12-05(4).jpg", 1400, "La cocina"),
 "dinette":      ("Fotos/salon 4.jpg", 1400, "La dinette"),
 "camarote":     (F + "Varios/PHOTO-2022-10-25-11-40-30.jpg", 1400, "Camarote de proa"),
 "cubierta":     (F + "Inspección inicial/WhatsApp Image 2022-12-22 at 14.34.38 (2).jpeg", 1400, "La cubierta hacia proa"),
 # en seco
 "grua":         (F + "230120 fondo/IMG_7281.HEIC", 1600, "En la grúa, enero de 2023"),
 "nombre":       (F + "Varios/0582D4E6-EB70-4175-877E-FF6D3D25247A.JPG", 1600, "El nombre en la proa"),
 "varada":       (F + "Varios/82E645A1-3EB5-4C93-AC04-A0E3F9573B8F.JPG", 1600, "En el varadero"),
 # historia: Peter y Sylvia
 "h-casa":       (P1 + "42EA1298-1A93-488D-BD53-F80DA17E6938.JPG", 1300, "Con grúa, entre las casas: la salida del fondo donde Peter lo terminó"),
 "h-amarra":     (P1 + "346927CF-B9CB-41F0-BC07-CA276AC42638.JPG", 1300, "En su amarra, en Inglaterra"),
 "h-blanco":     (P1 + "68A2F908-F8E2-40EE-AF72-DA279518A3E0.JPG", 1100, "Navegando con Peter y Sylvia"),
 "h-rojas":      (P1 + "BBAC99F0-5480-4A93-97B5-B062F5873630.JPG", 1100, "Las velas rojas, ya entonces"),
 # historia: Sean y Debie
 "h-marea":      (P2 + "IMG_9518.HEIC", 1200, "En seco con la bajante, en la época de Sean y Debie"),
 "h-nieve":      (P2 + "IMG_9519.HEIC", 1100, "Kitkat bajo la nieve"),
 "h-montana":    (P2 + "IMG_9520.HEIC", 1200, "Con Sean y Debie, entre montañas"),
 "h-puerto":     (P2 + "IMG_9521.HEIC", 1200, "Con Sean y Debie, en puerto"),
 # historia: Sebastián (Colonia, mayo de 2020; foto de @barullo.sailing)
 "h-colonia":    (F + "200520 Colonia/WhatsApp Image 2023-01-23 at 16.50.46.jpeg", 1300, "En Colonia, mayo de 2020. Foto: @barullo.sailing"),
}

os.makedirs(SALIDA, exist_ok=True)
for f in os.listdir(SALIDA):                      # sin restos de selecciones anteriores
    if f.endswith(".jpg"): os.remove(os.path.join(SALIDA, f))
meta, faltan, total = {}, [], 0
for clave, (rel, lado, epi) in FOTOS.items():
    ruta = os.path.join(IG, rel[3:]) if rel.startswith("ig:") else os.path.join(GENERAL, rel)
    if not os.path.isfile(ruta):
        faltan.append(clave); continue
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
    im.thumbnail((lado, lado), Image.LANCZOS)
    destino = os.path.join(SALIDA, clave + ".jpg")
    im.save(destino, "JPEG", quality=80, optimize=True, progressive=True)   # sin exif: sin GPS
    total += os.path.getsize(destino)
    meta[clave] = {"src": "fotos/" + clave + ".jpg", "w": im.width, "h": im.height, "t": epi}

with open(os.path.join(SALIDA, "fotos.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("/* generado por fotos.py */\nvar FOTOS = " + json.dumps(meta, ensure_ascii=False, indent=1) + ";\n")
print("%d fotos, %.1f MB" % (len(meta), total / 1e6))
if faltan: print("sin archivo (no se muestran):", ", ".join(faltan))
