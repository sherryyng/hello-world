# Sherry Energy Desk: daily update routine

The desk is a single page, `index.html`, built from data in this folder.
The old chatgpt.site desk is frozen at 2 Nov 2026 and is no longer updated. Editions up to 2 Nov were
imported from it once and now live in `data/editions.json`. Do not read that site again.

## Each day
1. `python3 energy-desk/tools/refresh_sb.py` pulls Ship & Bunker's Singapore table into `data/sb.json`.
   If it exits with an error, keep the previous day's prices, say so in the edition, and tell the owner.
2. Search the web and news for the day's developments, per product: crude and macro, bunkers (VLSFO/LSFO,
   HSFO, LSMGO/MGO), B24/B30, B100/UCOME, methanol, ethanol, LPG, LNG, ammonia, gasoil, IMO regulation.
   Aim for the top five per product. If fewer than five are relevant, publish what is relevant and important.
   Sources can be anywhere: Maritime Executive, Manifold Times, Ship & Bunker, Reuters, Straits Times, CNA,
   Business Times, S&P Global, Argus, MPA, IMO and others.
3. Append one edition object to `data/editions.json` (copy the latest as a shape guide). Fields:
   `date`, `label`, `headline`, `pulse`, `prices[]`, `sections[]` (each with `items[]`), `watchNext[]`,
   `changes` (comparedWith, items[], limitations), `mgmt` (summary, priorities[], operations, timelines[],
   connections[], watchlist[], limitations, companyNews).
   Item fields: `id` (stable across days), `t`, `n`, `w` (why it matters), `src`, `u`, `d` (date), `c`.
4. `python3 energy-desk/tools/validate.py`, then `python3 energy-desk/tools/build.py`.
5. Publish `energy-desk/index.html` to the existing artifact URL (https://claude.ai/artifact/GvU3wU6nDDf4MRAiRggujM).
6. Commit `energy-desk/` to the working branch and push. Do not open a pull request.

## Rules
- Fact-check and cross-reference. Label every item: `x` cross-checked (two or more independent sources),
  `s` single source, `c` conflicting or weak. Show disagreeing figures side by side.
- Prices on the page are indicative public figures. Traders use Platts and MarketView. Only publish price rows from named, checkable sources; do not use tracker or aggregator sites (for example Farmbucks, Investing.com, Trading Economics, cbonds, relays of paywalled data).
- Never fill a gap with an estimate. A missing price or story is shown as not available.
- Singapore bunker prices come from Ship & Bunker only. Do not use ENGINE for price or volume figures.
  ENGINE may be cited for non-price facts such as lead times, labelled "availability only".
- Brent and other futures: use a settlement source (ICE via Reuters or an exchange page) when one is
  reachable. Otherwise say the level is approximate and name the source. ICE and Platts are not accessible
  from this environment and Platts is licensed, so do not publish Platts figures unless the owner supplies them.
- Reuse item ids for stories that continue, so "What changed" can show new, updated and carried items.
  Mark items carried from the previous day as "Carried" in `mgmt.priorities[].status`.
- No coverage note is shown on the page. Keep `mgmt.limitations` factual and short.
- Golden Island lens: state why an item matters to a product tanker owner-operator and physical fuel
  supplier. Assume no private fleet positions or charter terms. Flag items that name Golden Island.

## Notify the owner only when
- the Ship & Bunker refresh fails or its layout changes,
- VLSFO moves more than about $40/t in a day,
- Golden Island is named in the news,
- the IMO Net Zero Framework decision or another major regulation lands,
- the run could not complete.
Otherwise stay quiet.
