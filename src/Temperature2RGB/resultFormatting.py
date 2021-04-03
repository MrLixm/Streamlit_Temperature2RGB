

class Numpy2String:
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
        return (f"R: {self.r} \n"
                f"G: {self.g} \n"
                f"B: {self.b} \n")

    @property
    def singleline(self):
        return f"{self.r} {self.g} {self.b} 1.0"

    def nuke(self, node_name):
        """

        Returns:

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