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

###########################################################################
with Fahsocket(16, 7, True, True, True, False) as s1:

    #!
    sendsize = s1.setsendbuffer(False, None)
    recvsize = s1.setrecvbuffer(False, None)

    s1.connect('10.0.0.10', 36330)

    s1.send('auth C86fR57f\n')
    s1.recv(recvsize)

    s1.send('updates add 0 5 $slot-info\n')
    s1.recv(recvsize)

    s1.send('updates add 1 5 $queue-info\n')
    s1.recv(recvsize)
    #!

    try:	
        while 1:
            socketdescr1 = s1.sock.fileno()
            rlist, wlist, elist = select.select([socketdescr1], [], [], 5)

            for socketdescr in rlist:

                #!
                recvdata = s1.recv(recvsize)
                id_tpf = s1.getparameter(recvdata, 'tpf')

                for i, v in enumerate(id_tpf):

                    print('id:' + str(i) + ' ' + v)
                    s1.dolog('id:' + str(i) + ' ' + v)
                #!

    except KeyboardInterrupt:

        #!
        s1.send('quit\n')
        s1.recv(recvsize)
        #!