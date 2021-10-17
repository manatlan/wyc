# wyc
Create a Web Component (a Custom Element) from a python file (transpile python code to javascript (es2015)).

## features

 * Use python to define your custom element (the important one ;-))
 * Use @react decorator to auto declare js methods (avoid `observedAttributes` and `attributeChangedCallback`)
 * can generate multiple custom elements from a single python file
 * auto register component's names in the page, based on classnames (_customElements.define("my-component", MyComponent)_)
 * include javascript code (in module _docstring_)
 * generate es2015 javascript, for a maximum of compatibilities
 * 100% unittest coverage
 * should work with py2 too

## install

```pip install wyc```

## usecase

On server side ... just declare a http endpoint (`/generate/<py_file>`), get the content of the `<py_file>` and just `return wyc.build(content)`.

So, your python file is automatically transpiled to JS, and directly usable in your html page, by adding a `<script src='/generate/file.py' ></script>`.

If your component class is named "MyComponent", it will be usable as `<my-component ...> ... </my-component>`

## documentation

A minimal python custom element could be:

```python
class HelloWorld(HTMLElement):
    """<div>Hello World</div>"""
    pass
```

When it's linked in your html page, you can start to use `<hello-world/>`.

Your class must inherit from `HTMLElement`, so you will have access to *shadow dom* thru `self.shadowRoot`. And your class will work exactly like `HTMLElement` in js side.


### Initialize things at constructor phase
Your component can use an `init(self)` instance method, to initialize things in the constructor phase.

```python
class HelloWorld(HTMLElement):
    """<div>Hello World</div>"""
    def init(self):
        self.root = self.shadowRoot.querySelector("div")
```

### Declare react's attributes
By using the `@react(*attributes)`, you can declare method which will be called when an attribute change (no need to use the `observedAttributes` and `attributeChangedCallback`)

```python
class HelloWorld(HTMLElement):
    """<div>Hello World</div>"""

    @react("nb")
    def method(self):
        ...
```

When attribute "nb" change, the method is called ... simple!

### Declare js code in py component
Sometimes you'll need to use external js, you can declare them in module docstrings.

```python
"""
var myExternalJs=function() { ... }
"""

class HelloWorld(HTMLElement):
    """<div>Hello World</div>"""

    def a_method(self):
        myExternalJs()
```

see [examples](examples/), for real examples and more tips ...

## history
At the beginning, I wanted to build the same kind of things for [brython](https://brython.info/) ... but it was not a good idea, because brython would have been mandatory to use them.

Based on my experience with [vbuild](https://github.com/manatlan/vbuild), I had made a POC ... And the POC comes to a real life module, which is pretty usable, in production too.

Like that, *wyc* components are usable in html/js, brython, angular, react, svelte ...etc... it's the power of standards.


