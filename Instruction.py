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
        stdout_list=[]
        stderr_list=[b'']
        for r in self.__commands:
            std = r.result
            stdout_list.append(std['stdout'])
            stderr_list.append(std['stderr'])
        result = all(stdout_list[0] == item for item in stdout_list)
        result = all(stderr_list[0] == item for item in stderr_list) and result
        return result