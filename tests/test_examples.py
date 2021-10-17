#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import wyc
from glob import glob

def test():
    for f in glob("examples/*.py"):
        src = open(f).read()
        js = wyc.build(src)
        assert 'customElements.define(' in js
        assert "_pyfunc_op_instantiate" not in js
        with open(f+".js","w+") as fid:
            fid.write(js)


