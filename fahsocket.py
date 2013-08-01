###########################################################################
#!    This program is free software: you can redistribute it and/or modify
#!    it under the terms of the GNU General Public License as published by
#!    the Free Software Foundation, either version 3 of the License, or
#!    (at your option) any later version.

#!    This program is distributed in the hope that it will be useful,
#!    but WITHOUT ANY WARRANTY; without even the implied warranty of
#!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#!    GNU General Public License for more details.

#!    You should have received a copy of the GNU General Public License
#!    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!    Copyright Cody Ferber, 2013.
###########################################################################
from contextlib import closing, ContextDecorator
import socket

###########################################################################
class Fahsocket(ContextDecorator):
###########################################################################

    def __init__(self, timeout=None, size_HDR=None, get_HOC=False, log_ON=False, debug_ON=False, sh_NLINE=False):

        self.timeout = timeout #!Time to socket time-out.
        self.size_HDR = size_HDR #!Size of header if get_HOC is True.
        self.get_HOC = get_HOC #!Get a header on connect.
        self.log_ON = log_ON #!Log console and debug output to log.txt.
        self.debug_ON = debug_ON #!Verbose debug output and write to log if log_ON is True.
        self.sh_NLINE = sh_NLINE #!Show '\n' after .splitlines() is called.
        self.connected_client = False #! Declare incase __exit__() before connect() is called.
        self.connected_server = False #! Declare incase __exit__() before connect() is called.

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except IOError as msg:

            print('\nError: ' + str(msg) + '!\n')
            Fahsocket.dolog(self, 'Error: ' + str(msg))

        return None


###########################################################################
    def __enter__(self):        

        print('\nSet socket timeout: ' + str(self.timeout))
        Fahsocket.dolog(self, 'Set socket timeout: ' + str(self.timeout))
        self.sock.settimeout(self.timeout)

        print('Set socket option: SO_REUSEADDR')
        Fahsocket.dolog(self, 'Set socket option: SO_REUSEADDR')
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sendsize = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) #! Size of send buffer.
        print('Send buffer size: ' + str(self.sendsize))
        Fahsocket.dolog(self, 'Send buffer size: ' + str(self.sendsize))

        self.recvsize = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF) #! Size of receive buffer.
        print('Receive buffer size: ' + str(self.recvsize))
        Fahsocket.dolog(self, 'Receive buffer size: ' + str(self.recvsize))

        return self


###########################################################################
    def __exit__(self, type, value, tb):

        #!If were exiting after connection has been established.
        if self.connected_client is True:

            print('\nFahsocket.__exit__(); Flushing Socket Buffer!')
            Fahsocket.dolog(self, 'Fahsocket.__exit__(); Flushing Socket Buffer!')

            if self.buffer == Fahsocket.recv(self, self.recvsize):

                print('Buffer Empty!')
                Fahsocket.dolog(self, 'Buffer Empty!')

            else:
                print('ERROR: Buffer not empty...Flushing Buffer!')
                Fahsocket.dolog(self, 'ERROR: Buffer not empty...Flushing Buffer!')
                Fahsocket.recv(self, self.recvsize)

            print('-> self.sock.shutdown()!')
            Fahsocket.dolog(self, '-> self.sock.shutdown()!')
            self.sock.shutdown(2)

            print('-> self.sock.close()!')
            Fahsocket.dolog(self, '-> self.sock.close()!')
            self.sock.close()

        elif self.connected_server is True:

            print('-> self.connection.shutdown()!')
            Fahsocket.dolog(self, '-> self.connection.shutdown()!')
            self.connection.shutdown(2)

            print('-> self.connection.close()!')
            Fahsocket.dolog(self, '-> self.connection.close()!')
            self.connection.close()

        else:
            print('Fahsocket.__exit__():')
            Fahsocket.dolog(self, 'Fahsocket.__exit__():')

        if self.debug_ON is True:

            print('\nError Type: ' + str(type))
            print('Error Value: ' + str(value))
            print('Traceback: ' + str(tb))

            Fahsocket.dolog(self, 'Error Type: ' + str(type))
            Fahsocket.dolog(self, 'Error Value: ' + str(value))
            Fahsocket.dolog(self, 'Traceback: ' + str(tb))

        #!Return True on exception; else return False on no exception.
        if type is not None:

            return True
    
        else:
            return False


###########################################################################
    def bind(self, ip, port):

        self.ip = ip
        self.port = port

        print('\nBinding: ' + str(ip) + ':' + str(port))
        Fahsocket.dolog(self, 'Binding: ' + str(ip) + ':' + str(port))
        self.sock.bind((ip, port))


###########################################################################
    def listen(self, que_conn):

        print('Listening for incoming connections on ' + str(self.ip) + ':' + str(self.port))
        Fahsocket.dolog(self, 'Listening for incoming connections on ' + str(self.ip) + ':' + str(self.port))
        self.sock.listen(que_conn)


###########################################################################
    def accept(self):

        self.connection, self.address = self.sock.accept() #!Not connected yet.
        self.connected_server = True #!Now were connected!
        print('Accepting incoming connection from ' + str(self.address))
        Fahsocket.dolog(self, 'Accepting incoming connection from ' + str(self.address))

        return self.connection


###########################################################################
    def connect(self, host, port):

        print('\nConnecting: ' + str(host) + ':' + str(port) + '\n')
        Fahsocket.dolog(self, 'Connecting: ' + str(host) + ':' + str(port))
        self.sock.connect((host, port)) #!Not connected yet.
        self.connected_client = True #!Now were connected!

        if self.get_HOC is True:

            Fahsocket.recv(self, self.size_HDR)
            Fahsocket.recv(self, self.recvsize - self.size_HDR)

        else:
            Fahsocket.recv(self, self.recvsize)


###########################################################################
    def send(self, command):

        print('\nSending: ' + str(command.splitlines(self.sh_NLINE)[0]) + '\n')
        Fahsocket.dolog(self, 'Sending: ' + str(command.splitlines(self.sh_NLINE)[0]))
        self.sock.send(command.encode('utf-8'))


###########################################################################
    def recv(self, size):

        self.pyon_data = []
        self.buffer = self.sock.recv(size).splitlines(self.sh_NLINE)

        for i, v in enumerate(self.buffer):

            v = v.decode('utf-8')
            list.append(self.pyon_data, v)
            print(v)
            Fahsocket.dolog(self, v)

        return self.pyon_data


###########################################################################
    def setsendbuffer(self, do, size): #!Use setsendbuffer(False, None) to only return size.

        if do is True:

            print('\nSet send buffer size: ' + str(size))
            Fahsocket.dolog(self, 'Set send buffer size: ' + str(size))
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, size)
            self.sendsize = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

        return self.sendsize


###########################################################################
    def setrecvbuffer(self, do, size): #!Use setrecvbuffer(False, None) to only return size.

        if do is True:

            print('\nSet receive buffer size: ' + str(size))
            Fahsocket.dolog(self, 'Set receive buffer size: ' + str(size))
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, size)
            self.recvsize = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

        return self.recvsize


###########################################################################
    def getparameter(self, pyon_data, parameter):

        self.data = []

        for i, v in enumerate(pyon_data):

            if parameter in v:

                v = v.strip(' ,')
                list.append(self.data, v)

        return self.data


###########################################################################
    def dolog(self, output):

        if self.log_ON is True:

            with closing(open('log.txt', 'a')) as self.logfile:

                self.logfile.write(output + '\n')

