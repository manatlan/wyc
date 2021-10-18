#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import wyc
import pytest

def test_minimal_ones():
    src="""

class MyToto(HTMLElement):
    '<b>Hello</b>'

"""
    js=wyc.build(src)
    assert 'customElements.define("my-toto", MyToto);' in js

def test_minimal_name(): # 2 UPPERCASE CHAR
    src="""

class CC(HTMLElement):
    '<b>Hello</b>'

"""
    js=wyc.build(src)
    assert 'customElements.define("c-c", CC);' in js


def test_use_of_python():
    src="""

def DO_SOMETHING():
    pass

class MyToto(HTMLElement):
    def method(self):
        DO_SOMETHING()

"""
    js=wyc.build(src)
    assert "DO_SOMETHING = function" in js
    assert "DO_SOMETHING();" in js
    assert 'customElements.define("my-toto", MyToto);' in js

def test_use_of_python_class():
    src="""

class Classic:
    pass

class MyToto(HTMLElement):
    def method(self):
        Classic()

"""
    js=wyc.build(src)
    assert 'customElements.define("my-toto", MyToto);' in js


def test_react_list():
    src="""
class MyToto(HTMLElement):

    @react("nb","data-value")
    def method(self):
        pass

"""
    js=wyc.build(src)
    assert """Object.defineProperty(MyToto, 'observedAttributes', {
  get: function() { return ['data-value', 'nb']; }
});""" in js
    assert """MyToto.prototype._reacts = {'nb': ['method'], 'data-value': ['method']};""" in js
    assert 'customElements.define("my-toto", MyToto);' in js

def test_include_js():
    src="""
'''var myjs=function() {};'''

'''var myjs2=function() {};'''  # THIS ONE IS FORGOTTEN

class MyToto(HTMLElement):
    pass
"""
    # with pytest.raises(wyc.WycException) as e_info:
    js=wyc.build(src)
    assert "var myjs=function() {};" in js
    assert "var myjs2=function() {};" not in js
    assert 'customElements.define("my-toto", MyToto);' in js
