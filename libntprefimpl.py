#!/usr/bin/python3

from __future__ import print_function
import libntprefimpl_Authentication
import libntprefimpl_Statistics


class NtpReferenceImplementation:
  """Top-level class representing an NTP reference implementation server.

  This class is an abstraction of an NTP server running the Network Time
  Foundation's reference implmentation.

  More Information:
  -----------------
  See https://nwtime.org/projects/ntp/ and http://www.ntp.org/
  """


  def __init__(self, hostname):
    """Constructor for an NTP reference implementation server.
    
    Parameters:
    -----------
      hostname : str 
        DNS hostname or IPv4/IPv6 address of the server

    """
    self._hostname  = hostname
    self._stats     = libntprefimpl_Statistics.NtpReferenceImplementation_Statistics(self)
    self._auth      = libntprefimpl_Authentication.NtpReferenceImplementation_Authentication(self)


  def getHostname(self):
    """Get the hostname for this server

    Returns:
    --------
    str
      hostname of the NTP server

    """
    return self._hostname


  def getStatistics(self):
    """Getter method for the server's statistics.

    Returns:
    --------
    NtpReferenceImplementation_Statistics
      Reference to object holding the collected statistics for this server

    """
    return self._stats


  def getAuthentication(self, authField=None):
    """Getter method for the server's authentication info.

    Returns:
    --------
    NtpReferenceImplementation_Authentication
      Reference to object holding authentication information for this server
 
    """
    return self._auth
