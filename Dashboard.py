import xml.etree.ElementTree as ET
import webbrowser
from tabulate import tabulate
from HTML import HTML
from Command import Command
from Instruction import Instruction

def create_file(file_name,file_content):
    f = open(file_name,'wb')
    f.write(file_content)
    f.close()

# Command of instruction factory
def createCommand(node):
    exec = node.find('Executable').text
    rt = Command(exec)
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
    html_file_name = 'Dashboard.html'
    html = HTML(tabs_dict)
    create_file(html_file_name,html.file_content)
    webbrowser.open_new_tab(html_file_name)

    # Print result
    print_result(tabs_dict)
    
if __name__ == "__main__":
    main()
