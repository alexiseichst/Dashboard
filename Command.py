import subprocess

class Command:
    # Constructor with executable name and std type
    def __init__(self, executable):  
        self.__executable = executable
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
    @property
    def result(self):
        rt = {}
        command = "{} {}".format(self.__executable,' '.join(self.__args))
        process = subprocess.Popen(command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True)
        rt['stdout'], rt['stderr'] = process.communicate()
        rt['command'] = command
        return rt