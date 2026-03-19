import numpy


def rgb_array_to_single_line(array: numpy.ndarray, ndecimals: int) -> str:
    r = round(float(array[0]), ndecimals)
    g = round(float(array[1]), ndecimals)
    b = round(float(array[2]), ndecimals)
    return f"{r} {g} {b} 1.0"


def rgb_array_to_tuple(array: numpy.ndarray, ndecimals: int) -> str:
    r = round(float(array[0]), ndecimals)
    g = round(float(array[1]), ndecimals)
    b = round(float(array[2]), ndecimals)
    return f"({r}, {g}, {b})"


def rgb_array_to_nuke(
    array: numpy.ndarray,
    ndecimals: int,
    node_name: str,
    node_label: str,
) -> str:
    r = round(float(array[0]), ndecimals)
    g = round(float(array[1]), ndecimals)
    b = round(float(array[2]), ndecimals)
    return f"""
Constant {{
 inputs 0
 channels rgb
 color {{{r} {g} {b} 1}}
 color_panelDropped true
 name {node_name}
 label "{repr(node_label)[1:][:-1]}"
 selected true
 xpos 0
 ypos 0
}}"""


def xy_array_to_tuple(array: numpy.ndarray, ndecimals: int) -> str:
    x = round(float(array[0]), ndecimals)
    y = round(float(array[1]), ndecimals)
    return f"({x}, {y})"
