#!/usr/bin/env python
import argparse
import logging
import mailbox
import sys

from google.oauth2 import service_account
from googleapiclient import discovery
from multiprocessing import Process, Queue
from pathlib import Path
from time import time, sleep

logging.basicConfig(level=logging.INFO, format="%(asctime)-23s %(levelname)s %(message)s")

class RateLimiter:
    """Helper to rate-limit request"""

    def __init__(self, max_rate, interval):
        """Set class parameters"""
        self.hist = []
        self.max_rate = max_rate
        self.interval = interval

    def wait_for_clearance(self):
        """Wait if rate is too high, and then register time of new request"""
        now = time()
        while len(self.hist)/self.interval >= self.max_rate:
            self.hist = [t for t in self.hist if now - t <= self.interval]
            sleep(min(self.hist) + self.interval - now)
    
    def register(self):
        """Register time of new request"""
        self.hist.append(time())


def worker(work_q, feedback_q, group, creds, delegator):
    credentials = service_account.Credentials.from_service_account_file(
        creds,
        scopes=["https://www.googleapis.com/auth/apps.groups.migration"],
        subject=delegator,
    )
    service = discovery.build("groupsmigration", "v1", credentials=credentials)
    archive = service.archive()

    while True:
        msg_file = work_q.get()
        if msg_file is None:
            return
        req = archive.insert(
            groupId=args.dst_group,
            media_body=msg_file,
            media_mime_type="message/rfc822",
        )
        res = req.execute()
        feeback_q.put((msg_file, res))


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
    parser.add_argument(
        "--num-workers",
        metavar="NUM",
        default=8,
        help="number of workers",
    )
    parser.add_argument(
        "--work-dir",
        metavar="PATH",
        default="./workdir",
        help="storage for unpacked mailbox",
    )
    args = parser.parse_args()

    workdir = Path(args.work_dir)
    workdir.mkdir(exist_ok=True)
    if list(workdir.iterdir()):
        parser.exit(1, "Working directory not empty")

    mbox = mailbox.mbox(args.src_mbox)
    for key, msg in mbox.iteritems():
        msg_file = workdir / str(key)
        msg_file.write_text(str(msg))


    return
    credentials = service_account.Credentials.from_service_account_file(
        args.sa_creds,
        scopes=["https://www.googleapis.com/auth/apps.groups.migration"],
        subject=args.sa_delegator,
    )

    service = discovery.build("groupsmigration", "v1", credentials=credentials)
    archive = service.archive()

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
