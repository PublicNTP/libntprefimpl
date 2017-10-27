import sys
sys.path.append('..')
import argparse
import json
import libntprefimpl

def _parseArgs():
  parser = argparse.ArgumentParser(
    description="Pull stats from a Network Time Foundation NTP Reference Implementation server")

  parser.add_argument("hostname",
    help="Hostname or IP address of remote NTP server")
  parser.add_argument("stats_type",
    help="What kind of stats to pull", choices=['interface', 'host'])
  parser.add_argument("auth_type",
    help="The hash function for authentication", choices=['md5', 'sha', 'sha1'] )
  parser.add_argument("auth_key_id",
    help="Key ID to authenticate with remote NTP server",
    type=int )
  parser.add_argument("auth_password",
    help="Password we will use to authenticate with remote NTP server")

  return parser.parse_args()


if __name__ == "__main__":
  args = _parseArgs()
  ntpServer = libntprefimpl.NtpReferenceImplementation(args.hostname)
  ntpServer.getAuthentication().setAuth(args.auth_type, args.auth_key_id, args.auth_password)
  #print( statsObj )
  if args.stats_type == 'host':
    stats = ntpServer.getStatistics().getHostStats()
  else:
    stats = ntpServer.getStatistics().getInterfaceStats()

  print( json.dumps(stats, sort_keys=True, indent=4) )

