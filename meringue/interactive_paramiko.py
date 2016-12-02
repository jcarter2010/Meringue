import threading
import paramiko
import time

class SSH:
    shell = None
    client = None
    transport = None
    parnent = None
    current_command = None

    def __init__(self, address, username, password, port, parent):
        print("Connecting to server on ip", str(address) + ".")
        self.parent = parent
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, port))
        self.transport.connect(username=username, password=password)

        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

    def closeConnection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()

    def openShell(self):
        self.shell = self.client.invoke_shell()

    def sendShell(self, command):
        if(self.shell):
            self.current_command = command[command.find('ls'):]
            print(self.current_command)
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def process(self):
        global connection
        output = []
        should_return = False
        temp_str = ''
        while True:
            while should_return == False:
                if self.shell != None and self.shell.recv_ready():
                    alldata = self.shell.recv(1024)
                    while self.shell.recv_ready():
                        alldata += self.shell.recv(1024)
                        time.sleep(0.5)
                    strdata = str(alldata)
                    strdata = strdata.replace("b'", '')
                    strdata = strdata.replace("'", '')
                    strdata = strdata.replace('\\r', '')
                    strdata = strdata.replace('\\n', '\n')
                    strdata = strdata.replace('\r', '')
                    temp_str = temp_str + strdata
                    data = strdata.split(' ')
                    for dat in data:
                        if dat != '':
                            if dat.endswith("$"):
                                should_return = True
                            else:
                                pass
                    if should_return:
                        temp = temp_str.split('\n')
                        print(temp)
                        del(temp[0])
                        del(temp[len(temp) - 1])
                        if temp[0].startswith('ls: cannot access */'):
                            output = []
                        else:
                            tot_string = ''
                            for item in temp:
                                tot_string = tot_string + ' ' + item
                            print(tot_string)
                            data = tot_string.split(' ')
                            output = []
                            for dat in data:
                                if dat != '':
                                    dat = dat.replace('/', '')
                                    output.append(dat)
                        self.parent.Process_Output(self.current_command, output)
                        should_return = False
                        temp_str = ''
