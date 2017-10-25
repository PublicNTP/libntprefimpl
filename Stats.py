#!/usr/bin/python

from __future__ import print_function
import argparse
import pprint
import pexpect


class NTPRefImplServerStats:
  def __init__(self, hostname, auth_type, auth_key_id, auth_password ):
    self._hostname = hostname

    # Validate authentication type
    validAuthTypes = [ 'md5' ]
    if auth_type in validAuthTypes:
      self._auth = {}
      self._auth[auth_type] = { 'key_id': auth_key_id, 'password': auth_password } 
    else:
      raise RuntimeError("Invalid authentication type ({0}), known types: {1}".format(
        auth_type, pprint.pprint(validAuthTypes)))

  def __repr__(self):
    return "NTPRefImplServerStats(hostname={0}, auth={1})".format(
      self._hostname, pprint.pformat(self._auth))


  def getInterfaceStats(self):
    ntpqChild = pexpect.spawn("ntpq -c ifstats {0}".format(self._hostname))
    ntpqChild.expect("Keyid:")
    ntpqChild.sendline(str(self._auth['md5']['key_id']))
    ntpqChild.expect("MD5 Password:")
    ntpqChild.sendline(self._auth['md5']['password'])
    ntpqChild.expect(pexpect.EOF)

    return ntpqChild.before.decode('UTF-8')

    
     


def _parseArgs():
  parser = argparse.ArgumentParser(description="Pull stats from a Network Time Foundation NTP Reference Implementation server")

  parser.add_argument("hostname",       
    help="Hostname or IP address of remote NTP server")
  parser.add_argument("auth_md5_key_id",    
    help="MD5 key ID to authenticate with remote NTP server",
    type=int )
  parser.add_argument("auth_md5_password",  
    help="MD5 password we will use to authenticate with remote NTP server")

  return parser.parse_args()


if __name__ == "__main__":
  args = _parseArgs()
  statsObj = NTPRefImplServerStats(args.hostname, 'md5', args.auth_md5_key_id, args.auth_md5_password)
  #print( statsObj )
  stats = statsObj.getInterfaceStats()

  print( "Stats: {0}".format(stats))
