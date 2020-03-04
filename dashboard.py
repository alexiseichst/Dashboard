import subprocess
import xml.etree.ElementTree as ET
import webbrowser

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Command:
    # Constructor with executable name and std type
    def __init__(self, executable, std):  
        self.__executable = executable
        self.__std = std
        self.__args = []

    def __str__(self):
        rt = ''
        rt+='Executable: {}'.format(self.__executable)
        for arg in self.__args:
            rt+='\n  Arg: {}'.format(arg)
        return rt

    # Add argumment of the command
    def add_arg(self,arg):  
        self.__args.append(arg)

    # Execute the command
    def exec(self):
        rt = {}
        command = [self.__executable]
        command += self.__args
        process = subprocess.Popen(command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        rt['stdout'], rt['stderr'] = process.communicate()
        return rt

class Instruction:

    # constructor
    def __init__(self, name):  
        self.__name = name
        self.__description = ''
        self.__commands = []
    
    def __str__(self):
        return self.str

    @property
    def str(self):
        rt = ''
        rt+='{}'.format(self.name)
        rt+='\n Description: {}'.format(self.__description)
        rt+='\n Result: {}'.format(self.result)
        for c in self.__commands:
            rt+='\n {}'.format(c.__str__())
        return rt

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def description(self):
        return self.__name

    @description.setter
    def description(self, value):
        self.__description = value

    # Commands
    def add_command(self,command):  
        self.__commands.append(command)

    # Execute all commands and compare the result
    @property
    def result(self):
        rt = True
        res = self.__commands[0].exec()
        for c in self.__commands:
            if res != c.exec():
                rt = False
                break
        return rt

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

def create_html_file(file_name,file_content):
    f = open(file_name,'wb')
    f.write(file_content)
    f.close()

# Command of instruction factory
def createCommand(node):
    exec = node.find('executable').text
    std = node.attrib['std']
    rt = Command(exec,std)
    for a in node.findall('arg'):
       rt.add_arg(a.text)
    return rt

# Instruction factory
def createInstructions(node):
    rt = Instruction(node.tag)
    rt.description = node.find('description').text
    for c in node.findall('command'):
        rt.add_command(createCommand(c))
    print(rt)
    return rt

# Read the instructions in instructions.xml
def parseInstructions():
    inst_dict = {}
    root = ET.parse('instructions.xml').getroot()
    for node in root.findall('instructions/*'):
        inst_dict[node.tag] = createInstructions(node)
    return inst_dict

def genTabsDict(inst_dict):
    tabs_dict = {}
    tab = [['name','description','result']]
    for key in inst_dict.keys:
        inst = inst_dict[key]
        tab.append([inst.name,inst.name,inst.result])
    tabs_dict['Daily Build'] = tab
    return tabs_dict

def main():
    print("Reading xml...")
    inst_dict = parseInstructions()
    tabs_dict = genTabsDict(inst_dict)

    print("Generate html...")
    html_file_name = 'Dashboard.html'
    html = HTML(tabs_dict)
    create_html_file(html_file_name,html.file_content)
    webbrowser.open_new_tab(html_file_name)
    
if __name__ == "__main__":
    main()
