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
  parser.add_argument("auth_md5_key_id",
    help="MD5 key ID to authenticate with remote NTP server",
    type=int )
  parser.add_argument("auth_md5_password",
    help="MD5 password we will use to authenticate with remote NTP server")

  return parser.parse_args()


if __name__ == "__main__":
  args = _parseArgs()
  ntpServer = libntprefimpl.NtpReferenceImplementation(args.hostname)
  ntpServer.getAuthentication().setAuth('md5', args.auth_md5_key_id, args.auth_md5_password)
  #print( statsObj )
  if args.stats_type == 'host':
    stats = ntpServer.getStatistics().getHostStats()
  else:
    stats = ntpServer.getStatistics().getInterfaceStats()

  print( json.dumps(stats, sort_keys=True, indent=4) )

