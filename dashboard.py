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

class command:
    executable = ''
    args = []
    std = ''

    # Constructor with executable name and std type
    def __init__(self, executable, std):  
        self.executable = executable
        self.std = std
        self.args = []

    def __str__(self):
        rt = ''
        rt+='Executable: {}'.format(self.executable)
        for arg in self.args:
            rt+='\n\t\tArg: {}'.format(arg)
        return rt

    # Add argumment of the command
    def addArg(self,arg):  
        self.args.append(arg)

    # Execute the command
    def exec(self):
        rt = {}
        command = [self.executable]
        command += self.args
        process = subprocess.Popen(command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        rt['stdout'], rt['stderr'] = process.communicate()
        return rt

class instruction:
    name = ''
    description = ''
    commands = []

    # constructor
    def __init__(self, name):  
        self.name = name
        self.description = ''
        self.commands = []
    
    def __str__(self):
        rt = ''
        rt+='{}'.format(self.name)
        rt+='\n\tDescription: {}'.format(self.description)
        rt+='\n\tResult: {}'.format(self.getResult())
        for c in self.commands:
            rt+='\n\t{}'.format(c.__str__())
        return rt

    # Description   
    def setName(self,name):
        self.name = name

    def getName(self):
        return self.name

    # Description   
    def setDescription(self,description):  
        self.description = description

    def getDescription(self):      
        return self.description

    # Commands   
    def addCommand(self,command):  
        self.commands.append(command)

    # Execute all commands and compare the result
    def getResult(self):
        rt = True
        res = self.commands[0].exec()
        for c in self.commands:
            if res != c.exec():
                rt = False
                break
        return rt

class html:
    instructions = {}

    # constructor
    def __init__(self, instructions):  
        self.instructions = instructions

    def getFileContent(self):
        return self.getTableHead()

    def getHead(self,cols):
        txt = "<tr>"
        for c in cols:
           txt += "<th>{}</th>".format(c)
        txt += "</tr>"
        return txt

    def getLine(self,cols):
        txt = "<tr>"
        for c in cols:
           txt += "<td>{}</td>".format(c)
        txt += "</tr>"
        return txt

    def generateTable(self):
        txt = "<table style=\"width:100%\">"
        txt += self.getHead(['Name','Description','Result'])
        for key in self.instructions:
            inst = self.instructions[key]
            txt += self.getLine([inst.getName(),
                                inst.getDescription(),
                                inst.getResult()])
        txt += "</table>"
        return txt
        

    def generateFile(self):
        file_name = 'dashboard.html'
        txt = self.generateTable()
        f = open(file_name,'wb')
        f.write(txt.encode())
        f.close()
        return file_name

# Command of instruction factory
def createCommand(node):
    exec = node.find('executable').text
    std = node.attrib['std']
    rt = command(exec,std)
    for a in node.findall('arg'):
       rt.addArg(a.text)
    return rt

# Instruction factory
def createInstructions(node):
    rt = instruction(node.tag)
    rt.setDescription(node.find('description').text)
    for c in node.findall('command'):
        rt.addCommand(createCommand(c))
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
    html_file = html(inst_dict)
    html_file.generateFile()
    webbrowser.open_new_tab(html_file.generateFile())
    
if __name__ == "__main__":
    main()
