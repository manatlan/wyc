import re


js="""
var myjs=function() {};
var _pyfunc_op_instantiate = function (ob, args) { // nargs: 2
    if ((typeof ob === "undefined") ||
            (typeof window !== "undefined" && window === ob) ||
            (typeof global !== "undefined" && global === ob))
            {throw "Class constructor is called as a function.";}
    for (var name in ob) {
        if (Object[name] === undefined &&
            typeof ob[name] === 'function' && !ob[name].nobind) {
            ob[name] = ob[name].bind(ob);
            ob[name].__name__ = name;
        }
    }
    if (ob.__init__) {
        ob.__init__.apply(ob, args);
    }
};
var MyToto;
MyToto = function () {
};
hello
"""

jss=re.sub(r"var _pyfunc_op_instantiate = function.*?};\n","",js,flags=re.DOTALL)

print(jss)


# q="<a> <b> <c>"

# ll=re.findall("<.*?>",q)
# print(ll)