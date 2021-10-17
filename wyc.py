#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2021 manatlan manatlan[at]gmail(dot)com
#
#    MIT licence
#
#    https://github.com/manatlan/wyc
#
##############################################################################
import io, tokenize, re
import pscript

__version__ = "1.0.0"

class WycException(Exception): pass

def remove_comments_and_docstrings(source:str):
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    out = '\n'.join(l for l in out.splitlines() if l.strip())
    return out


def className2tagName(cn:str):
    words=''.join(" " + x if x.isupper() else x for x in cn).strip(" ").split(" ")
    return "-".join( [i.lower() for i in words] ) if len(words)>1 else None



def build( code:str ) -> str:
    """ return the JS for components declared in 'code' source """

    def react(*ln):
        def _(f):
            f._reacts = ln
            return f
        return _

    class HTMLElement:
        classes={}
        js=""

        def __init__(self):
            cn=self.__class__.__name__
            observedAttributes=[]
            reacts={}
            for i in dir(self):
                o=getattr(self,i)
                if hasattr(o,"_reacts"): #it's kindly a reacted method
                    observedAttributes = list(sorted(list( set( observedAttributes + list(o._reacts) ) )))
                    for name in o._reacts:
                        reacts.setdefault(name,[]).append( i )

            template = self.__doc__
            if template:
                template = f"`{template}`"
            else:
                template = "null"

            HTMLElement.classes[cn] = dict(
                attrs=observedAttributes,
                reacts=reacts,
                template=template,
            )


    # test the python syntax of the code
    # by executing the code (help to find wyc'able class later)
    g=globals()
    g["HTMLElement"]=HTMLElement
    g["react"]=react
    g["__doc__"]=None
    try:
        exec(code, g)
    except Exception as e:
        raise WycException(f"Python code has invalid syntax {e}")

    # get eventual JS in __main__ __doc__
    HTMLElement.js = g["__doc__"] or ""

    # remove comments and docstrings
    code=remove_comments_and_docstrings(code)

    # remove decorators (coz, don't need them anymore)
    code=re.sub(r'@react\([^\)]+\)',"",code)

    # find wyc'able classNames
    classNames = [ n for n,o in g.items() if isinstance(o, type) and o!=HTMLElement and issubclass(o,HTMLElement)]
    if not classNames:
        raise WycException(f"There is no Wyc'able class")

    # instanciate the class, for declarations (build HTMLElement.classes)
    for className in classNames:
        try:
            exec(className+"()")
        except Exception as e:
            raise WycException(f"Can't instanciate class {className} coz {e}")

    # py2js convert
    try:
        js=pscript.py2js( code )
    except Exception as e:
        raise WycException(f"Python code can't be transpiled to javascript coz {e}")

    # remove "_pyfunc_op_instantiate" (useless for our needs, will be replaced later)
    js=re.sub(r"var _pyfunc_op_instantiate = function.*?};\n","",js,flags=re.DOTALL)

    #build class specializations
    jss=[]
    for className,cfg in HTMLElement.classes.items():
        attrs=cfg["attrs"]
        reacts=cfg["reacts"]
        template=cfg["template"]

        # replace the js constructor
        orig=r"%s = function \(\) {\s+_pyfunc_op_instantiate\(this, arguments\);" % className
        dest=r"""%s = function () {
let o=Reflect.construct(HTMLElement, [], %s);
if(o._template) {
    let tpl = document.createElement('template');
    tpl.innerHTML = o._template;
    o.attachShadow({"mode": "open"}).appendChild(tpl.content.cloneNode(true));
}
if(o.init) o.init();
return o;""" % (className,className)

        js=re.sub(orig,dest,js)

        # build the html tag name
        tagName = className2tagName(className)
        if not tagName:
            raise WycException(f"The name of the class '{className}' should contain more than one word (try 'My{className}' instead)")

        # specialize js classes
        jss.append(f"""//================================================================== {className} ({tagName})
Object.defineProperty({className}, 'observedAttributes', {{
  get: function() {{ return {attrs}; }}
}});

{className}.prototype._template = {template};
{className}.prototype._reacts = {reacts};

{className}.prototype.attributeChangedCallback = function (attr, old_value, new_value) {{
    if( this._reacts[attr] ) {{
        for(var idx in this._reacts[attr]) {{
            let method=this._reacts[attr][idx]
            this[method](); // call reacted method
        }}
    }}
}};

customElements.define("{tagName}", {className});
""")

    pub = f"// Generated by WYC {__version__} (https://github.com/manatlan/wyc)\n"
    return pub+HTMLElement.js+"\n"+js+"\n".join(jss)
