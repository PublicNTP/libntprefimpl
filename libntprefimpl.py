#!/usr/bin/python3

from __future__ import print_function
import argparse
import ntprefimpl_Authentication
import ntprefimpl_Statistics

class NtpReferenceImplementation:

  def __init__(self, hostname):
    self._hostname  = hostname
    self._stats     = ntprefimpl_Statistics.NtpReferenceImplementation_Statistics(self)
    self._auth      = ntprefimpl_Authentication.NtpReferenceImplementation_Authentication(self)

  def getHostname(self):
    return self._hostname

  def getStatistics(self):
    return self._stats

  def getAuthentication(self, authField=None):
    return self._auth
