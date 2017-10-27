#!/usr/bin/python3


from __future__ import print_function
import pprint
import pexpect


class NtpReferenceImplementation_Statistics:
  """Collects statistics from an NTP Reference Implementation server.

  Used to retrieve detailed host/interface statistics from an 
  NTP reference implementation server.
  """


  def __init__(self, serverHostname, serverAuth):
    """Create new Statistics object

    Arguments:
    ----------
    serverHostname : str
      Name of the server these stats apply to
    serverAuth : :obj:`NtpReferenceImplementation_Authentication`
      Reference to object containing authentication information for the server 

    """
    self._serverHostname = serverHostname
    self._serverAuth = serverAuth


  def __repr__(self):
    """Generate string representation of this object, used for debugging.

    Returns:
    --------
    str 
      Format: "NTPRefImplStats(hostname=<hostname>)"
    
    """
    return "NTPRefImplStats(hostname={0})".format(
      self._serverHostname ) 


  def _parseInterfaceStatsString(self, statsString):
    """Parse multiline string with server stats into a dictionary.

    Arguments:
    ----------
    statsString : str
      Multiline string with detailed stats for each server interface

    Returns:
    --------
    dict 
      Key values are interface name, each entry is a dictionary
      with a key per interface address for the interface,
      and the value is detailed stats for that interface address

    """
    # Columns in a stats line
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
    """Retrieve detailed per-interface statistics.

    Returns:
    --------
    dict
      Keys are interface names, values are dictionaries of 
      interface address -> detailed stats
    
    """
    ntpqChild = pexpect.spawn( "ntpq -c ifstats {0}".format(self._serverHostname) )
    ntpqChild.expect("Keyid:")
    ntpqChild.sendline( str(self._serverAuth.getAuthKeyId() ) )
    ntpqChild.expect("MD5 Password:")
    ntpqChild.sendline( self._serverAuth.getAuthPassword() )
    ntpqChild.expect( pexpect.EOF )

    return self._parseInterfaceStatsString( ntpqChild.before.decode('UTF-8') )


  def getSysstat(self):
    """Get parsed results of a `ntpq -c sysstat` command. 
    
    Returns:
    --------
    dict
      Parsed results of `sysstat` command
    
    """
    ntpqChild = pexpect.spawn("ntpq -c sysstat {0}".format(self._serverHostname))
    ntpqChild.expect(pexpect.EOF)

    return self._createDictionary(ntpqChild.before.decode('UTF-8').splitlines())


  def getKernelInfo(self):
    """Get parsed results of an `ntpq -c kerninfo` command.

    Returns:
    --------
    dict
      Parsed results of `kerninfo` command

    """
    ntpqChild = pexpect.spawn("ntpq -c kerninfo {0}".format(self._serverHostname))
    ntpqChild.expect(pexpect.EOF)

    linesToParse = ntpqChild.before.decode('UTF-8').splitlines()[1:]

    # Fix calibration interval (string is missing a colon)
    for i in range(len(linesToParse)):
      if linesToParse[i].startswith("calibration interval") is True:
        linesToParse[i] = "calibration interval:{0}".format(
          linesToParse[i][len("calibration interval")+1:])
        #print( "after fix:\n{0}".format(linesToParse[i]))

    return self._createDictionary(linesToParse)


  def _createDictionary(self, colonDelineatedLines):
    """Parse multiple lines of colon-delimited statistics.

    Arguments:
    ----------
    colonDelineatedLines : :obj:`list` of :obj:`str`
      List of strings of type "description: value"

    Returns:
    --------
    dict
      Each row is parsed into a (key, value) pair, the key
      being on left hand side of the colon, the value on
      the right. Integers and floats are converted 
      properly.

    """ 
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
    """Retrieve all stats available for a host.

    Returns:
    --------
    dict
      Full dictionary of data that can be obtained
      for the server
    
    """
    hostStats = {
      'hostname': self._serverHostname,
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
