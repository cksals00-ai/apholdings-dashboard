#!/usr/bin/env python3
"""Transfer locally completed AP News to a draft release, without paid AI APIs."""
import argparse
from contextlib import contextmanager
from datetime import date, datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
import zipfile

import newsletter as builder
import newsletter_server as publisher

ROOT = builder.ROOT
REPO = 'cksals00-ai/apholdings-dashboard'
CHECKS = ('original_sources', 'all_pdf_pages', 'mobile_layout', 'image_loading')


def paths_for(issue):
    day = issue['date']
    return {f'site-source/newsletter/issues/{day}.json',
            f'ko/news/daily/{day}/index.html',
            f'newsletters/AP-News-{day}.pdf',
            f'newsletters/email/{day}.html',
            *(s['image']['path'].lstrip('/') for s in issue['stories']),
            *(issue['hero'][key].lstrip('/') for key in ('path','poster') if issue.get('layout')=='editorial-v2')}


@contextmanager
def document_root(root):
    previous = builder.ROOT, builder.ISSUES, publisher.ROOT
    builder.ROOT = publisher.ROOT = root
    builder.ISSUES = root / 'site-source/newsletter/issues'
    try:
        yield
    finally:
        builder.ROOT, builder.ISSUES, publisher.ROOT = previous


def create_bundle(day, output, reviewed=False):
    date.fromisoformat(day)
    if reviewed is not True:
        raise ValueError('Confirm original sources, every PDF page, mobile layout and images before handoff')
    issue = builder.validate_issue(publisher.load_json(builder.ISSUES / f'{day}.json'))
    if issue['status'] != 'published' or not issue.get('source_checked_at'):
        raise ValueError('Only a fully source-checked completed edition may be transferred')
    publisher.check_sources(issue, [])
    publisher.verify_documents(issue)
    files = {path: (ROOT / path).read_bytes() for path in paths_for(issue)}
    manifest = {'version': 1, 'date': day, 'number': issue['number'],
        'prepared_at': datetime.now(publisher.KST).isoformat(),
        'review': {'method': 'AI 작성 및 원문·지면 확인',
                   'checks': {key: True for key in CHECKS}},
        'files': {path: hashlib.sha256(data).hexdigest() for path, data in files.items()}}
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
        for path, data in sorted(files.items()):
            archive.writestr(path, data)
    validate_bundle(output, day)
    return output


def validate_bundle(path, day):
    date.fromisoformat(day)
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or sum(i.file_size for i in archive.infolist()) > 80_000_000:
            raise ValueError('Duplicate ZIP entries or oversized handoff')
        for name in names:
            part = PurePosixPath(name)
            if part.is_absolute() or '..' in part.parts or '\\' in name:
                raise ValueError('Unsafe handoff path')
        manifest = json.loads(archive.read('manifest.json'))
        if manifest.get('date') != day:
            raise ValueError('Handoff is not for the requested date')
        issue_path = f'site-source/newsletter/issues/{day}.json'
        issue = json.loads(archive.read(issue_path))
        if (manifest.get('version') != 1 or manifest.get('date') != day or
                issue.get('date') != day or manifest.get('number') != issue.get('number') or
                issue.get('status') != 'published' or issue.get('verified') is not True):
            raise ValueError('Edition date, number or source verification mismatch')
        checks = manifest.get('review', {}).get('checks', {})
        if any(checks.get(key) is not True for key in CHECKS):
            raise ValueError('Incomplete source/PDF/mobile review receipt')
        expected = paths_for(issue)
        if set(names) != expected | {'manifest.json'} or set(manifest.get('files', {})) != expected:
            raise ValueError('Unexpected or missing handoff files')
        files = {name: archive.read(name) for name in expected}
        for name, data in files.items():
            if hashlib.sha256(data).hexdigest() != manifest['files'][name]:
                raise ValueError('Handoff checksum mismatch')
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        for name, data in files.items():
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        with document_root(root):
            builder.validate_issue(issue)
            from PIL import Image, UnidentifiedImageError
            for story in issue['stories']:
                try:
                    with Image.open(root / story['image']['path'].lstrip('/')) as image:
                        image.verify()
                    with Image.open(root / story['image']['path'].lstrip('/')) as image:
                        image.load()
                        if min(image.size) < 320:
                            raise ValueError('Editorial image is too small')
                except (OSError, UnidentifiedImageError) as exc:
                    raise ValueError('Editorial image is corrupt') from exc
            publisher.check_sources(issue, [])
            publisher.verify_documents(issue)
            if files[f'ko/news/daily/{day}/index.html'].decode() != builder.render_issue(issue):
                raise ValueError('Completed web page does not match the source JSON')
            if files[f'newsletters/email/{day}.html'].decode() != builder.render_email(issue):
                raise ValueError('Completed email does not match the source JSON')
    return issue, files


