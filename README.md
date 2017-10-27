# Introduction

`libntprefimpl` enables easy interaction with NTP servers running the
[NTP Reference Implementation](http://www.ntp.org/), maintained by the 
[Network Time Foundation](https://nwtime.org/).

# Example Usage

```python
from __future__ import print_function
import libntprefimpl
import json

ntpServer = libntprefimpl.NtpReferenceImplementation(
  hostname="ntp1.someorganization")

ntpServer.getAuthentication().setAuth(
  auth_type='md5',
  key_id=1,
  password='md5password' )

print( json.dumps(ntpServer.getStatistics().getHostStats(),
  sort_keys=True, indent=4) )
```

# Licensing

`libntprefimpl` is licensed under the 
[MIT License](https://en.wikipedia.org/wiki/MIT_License). Refer to 
[LICENSE](https://github.com/PublicNTP/libntprefimpl/blob/master/LICENSE) 
for the full license text.
