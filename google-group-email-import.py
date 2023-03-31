#!/usr/bin/env python
import argparse
import mailbox
import sys

from google.oauth2 import service_account
from googleapiclient import discovery


def main():
    parser = argparse.ArgumentParser(
        description="%(prog)s is a utility to import email messagges from a mailbox\n"
        "in mbox format into a Google Group archive.",
        epilog="Notes:\n"
        "[1] The service account needs to be set up for domain-wide delegation.\n"
        "[2] The delegator account needs to have a Google Workspace admin role.\n"
        "\nAlso note that importing the same message (same Message-ID) multiple\n"
        "times will not result in duplicates.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--sa-creds",
        metavar="PATH",
        required=True,
        help="service account credentials JSON¹",
    )
    parser.add_argument(
        "--sa-delegator",
        metavar="EMAIL",
        required=True,
        help="the principal on whose behalf the\n        service account will act²",
    )
    parser.add_argument(
        "--src-mbox",
        metavar="PATH",
        required=True,
        help="source email archive in mbox format",
    )
    parser.add_argument(
        "--dst-group",
        metavar="EMAIL",
        required=True,
        help="destination group ID",
    )
    args = parser.parse_args()

    mbox = mailbox.mbox(args.src_mbox)

    credentials = service_account.Credentials.from_service_account_file(
        args.sa_creds,
        scopes=["https://www.googleapis.com/auth/apps.groups.migration"],
        subject=args.sa_delegator,
    )

    service = discovery.build("groupsmigration", "v1", credentials=credentials)
    archive = service.archive()

    for msg in mbox:

    req = archive.insert(
        groupId=args.dst_group,
        media_body=XXX,
        media_mime_type="message/rfc822",
    )
    res = req.execute()
    service.close()

    # try:
    #    response = request.execute()
    # except HttpError as e:
    #    print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    # print(json.dumps(response, sort_keys=True, indent=4))


if __name__ == "__main__":
    sys.exit(main())
