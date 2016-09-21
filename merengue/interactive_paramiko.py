import threading
import paramiko

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
            self.current_command = command
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def process(self):
        global connection
        output = []
        should_return = False
        while True:
            while should_return == False:
                if self.shell != None and self.shell.recv_ready():
                    alldata = self.shell.recv(1024)
                    while self.shell.recv_ready():
                        alldata += self.shell.recv(1024)
                    strdata = str(alldata)[2:-1]
                    #strdata = strdata[2:-1]
                    strdata = strdata.replace('\\r', '')
                    strdata = strdata.replace('\\n', ' ')
                    data = strdata.split(' ')
                    for dat in data:
                        if dat != '':
                            if dat.endswith("$"):
                                should_return = True
                            else:
                                dat = dat.replace('/', '')
                                output.append(dat)
                    print(output)
                    if should_return:
                        self.parent.Process_Output(self.current_command, output)
                        output = []
                        should_return = False
