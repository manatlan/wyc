#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import wyc
import pytest

def test_empty_file():
    with pytest.raises(wyc.WycException) as e_info:
        wyc.build("")


def test_bad_minimal_one():
    src="""
class Toto(HTMLElement):    # not pythonic !
"""
    with pytest.raises(wyc.WycException) as e_info:
        wyc.build(src)


def test_bad_named_single_word():
    src="""
class Toto(HTMLElement):
    pass
"""
    with pytest.raises(wyc.WycException) as e_info:
        wyc.build(src)



def test_bad_inherit():
    src="""
class MyToto:
    pass
"""
    with pytest.raises(wyc.WycException) as e_info:
        wyc.build(src)


def test_bad_syntax():
    src="""
class MyToto(HTMLElement) # miss ':'
    pass
"""
    with pytest.raises(wyc.WycException) as e_info:
        wyc.build(src)


def test_bad_cant_instanciate():
    src="""
class MyToto(HTMLElement):
    def __init__(self, DONT_CREATE_YOUR_REAL_CONSTRUCTOR):
        pass
"""
    with pytest.raises(wyc.WycException) as e_info:
        wyc.build(src)


def test_bad_react_use():
    src="""
class MyToto(HTMLElement):
    @react                  # react is bad used
    def toto(self):
        pass
"""
    with pytest.raises(wyc.WycException) as e_info:
        wyc.build(src)

def test_bad_import():
    src="""
import DONT_DO_THAT_YET     #TODO: perhaps one day ?!

class MyToto(HTMLElement):
    pass
"""
    with pytest.raises(wyc.WycException) as e_info:
        wyc.build(src)
