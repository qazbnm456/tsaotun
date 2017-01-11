# -*- coding: UTF-8 -*-
"""
This module provides a recursive way to dig down through nested objects.
Taken from http://pingfive.typepad.com/blog/2010/04/deep-getattr-python-function.html, and made by Andew.
"""


def deepgetattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value"""
    return reduce(getattr, attr.split('.'), obj)
