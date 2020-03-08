import xml.etree.ElementTree as ET

class HTML:
    def __init__(self,tabs):
        self.__tabs = tabs
        self.__init_bool_to_html()
        self.__init_type_to_html()
        
    def __init_type_to_html(self):
        self.__type_html = {}
        self.__type_html[str] = lambda data : data
        self.__type_html[bool] = lambda data : self.bool_html(data)
        
    def data_to_html(self,data):
        t = type(data)
        return self.__type_html[t](data)
        
    def __init_bool_to_html(self):
        self.__bool_html = {}
        self.__bool_html[True] = lambda : 'Valid'
        self.__bool_html[False] = lambda : 'Error'

    def bool_html(self,data):
        return self.__bool_html[data]()

    @property
    def tabs(self):
        return self.__tabs

    @property
    def file_content(self):
        html = ET.Element('html')

        #Head
        head = ET.SubElement(html,'head')
        ET.SubElement(head,'link',rel='stylesheet',href='styles.css')

        #Body
        body = ET.SubElement(html, 'body')
        div = ET.SubElement(body, "div", style="overflow-x:auto;")
        for name,tab in self.tabs.items():
            self.__gen_tab(div,name,tab)
        return ET.tostring(html)

    def __gen_tab(self,elem,name,tab):
        #Table
        table = ET.SubElement(elem, "table")

        #Head
        head = ET.SubElement(table, "tr")
        for col in tab[0]:        
            ET.SubElement(head, "th").text = col

        #Data
        for t in tab[1:]:
            data = ET.SubElement(table, "tr")
            for col in t:
                ET.SubElement(data, "td").text = self.data_to_html(col)