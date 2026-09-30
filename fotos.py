"""Prepara las fotos de la web pública a partir de la carpeta General y de las fotos del
Instagram (bajadas a instagram/, que no se sube).

Reduce cada foto, la gira según su orientación y la guarda como JPEG SIN metadatos:
no queda fecha, modelo de teléfono ni ubicación GPS. Escribe fotos/fotos.js con
los epígrafes (español e inglés) y las medidas, que usa la página.
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
IG = os.path.join(AQUI, "instagram")          # fotos de @kitkatsailing: <código del post>_<nº>.jpg
F = "Fotos-20260918T173034Z-1-001/Fotos/"
RB = F + "20230113-14 Riachuelo  - Buceo/"
P1 = F + "Fotos primera dueña/"               # fotos de Sylvia (Peter y Sylvia)
P2 = F + "Fotos dueños anteriores/"           # fotos que compartieron Sean y Debie
SALIDA = os.path.join(AQUI, "fotos")

# clave: (archivo relativo a GENERAL, o "ig:<archivo en instagram/>", lado mayor en px, epígrafe, caption)
# Las fotos del Instagram se pueden usar tal cual, aunque tengan caras (lo dijo el usuario).
# Nunca las capturas de mapas: muestran el nombre del usuario.
FOTOS = {
 # portada
 "portada":      ("ig:DMVXnfgx8rM_02.jpg", 1440, "Kitkat con el spinnaker de Sylvia, en la regata del 119 aniversario del YCU", "Kitkat flying Sylvia's spinnaker at the YCU 119th anniversary regatta"),
 # el spinnaker de Sylvia
 "spi-dibujo":   ("ig:Cp5OLJQrk9Y_02.jpg", 1440, "El personaje que pintó Sylvia", "The figure Sylvia painted"),
 "spi-piso":     ("ig:Cp5OLJQrk9Y_01.jpg", 1440, "La sorpresa, desplegada en el varadero", "The surprise, spread out in the boatyard"),
 # navegando
 "nav-mayor":    (RB + "a97b4cb1-2f9b-4a94-a78b-9411b93a9d5c.JPG", 1500, "La mayor roja al atardecer", "The red mainsail at sunset"),
 "nav-yankee":   (RB + "520bd900-14a1-4800-8593-a214731f9069.JPG", 1500, "Yankee y mayor, rumbo al sol", "Yankee and main, heading into the sun"),
 "nav-piria":    ("ig:DD4iM_4RuZk_01.jpg", 1440, "Llegando a Piriápolis", "Arriving at Piriápolis"),
 "nav-faro":     ("ig:DD4iM_4RuZk_02.jpg", 1440, "En conserva, rumbo a Piriápolis", "Sailing in company towards Piriápolis"),
 "nav-ocaso":    (RB + "98674839-55f9-4de7-aa8d-9dcdabdf62b8.JPG", 1500, "Cae el sol sobre el Río de la Plata", "Sunset over the Río de la Plata"),
 "nav-regata":   ("ig:C9s53SlP2Q7_02.jpg", 1440, "Regata en Montevideo", "Racing off Montevideo"),
 "nav-velas":    (RB + "IMG_7156.HEIC", 1500, "Desde el pie del palo", "From the foot of the mast"),
 "nav-fondeo":   ("ig:DEyVEleRVsH_01.jpg", 1440, "Fondeado en Piriápolis", "At anchor in Piriápolis"),
 "nav-noche":    ("ig:C1cX9Dfr__d_04.jpg", 1440, "De noche, en el puerto", "In harbour at night"),
 "nav-chapuzon": ("ig:C1cX9Dfr__d_07.jpg", 1440, "Un chapuzón desde la borda", "A swim off the side"),
 "nav-botavara": (RB + "20230114_054432.jpg", 1500, "La botavara y el sol que sale", "The boom and the rising sun"),
 "nav-bsas":     ("ig:DASAbwxusMI_02.jpg", 1440, "En Buenos Aires", "In Buenos Aires"),
 # a bordo
 "salon":        ("ig:Cy8l99wLD-M_02.jpg", 1440, "El salón, con el tapizado nuevo", "The saloon, with its new upholstery"),
 "navegacion":   (F + "Varios/PHOTO-2022-10-25-11-12-05(2).jpg", 1400, "Mesa de navegación y tablero", "Chart table and switchboard"),
 "cocina":       (F + "Varios/PHOTO-2022-10-25-11-12-05(4).jpg", 1400, "La cocina", "The galley"),
 "timon":        ("ig:C3f8NHpLSun_07.jpg", 1440, "En la rueda", "At the wheel"),
 "camarote":     (F + "Varios/PHOTO-2022-10-25-11-40-30.jpg", 1400, "Camarote de proa", "Forward cabin"),
 # en seco y la puesta a punto
 "grua":         ("ig:CnrgbG2uI1Y_01.jpg", 1440, "A seco en el YCU, enero de 2023", "Hauled out at the YCU, January 2023"),
 "obra":         ("ig:CpYVO8POcGY_02.jpg", 1440, "Pintando la obra muerta", "Painting the topsides"),
 "vuelve":       ("ig:Cw0QkH6LUf3_04.jpg", 1440, "De vuelta al agua, setiembre de 2023", "Back in the water, September 2023"),
 "nombre":       (F + "Varios/0582D4E6-EB70-4175-877E-FF6D3D25247A.JPG", 1600, "El nombre en la proa", "The name on the bow"),
 # historia: Peter y Sylvia
 "h-casa":       (P1 + "42EA1298-1A93-488D-BD53-F80DA17E6938.JPG", 1300, "Con grúa, entre las casas: la salida del fondo donde Peter lo terminó", "Craned out between the houses, from the garden where Peter finished her"),
 "h-amarra":     (P1 + "346927CF-B9CB-41F0-BC07-CA276AC42638.JPG", 1300, "En su amarra, en Inglaterra", "On her mooring in England"),
 "h-blanco":     (P1 + "68A2F908-F8E2-40EE-AF72-DA279518A3E0.JPG", 1100, "Navegando con Peter y Sylvia", "Sailing with Peter and Sylvia"),
 "h-rojas":      (P1 + "BBAC99F0-5480-4A93-97B5-B062F5873630.JPG", 1100, "Las velas rojas, ya entonces", "Red sails, even back then"),
 # historia: Sean y Debie
 "h-marea":      (P2 + "IMG_9518.HEIC", 1200, "En seco con la bajante, en la época de Sean y Debie", "Dried out at low tide, in Sean and Debie's days"),
 "h-nieve":      (P2 + "IMG_9519.HEIC", 1100, "Kitkat bajo la nieve", "Kitkat under snow"),
 "h-montana":    (P2 + "IMG_9520.HEIC", 1200, "Con Sean y Debie, entre montañas", "With Sean and Debie, among the mountains"),
 "h-puerto":     (P2 + "IMG_9521.HEIC", 1200, "Con Sean y Debie, en puerto", "With Sean and Debie, in harbour"),
 # historia: Sebastián (Colonia, mayo de 2020; foto de @barullo.sailing)
 "h-colonia":    (F + "200520 Colonia/WhatsApp Image 2023-01-23 at 16.50.46.jpeg", 1300, "En Colonia, mayo de 2020. Foto: @barullo.sailing", "Colonia, May 2020. Photo: @barullo.sailing"),
 # la tripulación de hoy
 "t-sean":       ("ig:C4A2hu-ruHT_01.jpg", 1440, "Navegando otra vez con Sean, marzo de 2024", "Sailing with Sean again, March 2024"),
 "t-regata":     ("ig:DMVXnfgx8rM_01.jpg", 1440, "Con amigos, en la regata del YCU", "With friends at the YCU regatta"),
 "t-proa":       ("ig:C3f8NHpLSun_06.jpg", 1440, "Mirando el agua desde proa", "Watching the water from the bow"),
 "t-chicos":     ("ig:DMITInIR6-G_02.jpg", 1440, "Kitkat, según los más chicos", "Kitkat, as seen by the kids"),
}

os.makedirs(SALIDA, exist_ok=True)
for f in os.listdir(SALIDA):                      # sin restos de selecciones anteriores
    if f.endswith(".jpg"): os.remove(os.path.join(SALIDA, f))
meta, faltan, total = {}, [], 0
for clave, (rel, lado, epi, cap) in FOTOS.items():
    ruta = os.path.join(IG, rel[3:]) if rel.startswith("ig:") else os.path.join(GENERAL, rel)
    if not os.path.isfile(ruta):
        faltan.append(clave); continue
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
    im.thumbnail((lado, lado), Image.LANCZOS)
    destino = os.path.join(SALIDA, clave + ".jpg")
    im.save(destino, "JPEG", quality=80, optimize=True, progressive=True)   # sin exif: sin GPS
    total += os.path.getsize(destino)
    meta[clave] = {"src": "fotos/" + clave + ".jpg", "w": im.width, "h": im.height, "t": epi, "en": cap}

with open(os.path.join(SALIDA, "fotos.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("/* generado por fotos.py */\nvar FOTOS = " + json.dumps(meta, ensure_ascii=False, indent=1) + ";\n")
print("%d fotos, %.1f MB" % (len(meta), total / 1e6))
if faltan: print("sin archivo (no se muestran):", ", ".join(faltan))
