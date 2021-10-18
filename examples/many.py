
class MySimplest( HTMLElement ): #EXAMPLE: minimal one (the className + template)
    """
    <style>
    div {background:yellow}
    </style>

    <div>Hello World</div>
    """


class MyTest( HTMLElement ):    #EXAMPLE: re-render on attribte change
    """
    <style>
    * {background:red}
    </style>

    <b>Kaputt</b>
    """

    def init(self):
        self.root = self.shadowRoot.querySelector("b")

    @react("nb")
    def render(self):
        self.root.innerHTML = int(self.attributes["nb"].value) * "&#11088";



class MyTest2( HTMLElement ):   #EXAMPLE: reuse <my-test> ^^
    """
    <style>
    div {background:green}
    </style>

    <div>
        <button id="sub">-</button>
        <button id="add">+</button>
        <my-test id="mt"></my-test>
    </div>
    """

    def init(self):
        self.mt = self.shadowRoot.querySelector("#mt")
        self.shadowRoot.querySelector("#add").addEventListener('click', lambda e: self.setAttribute("value",self.getValue()+1) )
        self.shadowRoot.querySelector("#sub").addEventListener('click', lambda e: self.setAttribute("value",self.getValue()-1) )

    def getValue(self):
        return int(self.attributes["value"].value)

    @react("value")
    def render(self):
        self.mt.setAttribute( "nb", self.getValue() )



class MyBack( HTMLElement ):    #EXAMPLE: draw outside with an exposed method
    """
    <style>
        div      {background:black;padding:4px;color:red;border:4px solid black}
        div    > span {display: none}

        div.on   {border:4px solid red}
        div.on > span {display: block;position:absolute;top:0px;right:0px;background:#888}
    </style>

    <div>
        CLICK
        <span>XXX</span>
    </div>
    """

    def init(self):
        self.root = self.shadowRoot.querySelector("div")

    def connectedCallback(self): #needed to force the style !
        self.setAttribute("style","cursor:pointer;")

    def toggle(self):
        self.root.classList.toggle("on")

class MyFold(HTMLElement):  #EXAMPLE: use a slot !
    """
    <style>
        div#line {cursor:pointer}
        div#line::before {content: "▶ " }
        div#detail {display:none;margin-left:8px}
        div.open > div#line::before {content: "▼ "}
        div.open > div#detail {display:inherit}
    </style>
    <div>
        <div id="line"></div>
        <div id="detail"><slot/></div>
    <div>
    """

    def init(self):
        self.root = self.shadowRoot.querySelector("div")
        self.shadowRoot.querySelector("#line").addEventListener('click', lambda e: self.switch() )

    def connectedCallback(self):
        self.setTitle( self.getAttribute("title") or "" )

    def setTitle(self,title):
        self.shadowRoot.querySelector("#line").innerHTML = title
    def setDetail(self,detail):
        self.shadowRoot.querySelector("#detail").innerHTML = detail
    def getDetail(self,detail):
        return self.shadowRoot.querySelector("#detail").innerHTML

    def getOpen(self):
        return self.getAttribute("open") not in [None, 0, False, "0","false","no","null"]

    def switch(self):
        self.setAttribute("open",not self.getOpen())

    @react("open")
    def openclose(self, *a):
        if self.getOpen():
            self.root.classList.add("open")
        else:
            self.root.classList.remove("open")

        self.dispatchEvent( window.Event('change') )

