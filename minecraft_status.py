#!/usr/bin/python
"""Simple Minecraft Status.

This is a simple library for querying Minecraft servers running
beta or later software. The 'poll' packet is used to return server MOTD
as well as current player count, and the server player limit.
"""
__author__ = 'Will Nowak <wan@ccs.neu.edu>'

import codecs
import logging
import socket
import sys

def ping(host, port, results = None):
  """Ping a port....."""
  try:
    socket.socket().connect((host, port))
    if results is not None:
      results.append(port)
    return True
  except:
    return False


def GetMCStatus(hostname, port=25565, timeout=0.5):
  """Query a minecraft beta server.

  Args:
     hostname: (String) hostname of the server to connect to
     port: (integer) port number to connect to
     timeout: (float) timeout in seconds for making a TCP connection

  Returns:
     list: If successful, something like:
           [True, 'MOTD here', 5, 20] # Online, MOTD, cur_players, max_players
           If unsuccessful, returns [False]
  """
  logging.debug('Trying to establish connection to %s:%d with timeout %f',
                hostname, port, timeout)
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname(hostname)
    if ping(ip, port):
        s.connect((ip, port))
        s.settimeout(timeout)
        s.send(chr(254))
        data, _ = s.recvfrom(2048)
        if data[0] == chr(255):
          data, _ = codecs.utf_16_be_decode(data[1:])
          data = data[1:]
          p = data.split(u'\xa7')
          return [True] + p
    else:
          return [False]
  except socket.error:
    logging.exception('Socket error when querying from %s', hostname)
  return [False]


if __name__ == '__main__':
  if len(sys.argv) == 2:
    print GetMCStatus(sys.argv[1])
  elif len(sys.argv) == 3:
    print GetMCStatus(sys.argv[1], int(sys.argv[2]))
  elif len(sys.argv) == 4:
    print GetMCStatus(sys.argv[1], int(sys.argv[2]), float(sys.argv[3]))
  else:
    print 'Usage: %s hostname [port] [timeout]' % sys.argv[0]
