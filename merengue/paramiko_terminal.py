import threading
import paramiko
import sys
import colorama

class SSH_Terminal:
    shell = None
    client = None
    transport = None

    def __init__(self, address, username, password, port):
        print("Connecting to server on ip", str(address) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, int(port)))
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
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def process(self):
        global connection
        while True:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = str(alldata)
                strdata = strdata[2:-1]
                strdata = strdata.replace('\\r', '\r')
                strdata = strdata.replace('\\n', '\n')
                strdata = strdata.replace('\\x1b', '\x1b')
                data = strdata.split(' ')
                #for dat in data:
                #    print(dat)
                #print('\x1b[0m\x1b[01;34manaconda3\x1b[0m')
                print(strdata)

                #self.print_output(strdata)
                if(strdata.endswith("$ ")):
                    print("\n$ ")

    def print_output(self, text):
        first_format = ''
        second_format = ''
        for style in range(8):
            for fg in range(30,38):
                s1 = ''
                for bg in range(40,48):
                    format = ';'.join([str(style), str(fg), str(bg)])
                    color1 = '\x1b[%sm' % format
                    color2 = '\x1b[0m'
                    if text.startswith(color1):
                        first_format = colo1
                        text = text.replace(color1, '')
                    if text.endswith(color2):
                        second_format = color2
                        text = text.replace(color2, '')
        print(first_format + ' ' + text + ' ' + second_format)

colorama.init()
terminal_connection = SSH_Terminal(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
terminal_connection.openShell()
terminal_connection.sendShell('cd {}'.format(sys.argv[1]))
while True:
    try:
        command = raw_input('$ ')
    except:
        command = input('$ ')
    if command.startswith(" "):
        command = command[1:]
    terminal_connection.sendShell(command)
