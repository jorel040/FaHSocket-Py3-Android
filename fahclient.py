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

###########################################################################
with Fahsocket(16, None, False, True, True, False) as s1:

    #!
    sendsize = s1.setsendbuffer(False, None)
    recvsize = s1.setrecvbuffer(False, None)

    s1.connect('localhost', 80)

    s1.send('ping')
    s1.recv(recvsize)

    s1.send('quit')
    s1.recv(recvsize)
    #!