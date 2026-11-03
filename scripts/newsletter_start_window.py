"""Hold only early real production until the Korean 03:05 source-work window."""
import argparse
import datetime as dt
import time
from zoneinfo import ZoneInfo


def wait_for_source_start(dry_run, *, now=lambda: dt.datetime.now(dt.timezone.utc), sleep=time.sleep):
    if dry_run:
        return
    current=now().astimezone(ZoneInfo('Asia/Seoul'))
    target=current.replace(hour=3,minute=5,second=0,microsecond=0)
    while current < target:
        sleep(min(60,(target-current).total_seconds()))
        current=now().astimezone(ZoneInfo('Asia/Seoul'))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    wait_for_source_start(args.dry_run)
