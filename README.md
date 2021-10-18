# wyc
Create a Web Component (a Custom Element) from a python file (transpile python code to javascript (es2015)).

[![Test](https://github.com/manatlan/wyc/actions/workflows/tests.yml/badge.svg)](https://github.com/manatlan/wyc/actions/workflows/tests.yml)

## Features

 * Use python to define your custom element (the important one ;-))
 * Use @react decorator to auto declare js methods (avoid `observedAttributes` and `attributeChangedCallback`)
 * can generate multiple custom elements from a single python file
 * auto register component's names in the page, based on classnames (_customElements.define("my-component", MyComponent)_)
 * include javascript code (in module _docstring_)
 * generate es2015 javascript, for a maximum of compatibilities
 * 100% unittest coverage
 * should work with py2 too

## Changelog

[Zee changelog](changelog.md)

## Install

**wyc** is on [pypi](https://pypi.org/project/wyc/) :

```pip install wyc```

## Usecase

On server side ... just declare a http endpoint (`/generate/<py_file>`), get the content of the `<py_file>` and just `return wyc.build(content)`.

So, your python file is automatically transpiled to JS, and directly usable in your html page, by adding a `<script src='/generate/file.py' ></script>`.

If your component class is named "MyComponent" (in `file.py`), it will be usable as `<my-component ...> ... </my-component>`

## Documentation

A minimal python custom element could be:

```python
class HelloWorld(HTMLElement):
    """<div>Hello World</div>"""
```

When it's linked in your html page, you can start to use `<hello-world/>`.

Your class must inherit from `HTMLElement`, so you will have access to *shadow dom* thru `self.shadowRoot`. And your class will work exactly like `HTMLElement` in js side, so there are special methods which are usable nativly:

 * `def connectedCallback(self)`: Invoked each time the custom element is appended into a document-connected element. This will happen each time the node is moved, and may happen before the element's contents have been fully parsed.
 * `def disconnectedCallback(self)`: Invoked each time the custom element is disconnected from the document's DOM.
 * `def adoptedCallback(self)`: Invoked each time the custom element is moved to a new document.

the others methods (`observedAttributes` and `attributeChangedCallback`) should not be used, because **wyc** generate them automatically depending on the usage of the `@react()` decorator.

### Declare react's attributes
By using the `@react(*attributes)`, you can declare method which will be invoked when an attribute change.

```python
class HelloWorld(HTMLElement):
    """<div>Hello World</div>"""

    @react("nb")
    def method(self):
        ...
```

When "nb" attribute change, the method is invoked ... simple!

### Initialize things at constructor phase
Your component can use an `init(self)` instance method, to initialize things at constructor phase.

```python
class HelloWorld(HTMLElement):
    """<div>Hello World</div>"""
    def init(self):
        self.root = self.shadowRoot.querySelector("div")
```

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

### Demos and examples

See [examples](examples/), for real examples and more tips ...

## History
At the beginning, I've built the same kind of things for [brython](https://brython.info/) ... but it was not a good idea, because brython would have been mandatory to use them.

Based on my experience with [vbuild](https://github.com/manatlan/vbuild), I had made a POC with the marvelous [pscript](https://pscript.readthedocs.io/en/latest/)... And the POC comes to a real life module, which is pretty usable, in production too.

Thus, **wyc** components are usable in html/js, brython, angular, vuejs, react, svelte ...etc... it's the power of standards.


