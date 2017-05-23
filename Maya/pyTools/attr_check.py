#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 CGRnDStudio.

Maya attributes check
Author: andy
WeChat: CGRnDStudio
E-mail: andyvfxtd@gmail.com
Last edited: May 2017
"""

SIZE = 48

import pymel.core as pm


def format_(str):
    return "|{0: <{1}}".format(str, SIZE)


def format_s():
    return "{0:-<{1}}".format("|", SIZE+2)


def check(*args):
    print format_s()*3
    node = pm.textFieldButtonGrp("nodeName", q=1, text=1)
    for i, each in enumerate(sorted(pm.listAttr(node))):
        attr = ".".join([node, each])
        nice_name = pm.attributeName(attr, nice=1)
        short_name = pm.attributeName(attr, short=1)
        print format_(nice_name), format_(each), format_(short_name)
        print format_s()*3


def init_ui():
    """
    Create ui
    :return: None
    """
    name = "Attributes Check"
    win_n = "_".join(name.split(" "))
    if pm.window(win_n, exists=True):
        pm.deleteUI(win_n)
    window = pm.window(win_n, title=name)
    pm.columnLayout(adj=1)
    pm.textFieldButtonGrp("nodeName", label="Enter node name:", buttonLabel="Check", buttonCommand=check)
    pm.showWindow(window)

if __name__ == "__main__":
    init_ui()
