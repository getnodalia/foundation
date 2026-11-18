# Ilustración del icono de una app

`portrait.py` convierte un retrato histórico en la ilustración del icono de una app Nodalia: busca
la figura en la imagen, la recorta del fondo, la pasa a blanco y negro con algo más de contraste y
la pone, con una sombra suave detrás, sobre un campo a sangre del color de la app. Sale un PNG de
1024 px que cada app convierte en su SVG maestro y en todos sus tamaños (la regla y la lista de
figuras están en `docs/iconography.md`).

## Uso

```sh
pip install "rembg[cpu]" pillow   # el modelo de recorte se descarga la primera vez
python3 tools/app-portrait/portrait.py RETRATO SALIDA.png --box L,T,R,B --colors ARRIBA ABAJO
```

- `--box`: el cuadrado del retrato, en píxeles del original, que llena la baldosa. Puede salirse
  de la imagen (lo que queda fuera es fondo). Encuadra cabeza y hombros, con el busto llegando al borde de abajo y sin cortarlo por los lados, con la cabeza ocupando
  más o menos la mitad del ancho, para que se lea a 32 px.
- `--colors`: los dos tonos del campo, arriba y abajo, los mismos del icono anterior y de la
  ventana del DMG de la app.
- `--gamma`: por encima de 1 oscurece los medios tonos, útil en fotos quemadas o grabados claros.
- `--add-mask X,Y,X,Y,...`: un polígono, en píxeles del original, que se suma a la figura cuando
  el modelo pierde un hombro en un fondo del mismo tono.
- `--mask X,Y,X,Y,...`: un polígono, en píxeles del original, que es la figura entera en lugar
  del recorte del modelo. Sirve para grabados, cuyo fondo rayado el modelo toma por parte de la
  figura.
- `--model`: el modelo de rembg; `u2net_human_seg` (el de por defecto) es el que mejor separa
  retratos.

## Ejemplos

```sh
# Trama: Jacquard, de un grabado de 1878 (Wikimedia Commons, dominio público; la versión de
# 1280 px). El fondo rayado obliga a trazar la figura con --mask.
python3 tools/app-portrait/portrait.py "Joseph_Marie_Jacquard-portrait.jpg" trama.png \
  --box 210,170,1090,1050 --colors '#9A45E2' '#7A26C9' --gamma 1.25 \
  --mask 180,1300,230,1000,260,860,330,780,420,700,452,630,450,560,442,480,468,400,512,325,568,262,640,238,708,240,770,272,822,330,858,410,872,495,864,560,846,612,880,660,960,730,1030,820,1080,940,1110,1100,1130,1300

# Ánima: Émile Cohl, foto de hacia 1885 (Wikimedia Commons, dominio público).
python3 tools/app-portrait/portrait.py "Emile_Cohl_portrait.jpg" anima.png --box 0,20,1080,1100 \
  --colors '#6B4CE8' '#5034C6' --gamma 1.1
```

Mira siempre el resultado a 512, 64 y 16 px antes de llevarlo a la app.