def install_bundle(path, day, root):
    issue, files = validate_bundle(path, day)
    existing = root / f'site-source/newsletter/issues/{day}.json'
    if existing.exists():
        raise ValueError('Cannot replace an existing edition through handoff')
    previous = [publisher.load_json(p) for p in (root / 'site-source/newsletter/issues').glob('*.json')]
    if any(i['number'] == issue['number'] for i in previous):
        raise ValueError('Edition number already used')
    publisher.check_sources(issue, [s['url'] for i in previous for s in i.get('stories', [])])
    # All checks finish before writing. Only allowlisted completed files are installed.
    for name, data in files.items():
        destination = root / name
        if destination.exists() and destination.read_bytes() != data:
            raise ValueError('Prepared asset conflicts with an existing file')
    for name, data in files.items():
        destination = root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    with document_root(root):
        builder.build_all(render_documents=False, update_shared_pages=False)
        publisher.verify_documents(issue)
    return issue


def release_tag(day):
    date.fromisoformat(day)
    return 'ap-news-ready-' + day


def download_bundle(day):
    tag = release_tag(day)
    releases = json.loads(subprocess.check_output(['gh', 'api', f'repos/{REPO}/releases?per_page=100']))
    release = next((r for r in releases if r['tag_name'] == tag), None)
    if release is None:
        return None
    if not release['draft']:
        raise ValueError('Ready handoff must remain an authenticated draft release')
    name = f'AP-News-{day}-ready.zip'
    if not any(a['name'] == name for a in release.get('assets', [])):
        return None
    folder = publisher.STATE / day
    folder.mkdir(parents=True, exist_ok=True)
    subprocess.run(['gh', 'release', 'download', tag, '--repo', REPO, '--pattern', name,
                    '--dir', str(folder), '--clobber'], check=True)
    return folder / name


def upload_bundle(path, day):
    if path.name != f'AP-News-{day}-ready.zip':
        raise ValueError('Use canonical filename AP-News-YYYY-MM-DD-ready.zip')
    validate_bundle(path, day)
    tag = release_tag(day)
    releases = json.loads(subprocess.check_output(['gh', 'api', f'repos/{REPO}/releases?per_page=100']))
    release = next((r for r in releases if r['tag_name'] == tag), None)
    if release is None:
        subprocess.run(['gh', 'release', 'create', tag, '--repo', REPO, '--target', 'main',
                        '--draft', '--title', f'AP News ready {day}',
                        '--notes', 'Completed, source-checked web/PDF/email handoff. Server publication only; no paid AI API.'], check=True)
    elif not release['draft']:
        raise ValueError('Refusing to modify a public release')
    subprocess.run(['gh', 'release', 'upload', tag, str(path), '--repo', REPO, '--clobber'], check=True)
    print(f'Completed handoff uploaded for {day}; homepage and email unchanged')
    report_handoff(day)
    reserve_publication(day)


def reserve_publication(day):
    date.fromisoformat(day)
    subprocess.run(['gh','workflow','run','ap-news-daily.yml','--repo',REPO,
                    '-f','reserve_publication=true','-f',f'edition_date={day}'],check=True)
    print('Server publication reservation requested; waits until08:00 KST before publishing')


def report_handoff(day):
    date.fromisoformat(day)
    subprocess.run(['gh','workflow','run','ap-news-daily.yml','--repo',REPO,
                    '-f','record_handoff=true','-f',f'edition_date={day}'],check=True)
    print('Server receipt verification requested; admin status updates after server verification')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['package', 'upload', 'report', 'reserve'])
    parser.add_argument('--date', required=True)
    parser.add_argument('--file', type=Path)
    parser.add_argument('--reviewed', action='store_true', help='Assistant has checked originals, all PDF pages, mobile and images; does not mean human review')
    args = parser.parse_args()
    if args.stage not in ('report','reserve') and args.file is None: parser.error('--file is required for package/upload')
    if args.stage == 'package': create_bundle(args.date, args.file, args.reviewed)
    elif args.stage=='upload': upload_bundle(args.file, args.date)
    elif args.stage=='reserve': reserve_publication(args.date)
    else: report_handoff(args.date)


if __name__ == '__main__':
    main()
