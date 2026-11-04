#!/usr/bin/env python3
"""Rebuild index.html from data/editions.json and data/sb.json.

Run from anywhere:  python3 energy-desk/tools/build.py
It (re)applies Ship & Bunker Singapore rows to every edition's price table,
then replaces the data block inside index.html (from 'var EDITIONS = ' to the RENDER marker).
"""
import json, datetime, pathlib, re
R = pathlib.Path(__file__).resolve().parent.parent
URL = 'https://shipandbunker.com/prices/apac/sea/sg-sin-singapore'
SB = sorted(json.load(open(R/'data/sb.json')), key=lambda r: r['d'], reverse=True)
E = json.load(open(R/'data/editions.json'))
MINE = ('VLSFO Singapore', 'HSFO Singapore', 'LSMGO / MGO Singapore')

def sb_rows(d):
    c = [x for x in SB if x['d'] <= d]
    if not c: return []
    r = max(c, key=lambda x: x['d'])
    dd = datetime.date.fromisoformat(r['d']).strftime('%-d %b %Y')
    carry = '' if r['d'] == d else ' Latest trading day before this edition.'
    def row(name, k, extra=''):
        x = r[k]
        return {'p': name, 'v': '$%s/mt' % format(x['p'], ',.2f'), 'd': dd, 's': 'Ship & Bunker', 'u': URL,
                'n': '%+.2f on the day, day range %s to %s across sources.%s%s' % (x['ch'], format(x['lo'], ',.0f'), format(x['hi'], ',.0f'), extra, carry)}
    return [row(MINE[0], 'vl'), row(MINE[1], 'hs', ' Scrubber spread %s (%+.1f).' % (format(r['sp'], '.0f'), r['spc'])), row(MINE[2], 'ls')]

for e in E:
    e['prices'] = [p for p in e['prices'] if p['p'] not in MINE and 'ENGINE' not in p['s']] + sb_rows(e['date'])
E.sort(key=lambda e: e['date'])
sbc = [dict(d=r['d'], vl=r['vl']['p'], vlc=r['vl']['ch'], hs=r['hs']['p'], hsc=r['hs']['ch'], ls=r['ls']['p'], lsc=r['ls']['ch'], sp=r['sp'], spc=r['spc']) for r in SB]
js = 'var EDITIONS = ' + json.dumps(E, ensure_ascii=False) + ';\nvar SB = ' + json.dumps(sbc) + ';\n'
p = R/'index.html'
h = p.read_text()
s = h.index('var EDITIONS = ')
e = h.index('/* ============ RENDER')
p.write_text(h[:s] + js + '\n' + h[e:])
print('built', len(E), 'editions, latest', E[-1]['date'], '| S&B rows', len(SB))
