#!/usr/bin/env python3
"""Fetch Ship & Bunker's Singapore conventional bunker table and merge it into data/sb.json.
Uses curl so the environment's proxy settings apply. Note: use 'shipandbunker.com' (no www).
Exits non-zero, without touching data/sb.json, if the table cannot be parsed (layout change or no access)."""
import re, html, json, subprocess, sys, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
URL = 'https://shipandbunker.com/prices/apac/sea/sg-sin-singapore'
raw = subprocess.run(['curl', '-sS', '-m', '40', '-L', URL], capture_output=True, text=True).stdout
raw = re.sub(r'<script.*?</script>|<style.*?</style>', '', raw, flags=re.S)
t = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', raw)))
i = t.find('Latest Prices (Conventional')
if i < 0: sys.exit('S&B table not found: no access or layout changed')
t = t[i:]
num = r'([\d,]+\.\d+)'
cell = num + r' ([▼▲▶]) ' + num + r' ' + num + r' – ' + num + r' \(' + num + r'\)'
pat = r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), (\w{3}) (\d+) \w{3} \d+ \w{3} ' + ' '.join([cell] * 4) + ' ' + num + r' ([▼▲▶]) ' + num
mons = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
f = lambda s: float(s.replace(',', ''))
import datetime
today = datetime.date.today()
rows = []
for m in re.finditer(pat, t):
    g = m.groups(); mo = mons[g[0]]; d = int(g[1])
    yr = today.year if mo <= today.month else today.year - 1
    c = lambda o: dict(p=f(g[o]), ch={'▲': 1, '▼': -1, '▶': 0}[g[o + 1]] * f(g[o + 2]), hi=f(g[o + 3]), lo=f(g[o + 4]))
    rows.append(dict(d='%d-%02d-%02d' % (yr, mo, d), vl=c(2), hs=c(8), ls=c(14), mg=c(20), sp=f(g[26]), spc={'▲': 1, '▼': -1, '▶': 0}[g[27]] * f(g[28])))
if len(rows) < 5: sys.exit('Parsed only %d rows: layout probably changed' % len(rows))
old = {r['d']: r for r in json.load(open(R / 'data/sb.json'))}
new = sum(1 for r in rows if r['d'] not in old)
for r in rows: old[r['d']] = r
json.dump(sorted(old.values(), key=lambda r: r['d'], reverse=True), open(R / 'data/sb.json', 'w'))
print('S&B rows fetched', len(rows), '| new dates', new, '| latest', max(r['d'] for r in rows))
