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


def planned_rehearsal_failure(payload):
    if not isinstance(payload,dict):return False
    jobs=payload.get('jobs')
    if not isinstance(jobs,list) or not jobs or payload.get('total_count')!=len(jobs):return False
    if any(not isinstance(j,dict) or j.get('status')!='completed' for j in jobs):return False
    failed=[j for j in jobs if j.get('conclusion') in ('failure','timed_out')]
    if len(failed)!=1 or failed[0].get('name')!='produce / produce':return False
    if any(j is not failed[0] and j.get('conclusion')!='skipped' for j in jobs):return False
    steps=failed[0].get('steps',[])
    return (any(x.get('name')=='Preserve source evidence and unfinished work in a private company draft release' and x.get('conclusion')=='success' for x in steps)
            and any(x.get('name')=='Inject first-attempt failure after saving validated test bundle' and x.get('conclusion')=='failure' for x in steps))


if __name__ == '__main__':
    try:
        payload=json.load(sys.stdin)
        blocked = qualification_only(sys.argv[1], payload, Path(sys.argv[2]).read_text())
        rehearsal_retry=planned_rehearsal_failure(payload)
    except (ValueError, TypeError, IndexError, OSError):
        blocked = False
        rehearsal_retry=False
    print('blocked=' + str(blocked).lower())

    print('rehearsal_retry_allowed=' + str(rehearsal_retry).lower())
