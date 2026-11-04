#!/usr/bin/env python3
"""Sanity-check data/editions.json before publishing."""
import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent
E = json.load(open(R / 'data/editions.json'))
bad = []
dates = [e['date'] for e in E]
if len(set(dates)) != len(dates): bad.append('duplicate edition dates')
for e in E:
    for k in ('date', 'label', 'headline', 'prices', 'sections'):
        if k not in e: bad.append('%s missing %s' % (e.get('date'), k))
    for s in e.get('sections', []):
        for i in s['items']:
            for k in ('id', 't', 'n', 'src', 'd', 'c'):
                if not i.get(k): bad.append('%s/%s item %s missing %s' % (e['date'], s['name'], i.get('id'), k))
            if i.get('c') not in ('x', 's', 'c'): bad.append('%s item %s bad label' % (e['date'], i.get('id')))
            if 'ENGINE' in i['src'] and 'availability' not in i['src'] and i['n'] and any(ch in i['n'] for ch in '$') and False: pass
    for p in e.get('prices', []):
        if 'ENGINE' in p.get('s', ''): bad.append('%s price row from ENGINE: %s' % (e['date'], p['p']))
print('OK' if not bad else '\n'.join(bad))
sys.exit(1 if bad else 0)
