# Mapa conceptual: Circuitería alternativa de E/S

**Materia:** Sistemas Programables
**Actividad:** 4
**Alumno:** [TU NOMBRE]

Mapa conceptual programado en Python (matplotlib) sobre la circuitería alternativa de Entrada/Salida: las técnicas de transferencia (E/S programada, por interrupciones y DMA), el direccionamiento de E/S, los circuitos integrados de apoyo (8255, 8251, 8254, 8259, 8237) y los periféricos.

![Mapa conceptual](mapa_conceptual.png)

## Reglas de mapa conceptual que sigue

- Un **concepto principal** en la parte superior.
- **Jerarquía** de lo general a lo particular.
- Conceptos dentro de recuadros y unidos por **líneas con palabras de enlace** (*se basa en, requiere, responde con, agiliza con, se apoya en*).
- Se puede leer como proposiciones, por ejemplo: *"La circuitería alternativa de E/S agiliza con el acceso directo a memoria"* o *"…se apoya en circuitos de apoyo"*.
- **Ejemplos** concretos dentro de cada concepto (8259, 8237, 8255, 8251, 8254).

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python mapa_conceptual.py
```

El programa abre el mapa en una ventana y lo guarda como `mapa_conceptual.png`.

## Estructura del código

- `CONCEPTOS`: diccionario con cada nodo (texto, posición, nivel y rama).
- `RELACIONES`: lista de flechas con su palabra de enlace.
- `dibujar_mapa()`: dibuja las relaciones, luego los conceptos, y guarda la imagen.
