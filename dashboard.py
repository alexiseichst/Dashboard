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
    instructions = {}

    # constructor
    def __init__(self, instructions):  
        self.instructions = instructions

    @property
    def file_content(self):
        return self.__generate_table()

    def __gen_head(self,cols):
        txt = "<tr>"
        for c in cols:
           txt += "<th>{}</th>".format(c)
        txt += "</tr>"
        return txt

    def __gen_line(self,cols):
        txt = "<tr>"
        for c in cols:
           txt += "<td>{}</td>".format(c)
        txt += "</tr>"
        return txt

    def __generate_table(self):
        txt = "<table style=\"width:100%\">"
        txt += self.__gen_head(['Name','Description','Result'])
        for key in self.instructions:
            inst = self.instructions[key]
            txt += self.__gen_line([inst.name,
                                inst.description,
                                inst.result])
        txt += "</table>"
        return txt
        

    def generate_file(self):
        file_name = 'dashboard.html'
        txt = self.file_content
        f = open(file_name,'wb')
        f.write(txt.encode())
        f.close()
        return file_name

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

def main():
    print("Reading xml...")
    inst_dict = parseInstructions()

    print("Generate html...")
    html_file = HTML(inst_dict)
    html_file.generate_file()
    webbrowser.open_new_tab(html_file.generate_file())
    
if __name__ == "__main__":
    main()
