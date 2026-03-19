import contextlib

import colour
import matplotlib.style
import matplotlib.pyplot
import numpy

from ._conversions import BaseCCTConversion


@contextlib.contextmanager
def set_matplotlib_dark_style():
    """
    Stolen from Troy who stole it from Zach Lewis who stole it from Jed Smith.

    Works best with::
        spectral_locus_colours="RGB",
        show_diagram_colours=False,
        transparent_background=False,
    """

    STYLE_MATPLOTLIB_BASICS = {
        "figure.figsize": (12.0, 12.0),
        "figure.dpi": 72,
        "savefig.dpi": 72,
        "savefig.bbox": "tight",
        "font.size": 16,
    }

    # JERK_MODE = JEd's daRK MODE
    STYLE_MATPLOTLIB_JERK_MODE = {
        "axes.facecolor": "(0.1, 0.1, 0.1, 0.1)",
        "lines.color": "gray",
        "lines.linewidth": 1.0,
        "patch.edgecolor": "gray",
        "text.color": "(0.8, 0.8, 0.8)",
        "axes.edgecolor": "(0.3, 0.3, 0.3)",
        "axes.labelcolor": "(0.8, 0.8, 0.8)",
        "xtick.color": "(0.6, 0.6, 0.6)",
        "ytick.color": "(0.6, 0.6, 0.6)",
        "grid.color": "#222",
        "markers.fillstyle": "none",
        # not sure what they does ?
        "figure.facecolor": "orange",
        "figure.edgecolor": "green",
        "savefig.facecolor": "yellow",
        "savefig.edgecolor": "blue",
        # top right legend
        "legend.facecolor": "(0.2, 0.2, 0.2)",
        "legend.edgecolor": "(0.2, 0.2, 0.2, 0.0)",
    }

    style = STYLE_MATPLOTLIB_BASICS.copy()
    style.update(**STYLE_MATPLOTLIB_JERK_MODE)

    try:
        with matplotlib.style.context(style):
            yield
    finally:
        pass


@set_matplotlib_dark_style()
def plot_cct_conversion(cct_conversion: BaseCCTConversion):
    """
    References:
        - [1] https://colab.research.google.com/drive/1NRcdXSCshivkwoU2nieCvC3y14fx1X4X#scrollTo=Eh7rtFH5Gm-T
    """
    figure: matplotlib.pyplot.Figure
    axes: matplotlib.pyplot.Axes
    array = numpy.full((2, 2, 3), cct_conversion.rgb)
    zoom = 0.6
    offset = (0.1, 0.1)
    (
        figure,
        axes,
    ) = colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1960UCS(
        array,
        colourspace=cct_conversion.colorspace,
        colourspaces=[cct_conversion.colorspace],
        scatter_kwargs={
            "s": 90,  # size
            "c": [1, 1, 1],  # color
            "marker": "+",
            "zorder": 0,
        },
        # styling
        spectral_locus_colours="RGB",
        show_diagram_colours=False,
        transparent_background=False,
        standalone=False,
        # initial bb = (-0.1, 0.7, -0.2, 0.6)
        bounding_box=(
            -0.1 * zoom + offset[0],
            0.7 * zoom + offset[0],
            -0.2 * zoom + offset[1],
            0.6 * zoom + offset[1],
        ),
    )
    colour.plotting.temperature.plot_planckian_locus(
        "#5A534C", axes=axes, method="CIE 1960 UCS"
    )

    return figure, axes
