class RGBarray2String:
    """
    Convert a numpy array to a formatted string.
    The numpy array represent a RGB value
    """

    def __init__(self, numpy_ndarray, ndecimals=3):
        self.value = numpy_ndarray
        self.ndecimals = ndecimals

    @property
    def r(self):
        return round(float(self.value[0]), self.ndecimals)

    @property
    def g(self):
        return round(float(self.value[1]), self.ndecimals)

    @property
    def b(self):
        return round(float(self.value[2]), self.ndecimals)

    @property
    def linebreak(self):
        return f"R: {self.r} \n" f"G: {self.g} \n" f"B: {self.b} \n"

    @property
    def singleline(self):
        return f"{self.r} {self.g} {self.b} 1.0"

    def nuke(self, node_name):
        """
        Return a Nuke Constant node
        """
        out_str = f"""
Constant {{
 inputs 0
 channels rgb
 color {{{self.r} {self.g} {self.b} 1}}
 color_panelDropped true
 name  {node_name}
 selected true
 xpos 0
 ypos 0
}}
        """
        return out_str


class CIExy2String:
    """
    Utility to display a numpy array to string.
    The numpy array represent CIE xy chromaticity coordinates
    """

    def __init__(self, xy_array, ndecimals=3):
        self.value = xy_array
        self.ndecimals = ndecimals

    @property
    def x(self):
        return round(float(self.value[0]), self.ndecimals)

    @property
    def y(self):
        return round(float(self.value[1]), self.ndecimals)

    @property
    def tuple(self):
        return f"({self.x}, {self.y})"
