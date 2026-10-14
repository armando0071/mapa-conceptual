"""
Mapa conceptual: Circuitería alternativa de Entrada/Salida (E/S)
Materia: Sistemas Programables - Actividad 4
Autor: [TU NOMBRE]

Genera el mapa conceptual con matplotlib y lo guarda como imagen PNG.
Uso:
    pip install -r requirements.txt
    python mapa_conceptual.py
"""

import logging
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Rectangle
from matplotlib.path import Path

# Evita avisos si alguna fuente de la lista no está instalada
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

# ------------------------------------------------------------------
# 1. ESTILO GENERAL
# ------------------------------------------------------------------
FONDO = "#BFDDF8"
TINTA = "#111111"
FUENTE_TITULOS = ["Bahnschrift", "Arial Narrow", "DejaVu Sans"]  # usa la primera que exista
FUENTE_TEXTO = ["Segoe UI", "Calibri", "DejaVu Sans"]

# ------------------------------------------------------------------
# 2. CONCEPTO PRINCIPAL
# ------------------------------------------------------------------
PRINCIPAL = {
    "texto": "CIRCUITERÍA ALTERNATIVA\nDE ENTRADA / SALIDA",
    "x": 48, "y": 97, "ancho": 64, "alto": 17,
    "color": "#6CB8FA",
}

# ------------------------------------------------------------------
# 3. CONCEPTOS (tarjetas)
#    x, y = esquina inferior izquierda de la tarjeta
# ------------------------------------------------------------------
ANCHO, ALTO = 37, 30
CONCEPTOS = {
    "tecnicas": {
        "titulo": "TÉCNICAS DE TRANSFERENCIA",
        "texto": "Formas de mover datos entre el CPU y los periféricos: "
                 "E/S programada (polling), por interrupciones y por "
                 "acceso directo a memoria (DMA).",
        "x": 32, "y": 55, "color": "#FDB36B", "sombra": "#E8173F",
    },
    "direcc": {
        "titulo": "DIRECCIONAMIENTO DE E/S",
        "texto": "Cada dispositivo tiene una dirección. Puede ser E/S "
                 "mapeada en memoria (instrucción MOV) o E/S aislada en "
                 "puertos (instrucciones IN / OUT).",
        "x": 91, "y": 55, "color": "#EAEAEA", "sombra": "#3AA6A0",
    },
    "inter": {
        "titulo": "INTERRUPCIONES",
        "texto": "El periférico avisa al CPU cuando necesita atención, "
                 "sin que el CPU pregunte. Las gestiona el PIC 8259 y "
                 "pueden ser enmascarables o no enmascarables (NMI).",
        "x": 8, "y": 6, "color": "#BFE3CC", "sombra": "#C06FC0",
    },
    "dma": {
        "titulo": "ACCESO DIRECTO A MEMORIA",
        "texto": "Transfiere bloques de datos entre la memoria y el "
                 "periférico sin pasar por el CPU. Lo coordina el "
                 "controlador DMA 8237.",
        "x": 61.5, "y": 6, "color": "#EFCDFB", "sombra": "#F7CF35",
    },
    "apoyo": {
        "titulo": "CIRCUITOS DE APOYO",
        "texto": "Chips que facilitan la comunicación con el exterior: "
                 "PPI 8255 (puertos paralelos), USART 8251 (serie) y "
                 "PIT 8254 (conteo y temporización).",
        "x": 115, "y": 6, "color": "#FDF5C4", "sombra": "#1E63B8",
    },
}

# ------------------------------------------------------------------
# 4. RELACIONES: líneas punteadas con palabra de enlace
#    puntos = recorrido de la línea; etiqueta = (x, y) de la palabra
# ------------------------------------------------------------------
RELACIONES = [
    {"puntos": [(70, 97), (70, 92), (50.5, 92), (50.5, 85)],
     "enlace": "se basa en", "etiqueta": (59, 92)},
    {"puntos": [(90, 97), (90, 92), (109.5, 92), (109.5, 85)],
     "enlace": "requiere", "etiqueta": (101, 92)},
    {"puntos": [(48, 108), (26.5, 108), (26.5, 36)],
     "enlace": "responde con", "etiqueta": (26.5, 44)},
    {"puntos": [(80, 97), (80, 36)],
     "enlace": "agiliza con", "etiqueta": (80, 44)},
    {"puntos": [(112, 108), (133.5, 108), (133.5, 36)],
     "enlace": "se apoya en", "etiqueta": (133.5, 44)},
]


# ------------------------------------------------------------------
# 5. FUNCIONES DE DIBUJO
# ------------------------------------------------------------------
def ruta_redondeada(puntos, radio=3):
    """Crea un trazo que pasa por los puntos con esquinas redondeadas."""
    vertices, codigos = [puntos[0]], [Path.MOVETO]
    for i in range(1, len(puntos) - 1):
        (x0, y0), (x1, y1), (x2, y2) = puntos[i - 1], puntos[i], puntos[i + 1]

        def hacia(xa, ya, xb, yb, d):
            largo = max(abs(xb - xa), abs(yb - ya))
            d = min(d, largo / 2)
            return xa + (xb - xa) / largo * d, ya + (yb - ya) / largo * d

        antes = hacia(x1, y1, x0, y0, radio)
        despues = hacia(x1, y1, x2, y2, radio)
        vertices += [antes, (x1, y1), despues]
        codigos += [Path.LINETO, Path.CURVE3, Path.CURVE3]
    vertices.append(puntos[-1])
    codigos.append(Path.LINETO)
    return Path(vertices, codigos)


