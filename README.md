# google-groups-email-import

This script imports email messages from an mbox Mailbox into Google Groups
using Google [Group Migration API](https://googleapis.github.io/google-api-python-client/docs/dyn/groupsmigration_v1.html).

It requires [Google API Python Client](https://github.com/googleapis/google-api-python-client)
and [Google Auth Oauthlib](https://github.com/googleapis/google-auth-library-python-oauthlib/).

```
$ ./google-groups-email-import.py -h
usage: google-groups-email-import.py [-h] --sa-creds PATH --sa-delegator EMAIL 
                                     --src-mbox PATH --dst-group EMAIL [--work-dir PATH]
                                     [--resume] [--num-workers NUM] 
                                     [--log-level {debug,info,warning,error}]

google-groups-email-import.py is a utility to import email messagges from a mailbox
in mbox format into a Google Group archive.

options:
  -h, --help            show this help message and exit
  --sa-creds PATH       service account credentials JSON¹
  --sa-delegator EMAIL  the principal whome the service account
                                will impersonate²
  --src-mbox PATH       source email archive in mbox format
  --dst-group EMAIL     destination group ID
  --work-dir PATH       storage for unpacked mailbox (default: ./workdir)
  --resume              resume using previously unpacked mailbox
  --num-workers NUM     number of workers³ (default: 1)
  --log-level {debug,info,warning,error}
                        logging level (default: info)

Notes:
[1] The service account needs to be set up for domain-wide delegation.
[2] The delegator account needs to have a Google Workspace admin role.
[3] Officially, parallel insertions are not supported. However, sometimes
    using multiple workers results in significant peformance improvement.

Also note that importing the same message (same Message-ID) multiple
times will not result in duplicates.
