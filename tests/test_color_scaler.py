from colorgrade import ColorScaler

from colour import Color


def color(name):
    return Color(name).hex_l.replace("#", "hex")


def test_color_scaler_mid():
    cs = ColorScaler(0, 0.5, 1)
    assert cs.scale(-1.0) == color("lime")
    assert cs.scale(0.0) == color("lime")
    assert cs.scale(0.5) == color("yellow")
    assert cs.scale(1.0) == color("red")
    assert cs.scale(2.0) == color("red")

    cs = ColorScaler(0, 0.0, 1)
    assert cs.scale(-1.0) == color("yellow")
    assert cs.scale(0.0) == color("yellow")
    assert cs.scale(0.5) == color("#ff8000")
    assert cs.scale(1.0) == color("red")
    assert cs.scale(2.0) == color("red")

    cs = ColorScaler(0, 1.0, 1)
    assert cs.scale(-1.0) == color("lime")
    assert cs.scale(0.0) == color("lime")
    assert cs.scale(0.5) == color("#7fff00")
    assert cs.scale(1.0) == color("yellow")
    assert cs.scale(2.0) == color("yellow")

    cs = ColorScaler(0, -1, 1)
    assert cs.scale(-1.0) == color("yellow")
    assert cs.scale(0.0) == color("yellow")
    assert cs.scale(0.5) == color("#ff8000")
    assert cs.scale(1.0) == color("red")
    assert cs.scale(2.0) == color("red")

    cs = ColorScaler(0, 2, 1)
    assert cs.scale(-1.0) == color("lime")
    assert cs.scale(0.0) == color("lime")
    assert cs.scale(0.5) == color("#7fff00")
    assert cs.scale(1.0) == color("yellow")
    assert cs.scale(2.0) == color("yellow")

    cs = ColorScaler(0, 0, 0)
    assert cs.scale(-1.0) == color("yellow")
    assert cs.scale(0.0) == color("yellow")
    assert cs.scale(0.5) == color("yellow")
    assert cs.scale(1.0) == color("yellow")
    assert cs.scale(2.0) == color("yellow")
