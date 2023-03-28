#!/usr/bin/env python
import argparse
import sys
from pprint import pprint



from google.oauth2 import service_account
from googleapiclient import discovery


def main():
    parser = argparse.ArgumentParser(
            description="",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('args', nargs='*')
    args = parser.parse_args()
    pprint(args)

    SCOPES = ['https://www.googleapis.com/auth/apps.groups.migration']
    SERVICE_ACCOUNT_FILE = 'mailing-list-migration-381920-45ae46bb0e0e.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject='vbrik_gadm@icecube.wisc.edu')

    service = discovery.build('groupsmigration', 'v1', credentials=credentials)
    archive = service.archive()
    req = archive.insert(groupId='vbrik-test-group@icecube.wisc.edu',
                   media_body='msg', media_mime_type='message/rfc822')

    service.close()

    # try:
    #    response = request.execute()
    #except HttpError as e:
    #    print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    # print(json.dumps(response, sort_keys=True, indent=4))


if __name__ == '__main__':
    sys.exit(main())

