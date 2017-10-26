#!/usr/bin/python3

from __future__ import print_function
import pprint
import pexpect


class NtpReferenceImplementation_Statistics:

  def __init__(self, server):
    self._server = server

  def __repr__(self):
    return "NTPRefImplStats(hostname={0})".format(
      self._server.getHostname())


  def _parseInterfaceStatsString(self, statsString):
    tokenEntries = [
      'interface_number',
      'interface_name',
      'drop',
      'flag',
      'time_to_live',
      'multicast',
      'received',
      'sent',
      'failed',
      'peers',
      'uptime'
    ]

    #print( "Stats string:\n{0}".format(statsString) )

    # Break into array, one entry per line
    statLinesArray = statsString.splitlines()

    interfaces = {}
    filterTokens = [ 'interface_number', 'interface_name' ]
    stringTokens = [ 'drop' ]

    # Start iterating below header lines
    for i in range(4, len(statLinesArray), 2 ):
      statTokens = statLinesArray[i].split()
      interfaceAddress = statLinesArray[i+1].strip()

      #print( "Address: {0}\n\tTokens: {1}".format(interfaceAddress, pprint.pformat(statTokens)))
      parsedInterfaceTokens = {}

      for tokenIndex in range(len(tokenEntries)):
        parsedInterfaceTokens[tokenEntries[tokenIndex]] = statTokens[tokenIndex]

      #pprint.pprint(parsedInterfaceTokens)

      # Add to interfaces
      if parsedInterfaceTokens['interface_name'] not in interfaces:
        interfaces[ parsedInterfaceTokens['interface_name'] ] = {}

      interfaces[ parsedInterfaceTokens['interface_name'] ][ interfaceAddress ] = {}
      for interfaceToken in parsedInterfaceTokens.keys():
        if interfaceToken not in filterTokens:
          if interfaceToken not in stringTokens:
            parsedInterfaceTokens[interfaceToken] = int(parsedInterfaceTokens[interfaceToken])

          interfaces[ parsedInterfaceTokens['interface_name'] ][ interfaceAddress ][interfaceToken] = \
            parsedInterfaceTokens[interfaceToken]

      # If address has brackets, we have an IPv4 
      if interfaceAddress[0] == "[":
        ipVersion = 6
      else:
        ipVersion = 4

      interfaces[ parsedInterfaceTokens['interface_name'] ][ interfaceAddress ]['ip_version'] = \
        'IPv{0}'.format(ipVersion)

      # break

    #pprint.pprint(interfaces)

    return interfaces


  def getInterfaceStats(self):
    authInfo = self._server.getAuthentication().getAuth()

    ntpqChild = pexpect.spawn("ntpq -c ifstats {0}".format(self._server.getHostname()))
    ntpqChild.expect("Keyid:")
    ntpqChild.sendline(str(authInfo['keyId']))
    ntpqChild.expect("MD5 Password:")
    ntpqChild.sendline(authInfo['password'])
    ntpqChild.expect(pexpect.EOF)

    return self._parseInterfaceStatsString( ntpqChild.before.decode('UTF-8') )

  def getSysstat(self):
    ntpqChild = pexpect.spawn("ntpq -c sysstat {0}".format(self._hostname))
    ntpqChild.expect(pexpect.EOF)

    return self._createDictionary(ntpqChild.before.decode('UTF-8').splitlines())

  def getKernelInfo(self):
    ntpqChild = pexpect.spawn("ntpq -c kerninfo {0}".format(self._hostname))
    ntpqChild.expect(pexpect.EOF)

    linesToParse = ntpqChild.before.decode('UTF-8').splitlines()[1:]

    # Fix calibration interval, missing a colon
    for i in range(len(linesToParse)):
      if linesToParse[i].startswith("calibration interval") is True:
        linesToParse[i] = "calibration interval:{0}".format(
          linesToParse[i][len("calibration interval")+1:])
        #print( "after fix:\n{0}".format(linesToParse[i]))

    return self._createDictionary(linesToParse)


  def _createDictionary(self, colonDelineatedLines):

    returnDict = {}
    for currLine in colonDelineatedLines:
      #print( "processing {0}".format(currLine))
      (key, value) = currLine.split(':')
      returnDict[key] = value.strip()

      try:
        returnDict[key] = int(returnDict[key])
      except:
        try:
          returnDict[key] = float(returnDict[key])
        except:
          pass

    return returnDict


  def getHostStats(self):
    hostStats = {
      'hostname': self._hostname,
      'statistics': { 
        'interfaces': self.getInterfaceStats(), 
        'host': {
          'packets': { 
            'sent': { 
              'IPv4': {
                'count'               : 0,
                'packets_per_second'  : 0 
              },
              'IPv6': {
                'count'               : 0,
                'packets_per_second'  : 0
              },
              'total': {
                'count'               : 0,
                'packets_per_second'  : 0
              }
            }, 
            'received': { 
              'IPv4': {
                'count'               : 0,
                'packets_per_second'  : 0
              },
              'IPv6': {
                'count'               : 0,
                'packets_per_second'  : 0
              },
              'total': {
                'count'               : 0,
                'packets_per_second'  : 0
              }
            } 
          },
          'sysstat': self.getSysstat(),
          'kernel': self.getKernelInfo()
        }
      }
    }

    for interfaceName in hostStats['statistics']['interfaces']:
      for interfaceAddress in hostStats['statistics']['interfaces'][interfaceName]:
        currAddr = hostStats['statistics']['interfaces'][interfaceName][interfaceAddress]
        for trafficDirection in [ 'sent', 'received' ]:
          hostStats['statistics']['host']['packets'][trafficDirection][currAddr['ip_version']]['count'] += \
            currAddr[trafficDirection]
          hostStats['statistics']['host']['packets'][trafficDirection]['total']['count'] += \
            currAddr[trafficDirection]

    for trafficDirection in [ 'sent', 'received' ]:
      for ipVersion in [ 'IPv4', 'IPv6' ]:
        currStat = hostStats['statistics']['host']['packets'][trafficDirection][ipVersion]
        currStat['packets_per_second'] = int(currStat['count'] / 
          hostStats['statistics']['host']['sysstat']['uptime'])

      hostStats['statistics']['host']['packets'][trafficDirection]['total']['packets_per_second'] = int( 
         hostStats['statistics']['host']['packets'][trafficDirection]['total']['count'] / 
         hostStats['statistics']['host']['sysstat']['uptime'] )

    return hostStats
