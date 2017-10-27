# Introduction

`libntprefimpl` enables easy interaction with NTP servers running the
[NTP Reference Implementation](http://www.ntp.org/), maintained by the 
[Network Time Foundation](https://nwtime.org/).

# Usage

## Server Configuration

### /etc/ntp.conf

```
keys /etc/ntp.keys
trustedkey 321
controlkey 321
requestkey 321

# Allow all types of operations/requests that original from localhost
restrict 127.0.0.1
restrict ::1

```

### /etc/ntp.keys

```
#
# PLEASE DO NOT USE THE DEFAULT VALUES HERE.
#
#Key Num   Key Type     Password
#-------   --------     --------
#65535     M            akey
#1         M            pass

321        M            md5password
```

## Code

```python
from __future__ import print_function
import libntprefimpl
import json

ntpServer = libntprefimpl.NtpReferenceImplementation(
  hostname='localhost' )

ntpServer.getAuthentication().setAuth(
  auth_type='md5',
  key_id=321,
  password='md5password' )

print( json.dumps(ntpServer.getStatistics().getHostStats(),
  sort_keys=True, indent=4) )
```

## Output

```json
{
    "hostname": "localhost",
    "statistics": {
        "host": {
            "kernel": {
                "calibration cycles": 0,
                "calibration errors": 0,
                "calibration interval": 0,
                "estimated error": 0.000707,
                "frequency tolerance": 500,
                "jitter exceeded": 0,
                "kernel status": "pll nano",
                "maximum error": 0.379496,
                "pll frequency": 0.240997,
                "pll offset": 0.453533,
                "pll time constant": 9,
                "pps frequency": 0,
                "pps jitter": 0,
                "pps stability": 0,
                "precision": 1e-06,
                "stability exceeded": 0
            },
            "packets": {
                "received": {
                    "IPv4": {
                        "count": 2060131,
                        "packets_per_second": 151
                    },
                    "IPv6": {
                        "count": 345290,
                        "packets_per_second": 25
                    },
                    "total": {
                        "count": 2405421,
                        "packets_per_second": 176
                    }
                },
                "sent": {
                    "IPv4": {
                        "count": 1057944,
                        "packets_per_second": 77
                    },
                    "IPv6": {
                        "count": 294389,
                        "packets_per_second": 21
                    },
                    "total": {
                        "count": 1352333,
                        "packets_per_second": 99
                    }
                }
            },
            "sysstat": {
                "KoD responses": 0,
                "authentication failed": 92,
                "bad length or format": 133,
                "current version": 1834459,
                "declined": 0,
                "older version": 570965,
                "packets received": 2405441,
                "processed for time": 373,
                "rate limited": 1053012,
                "restricted": 10,
                "sysstats reset": 13637,
                "uptime": 13637
            }
        },
        "interfaces": {
            "eth0": {
                "1.2.3.4:123": {
                    "drop": ".",
                    "failed": 0,
                    "flag": 19,
                    "ip_version": "IPv4",
                    "multicast": 0,
                    "peers": 5,
                    "received": 2060131,
                    "sent": 1057944,
                    "time_to_live": 0,
                    "uptime": 13637
                },
                "[1:2:3:4:5:6:7:8]:123": {
                    "drop": ".",
                    "failed": 0,
                    "flag": 11,
                    "ip_version": "IPv6",
                    "multicast": 0,
                    "peers": 2,
                    "received": 345290,
                    "sent": 294389,
                    "time_to_live": 0,
                    "uptime": 13637
                }
            },
            "lo": {
                "127.0.0.1:123": {
                    "drop": ".",
                    "failed": 0,
                    "flag": 5,
                    "ip_version": "IPv4",
                    "multicast": 0,
                    "peers": 0,
                    "received": 0,
                    "sent": 0,
                    "time_to_live": 0,
                    "uptime": 13637
                },
                "[::1]:123": {
                    "drop": ".",
                    "failed": 0,
                    "flag": 5,
                    "ip_version": "IPv6",
                    "multicast": 0,
                    "peers": 0,
                    "received": 0,
                    "sent": 0,
                    "time_to_live": 0,
                    "uptime": 13637
                }
            },
            "v4wildcard": {
                "0.0.0.0:123": {
                    "drop": "D",
                    "failed": 0,
                    "flag": 89,
                    "ip_version": "IPv4",
                    "multicast": 0,
                    "peers": 0,
                    "received": 0,
                    "sent": 0,
                    "time_to_live": 0,
                    "uptime": 13637
                }
            },
            "v6wildcard": {
                "[::]:123": {
                    "drop": "D",
                    "failed": 0,
                    "flag": 81,
                    "ip_version": "IPv6",
                    "multicast": 0,
                    "peers": 0,
                    "received": 0,
                    "sent": 0,
                    "time_to_live": 0,
                    "uptime": 13637
                }
            }
        }
    }
}
```

# Legal

`libntprefimpl` is copyrighted by [PublicNTP](https://publicntp.org), Inc., 
open-sourced under the [MIT License](https://en.wikipedia.org/wiki/MIT_License). 

Refer to 
[LICENSE](https://github.com/PublicNTP/libntprefimpl/blob/master/LICENSE) 
for more information.