def dibujar_relacion(ax, relacion):
    trazo = PathPatch(ruta_redondeada(relacion["puntos"]), fill=False,
                      edgecolor=TINTA, linewidth=2, linestyle=(0, (4, 3)),
                      zorder=1)
    ax.add_patch(trazo)
    x, y = relacion["etiqueta"]
    ax.text(x, y, relacion["enlace"], ha="center", va="center",
            fontsize=12, style="italic", fontfamily=FUENTE_TEXTO, color=TINTA,
            zorder=2, bbox=dict(boxstyle="round,pad=0.35", fc=FONDO, ec="none"))


def dibujar_tarjeta(ax, c):
    x, y = c["x"], c["y"]
    # Sombra desplazada
    ax.add_patch(FancyBboxPatch((x + 2.5, y - 2.5), ANCHO, ALTO,
                                boxstyle="round,pad=0,rounding_size=0.8",
                                fc=c["sombra"], ec=TINTA, lw=2, zorder=3))
    # Tarjeta
    ax.add_patch(FancyBboxPatch((x, y), ANCHO, ALTO,
                                boxstyle="round,pad=0,rounding_size=0.8",
                                fc=c["color"], ec=TINTA, lw=2, zorder=4))
    titulo = textwrap.fill(c["titulo"], 16)
    ax.text(x + ANCHO / 2, y + ALTO - 3, titulo, ha="center", va="top",
            fontsize=22, fontfamily=FUENTE_TITULOS, color=TINTA,
            linespacing=1.05, zorder=5)
    lineas_titulo = titulo.count("\n") + 1
    cuerpo = textwrap.fill(c["texto"], 32)
    ax.text(x + ANCHO / 2, y + ALTO - 5.5 - lineas_titulo * 3.4, cuerpo,
            ha="center", va="top", fontsize=14, fontfamily=FUENTE_TEXTO,
            color=TINTA, linespacing=1.45, zorder=5)


def icono_chip(ax, cx, cy):
    """Ícono de circuito integrado dentro de un círculo."""
    ax.add_patch(Circle((cx, cy), 11, fc="white", ec=TINTA, lw=2.2, zorder=3))
    ax.add_patch(FancyBboxPatch((cx - 5, cy - 5), 10, 10,
                                boxstyle="round,pad=0,rounding_size=1",
                                fc="#3AA6A0", ec=TINTA, lw=2, zorder=4))
    for d in (-3, 0, 3):
        for (x1, y1, x2, y2) in [(cx - 7.5, cy + d, cx - 5, cy + d),
                                 (cx + 5, cy + d, cx + 7.5, cy + d),
                                 (cx + d, cy + 5, cx + d, cy + 7.5),
                                 (cx + d, cy - 7.5, cx + d, cy - 5)]:
            ax.plot([x1, x2], [y1, y2], color=TINTA, lw=2, zorder=4,
                    solid_capstyle="round")


def icono_foco(ax, cx, cy):
    """Ícono de foco (idea / señal) dentro de un círculo."""
    ax.add_patch(Circle((cx, cy), 11, fc="white", ec=TINTA, lw=2.2, zorder=3))
    ax.add_patch(Circle((cx, cy + 2), 5.2, fc="#F7CF55", ec=TINTA, lw=2, zorder=4))
    ax.add_patch(Rectangle((cx - 2.6, cy - 6), 5.2, 4, fc="white", ec=TINTA,
                           lw=2, zorder=5))
    for dy in (-4.7, -3.3):
        ax.plot([cx - 2.6, cx + 2.6], [cy + dy, cy + dy], color=TINTA, lw=1.5,
                zorder=6)
    ax.plot([cx - 1.5, cx - 0.5, cx + 0.5, cx + 1.5],
            [cy + 1, cy + 3, cy + 1, cy + 3], color=TINTA, lw=1.5, zorder=6)


def dibujar_mapa(nombre_archivo="mapa_conceptual.png"):
    fig, ax = plt.subplots(figsize=(16, 12))
    fig.patch.set_facecolor(FONDO)
    ax.set_facecolor(FONDO)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 120)
    ax.set_aspect("equal")
    ax.axis("off")

    for relacion in RELACIONES:
        dibujar_relacion(ax, relacion)

    # Concepto principal
    p = PRINCIPAL
    ax.add_patch(FancyBboxPatch((p["x"], p["y"]), p["ancho"], p["alto"],
                                boxstyle="round,pad=0,rounding_size=0.8",
                                fc=p["color"], ec=TINTA, lw=2.2, zorder=4))
    ax.text(p["x"] + p["ancho"] / 2, p["y"] + p["alto"] / 2, p["texto"],
            ha="center", va="center", fontsize=28, fontfamily=FUENTE_TITULOS,
            color=TINTA, linespacing=1.1, zorder=5)

    for concepto in CONCEPTOS.values():
        dibujar_tarjeta(ax, concepto)

    icono_chip(ax, 15, 80)
    icono_foco(ax, 146, 66)

    ax.text(158, 1.2, "Sistemas Programables · Act. 4 · [TU NOMBRE]",
            ha="right", va="bottom", fontsize=10, color="#3A4A60",
            fontfamily=FUENTE_TEXTO)

    plt.subplots_adjust(0, 0, 1, 1)
    plt.savefig(nombre_archivo, dpi=150, facecolor=FONDO)
    print(f"Mapa guardado como {nombre_archivo}")
    plt.show()


if __name__ == "__main__":
    dibujar_mapa()
