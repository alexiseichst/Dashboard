import xml.etree.ElementTree as ET

class HTML:
    def __init__(self,tabs):
        self.__tabs = tabs
        self.__init_bool_to_html()
        self.__init_type_to_html()
        self.__init_bool_to_style()
        self.__init_type_to_style()
        
    def __init_type_to_html(self):
        self.__type_html = {}
        self.__type_html[str] = lambda data : data
        self.__type_html[bool] = lambda data : self.bool_html(data)
    
    def __init_type_to_style(self):
        self.__type_style = {}
        self.__type_style[str] = lambda data : data
        self.__type_style[bool] = lambda data : self.bool_slyle(data)
        
    def data_to_html(self,data):
        t = type(data)
        return self.__type_html[t](data)
        
    def __init_bool_to_style(self):
        self.__bool_style = {}
        self.__bool_style[True] = lambda : 'table-success'
        self.__bool_style[False] = lambda : 'table-danger'
    
    def data_to_style(self,data):
        t = type(data)
        return self.__type_style[t](data)
        
    def __init_bool_to_html(self):
        self.__bool_html = {}
        self.__bool_html[True] = lambda : 'Valid'
        self.__bool_html[False] = lambda : 'Error'

    def bool_html(self,data):
        return self.__bool_html[data]()

    def bool_slyle(self,data):
        return self.__bool_style[data]()

    @property
    def tabs(self):
        return self.__tabs

    @property
    def file_content(self):
        html = ET.Element('html')

        #Head
        head = ET.SubElement(html,'head')
        ET.SubElement(head,'link',  rel="stylesheet",
                                    href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                                    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
                                    crossorigin="anonymous")

        #Body
        body = ET.SubElement(html, 'body')
        div = ET.SubElement(body, "div", style="overflow-x:auto;")
        for name,tab in self.tabs.items():
            self.__gen_tab(div,name,tab)
        return ET.tostring(html)

    def __gen_tab(self,elem,name,tab):
        #Table
        table = ET.SubElement(elem, "table")
        table.set('class',"table")

        #Head
        thread = ET.SubElement(table, "thead")
        thread.set('class',"table-active")
        head = ET.SubElement(thread, "tr")
        for col in tab[0]:        
            ET.SubElement(head, "th").text = col

        #Data
        for t in tab[1:]:
            data = ET.SubElement(table, "tr")
            data.set('class',self.data_to_style(t[-1]))
            for col in t:
                ET.SubElement(data, "td").text = self.data_to_html(col)