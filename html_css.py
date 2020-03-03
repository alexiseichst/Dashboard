import webbrowser
import xml.etree.cElementTree as ET

class HTML:
    def __init__(self,tabs):
        self.__tabs = tabs

    @property
    def file_content(self):
        return self.__gen_content()
    
    @property
    def tabs(self):
        return self.__tabs

    def __gen_content(self):
        root = ET.Element("root")
        doc = ET.SubElement(root, "doc")

        for name,tab in self.tabs.items():
            self.__gen_tab(doc,name,tab)
        
        return ET.tostring(root)

    def __gen_tab(self,elem,name,tab):
            #Table
            elem = ET.SubElement(elem, "table",style="width:100%")

            #Head
            elem = ET.SubElement(elem, "tr")
            for col in tab[0]:        
                ET.SubElement(elem, "th").text = col

            #Data
            for t in tab[1:]:
                elem = ET.SubElement(elem, "tr")
                for col in t:
                    ET.SubElement(elem, "td").text = col

def main():
    html = HTML({"Daily build":[['Name','Description','Result'],
                    ['AmesimDB','Amesim daily build','True'],
                    ['LyonDB','Lyon daily build','True'],
                    ['ChennaiDB','Chennai daily build','True'],
                    ['BracovDB','Bracov daily build','False']],
                "Proto":[['Name','Description','Result'],
                    ['AmesimProto','Amesim Proto','True'],
                    ['LyonProto','Lyon Proto','True'],
                    ['ChennaiProto','Chennai Proto','True'],
                    ['BracovProto','Bracov Proto','False']]})

    file_name = 'dashboard.html' 
    create_html_file(file_name,html.file_content)
    webbrowser.open_new_tab(file_name)

def create_html_file(file_name,file_content):
    f = open(file_name,'wb')
    f.write(file_content)
    f.close()

if __name__ == "__main__":
    main()