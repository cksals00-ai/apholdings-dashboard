#!/usr/bin/env python3
"""Record verifiable publication milestones. No content generation or mail dispatch."""
import argparse
from datetime import date
import hashlib
import os
from pathlib import Path
import re

import newsletter_server as publisher

EVENTS={'handoff','waiting','started','deployed','published','error'}


def report_event(day,event,metadata=None):
    date.fromisoformat(day)
    if event not in EVENTS:
        raise ValueError('Unknown publication event')
    values=dict(metadata or {})
    run=os.environ.get('GITHUB_RUN_ID','')
    if re.fullmatch(r'\d+',run):
        values['workflow_url']=f'https://github.com/cksals00-ai/apholdings-dashboard/actions/runs/{run}'
    return publisher.database('POST','rpc/ap_news_record_publication',{
        'p_day':day,'p_event':event,'p_metadata':values})


def ready_metadata(path,day):
    import newsletter_handoff as handoff
    issue,_=handoff.validate_bundle(path,day)
    return {'title':issue['title'],'number':issue['number'],
            'bundle_filename':f'AP-News-{day}-ready.zip',
            'bundle_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('event',choices=sorted(EVENTS))
    parser.add_argument('--date',default=publisher.datetime.now(publisher.KST).date().isoformat())
    parser.add_argument('--error',default='')
    args=parser.parse_args()
    metadata={}
    if args.event=='handoff':
        import newsletter_handoff as handoff
        bundle=handoff.download_bundle(args.date)
        if bundle is None: raise ValueError('Ready bundle was not uploaded')
        metadata=ready_metadata(bundle,args.date)
    if args.event=='published':
        issue=publisher.builder.validate_issue(publisher.load_json(publisher.builder.ISSUES/f'{args.date}.json'))
        publisher.verify_public(issue)
        rows=publisher.database('GET','ap_news_issues?issue_date=eq.'+args.date+'&select=status,verified,source_data')
        if not rows or rows[0]['status']!='published' or rows[0]['verified'] is not True or rows[0]['source_data']!=issue:
            raise ValueError('Public edition registration has not been verified')
    if args.event=='error':
        metadata['last_error']=args.error or '서버 처리 오류: 실행 기록을 확인하세요.'
    result=report_event(args.date,args.event,metadata)
    print(f'Publication milestone recorded: {args.date} / {args.event}')


if __name__=='__main__': main()
