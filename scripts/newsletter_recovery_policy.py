"""Distinguish a closed rollout gate from retryable production failures."""
import json
import sys
from pathlib import Path

KNOWN_BLOCK = 'Full server qualification is not yet successful with automatic recovery: completed/cancelled'


def qualification_only(workflow, payload, failure_log=''):
    if workflow != 'AP News server production' or not isinstance(payload, dict):
        return False
    jobs = payload.get('jobs')
    if not isinstance(jobs, list) or not jobs or payload.get('total_count') != len(jobs):
        return False
    if any(not isinstance(j, dict) or j.get('status') != 'completed' for j in jobs):
        return False
    failed = [j for j in jobs if j.get('conclusion') in ('failure', 'timed_out')]
    return (KNOWN_BLOCK in failure_log
            and len(failed) == 1 and failed[0].get('name') == 'qualification'
            and all(j is failed[0] or j.get('conclusion') == 'skipped' for j in jobs))


if __name__ == '__main__':
    try:
        blocked = qualification_only(sys.argv[1], json.load(sys.stdin), Path(sys.argv[2]).read_text())
    except (ValueError, TypeError, IndexError, OSError):
        blocked = False
    print('blocked=' + str(blocked).lower())
