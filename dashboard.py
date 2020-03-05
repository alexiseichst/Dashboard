import subprocess
import xml.etree.ElementTree as ET
import webbrowser
from tabulate import tabulate

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
        return self.__description

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
        root = ET.Element("html")
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
    exec = node.find('Executable').text
    std = node.attrib['std']
    rt = Command(exec,std)
    for a in node.findall('Args/*'):
       rt.add_arg(a.text)
    return rt

# Instruction factory
def createInstructions(node):
    rt = Instruction(node.attrib['name'])
    rt.description = node.attrib['description']
    for c in node.findall('CompareValues/Commands/*'):
            rt.add_command(createCommand(c))
    return rt

# Read the instructions in instructions.xml
def parseInstructions():
    inst_dict = {}
    root = ET.parse('instructions.xml').getroot()
    for node in root.findall('Instructions/*'):
        inst_dict[node.attrib['name']] = createInstructions(node)
    return inst_dict

def genTabsDict(inst_dict):
    tabs_dict = {}
    tab = [['Name','Description','Result']]
    for i in inst_dict:
        inst = inst_dict[i]
        tab.append([inst.name,inst.description,inst.result])
    tabs_dict['Daily Build'] = tab
    return tabs_dict

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def color_text(text):
    color = ''
    if (text == True):
        color = bcolors.OKGREEN
    elif (text == False):
        color = bcolors.FAIL
    return "{}{}{}{}{}".format(bcolors.ENDC,color,text,color,bcolors.ENDC)

def set_color(tabs_dict):
    for tab in tabs_dict:
        for l in tabs_dict[tab][1:]:
            l[-1] = color_text(l[-1])
    return tabs_dict

def print_result(tabs_dict):
    # Print result
    tabs_dict = set_color(tabs_dict)
    print("\n\n")
    for i in tabs_dict:
        print(tabulate(tabs_dict[i][1:], headers=tabs_dict[i][0]))
    print("{}\n\n{}".format(bcolors.ENDC,bcolors.ENDC))

def main():
    # Read xml and get results
    inst_dict = parseInstructions()
    tabs_dict = genTabsDict(inst_dict)

    # Create HTML
    #html_file_name = 'Dashboard.html'
    #html = HTML(tabs_dict)
    #create_html_file(html_file_name,html.file_content)
    #webbrowser.open_new_tab(html_file_name)

    # Print result
    print_result(tabs_dict)
    
if __name__ == "__main__":
    main()
