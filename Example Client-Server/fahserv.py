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
from fahsocket import Fahsocket
import select
import sys

###########################################################################
with Fahsocket(16, None, False, True, True, False) as s1:

    sendsize = s1.setsendbuffer(False, None)
    recvsize = s1.setrecvbuffer(False, None)

    s1.bind('localhost', 80)
    s1.listen(3)

    conn1 = s1.accept()
    print('Sending: ACK: Connected!')
    s1.dolog('Sending: ACK: Connected!')
    conn1.send('ACK: Connected!'.encode('utf-8'))

    try:	
        while 1:
            rlist, wlist, elist = select.select([conn1.fileno()], [], [], 5)

            for conn in rlist:

                recvdata = conn1.recv(recvsize)
                recvdata = recvdata.decode('utf-8')

                if recvdata is '':

                    print('Client not sending data! Disconnecting!')
                    s1.dolog('Client not sending data! Disconnecting!')
                    sys.exit(1)

                if 'ping' in recvdata:

                    output = 'pong'
                    print('Received: ' + recvdata)
                    s1.dolog('Received: ' + recvdata)
                    print('Sending: ' + output)
                    s1.dolog('Sending: ' + output)
                    conn1.send(output.encode('utf-8'))

                elif 'quit' in recvdata:

                    output = 'goodbye'
                    print('Received: ' + recvdata)
                    s1.dolog('Received: ' + recvdata)
                    print('Sending: ' + output)
                    s1.dolog('Sending: ' + output)
                    conn1.send(output.encode('utf-8'))
                    sys.exit(0)

    except KeyboardInterrupt:

        sys.exit(2)