#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 CGRnDStudio.

Create pivot curve from surface
Author: andy
WeChat: CGRnDStudio
E-mail: andyvfxtd@gmail.com
Last edited: May 2017
"""

import pymel.core as pm


def center_pivot_pos(circles):
    """
    selected object center position
    :param circles: selected object
    :return: vector
    """
    bbx = pm.xform(circles, q=True, bb=True, ws=True)
    cx = (bbx[0] + bbx[3]) / 2.0
    cy = (bbx[1] + bbx[4]) / 2.0
    cz = (bbx[2] + bbx[5]) / 2.0
    # pm.spaceLocator(p=(cx, cy, cz))
    return cx, cy, cz


def pick_circle():
    """
    set nurbsCircle
    :return: None
    """
    sel = pm.ls(sl=1)
    if len(sel) == 1:
        pm.textFieldButtonGrp("pickCircle", text=sel[0].name(), edit=1)
    else:
        # pm.error("Select circle error")
        pm.inViewMessage(smg="Select circle error", pos="midCenter", bkc=0x00FF1010, fade=True)


def cut_curve(*args):
    """
    cut curve function
    :param args: None
    :return: None
    """
    curves = pm.ls(sl=1)
    pm.group(empty=1, name="curve_group")
    for each in curves:
        # duplicate circle
        circle_ = pm.textFieldButtonGrp("pickCircle", q=1, text=1)
        circle_d = pm.duplicate(circle_, rr=1)
        # create extrude surface
        pm.pathAnimation([circle_d, each], followAxis="y")
        surf = pm.extrude([circle_d, each], ch=True, rn=True, po=0, et=2, ucp=0, fpt=0, upn=0, rotation=0, scale=1,
                          rsp=1)
        name = surf[0].name()

        # set subCurve Max Value
        sc = pm.floatSliderGrp("scale", q=1, value=1)
        pm.setAttr("subCurve2.maxValue", sc)
        # create center pivot curve and group
        new_curve(name)
        # delete extrude surface
        # delete circle
        pm.delete([surf, circle_d])


def new_curve(surface_):
    """
    new curve group
    :param surface_: nurbsSurface with path animation
    :return: None
    """
    points = []
    num = pm.getAttr("extrudedSurfaceShape1.spansV")
    for i in range(0, num + 3):
        pos = center_pivot_pos("%s.cv[0:7][%d]" % (surface_, i))
        # print pos
        # pm.spaceLocator(p=pos)
        points.append(pos)
    curve_ = pm.curve(p=points)
    pm.parent(curve_, "curve_group")


def init_ui():
    """
    create ui
    :return: None
    """
    name = "Curves cut tool"
    win_n = "_".join(name.split(" "))
    if pm.window(win_n, exists=True):
        pm.deleteUI(win_n)
    window = pm.window(name, title=name)
    pm.columnLayout(adj=1)
    pm.text(label="Pick a Circle first!")
    pm.textFieldButtonGrp("pickCircle", label="nurbsCircle:", text="", buttonLabel="Pick", buttonCommand=pick_circle)
    pm.floatSliderGrp("scale", label="Scale:", field=1, value=0.500, min=0, max=1, precision=3)
    pm.text(label="Select curves, then click Cut!")
    pm.button(label="Cut", command=cut_curve)
    pm.showWindow(window)


if __name__ == "__main__":
    init_ui()
