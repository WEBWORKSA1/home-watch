# Home.Watch

Static website for **home.watch** — home watch matching, free tools, guides and self-updating live alerts for homes that sit empty. Built to run on the GitHub Pages free plan straight from the `main` branch.

## What's inside

| Path | Purpose |
|---|---|
| `index.html`, `*.html`, `guides/`, `regions/`, `tools/` | Generated pages (do not edit by hand — edit `content/` and rebuild) |
| `content/` | Guides, regional hubs, cities, tool markup and page copy |
| `scripts/build.py` | Generator: pages, sitemap, RSS feed, search index, robots, ads.txt |
| `scripts/update_data.py` | Daily data refresh: CPSC recalls, FEMA declarations, news headlines, MET Norway forecasts, YouTube video checks |
| `scripts/make_images.py` | Regenerates favicon, app icons and social image (needs Pillow) |
| `.github/workflows/refresh.yml` | Runs the refresh + rebuild every day at 09:17 UTC, on manual dispatch and when scripts/content change; commits only when something changed |
| `assets/js/config.js` | Optional payment links for the Support page and the FormSubmit private alias |
| `data/` | JSON data used by pages and tools |

## Build locally

```bash
python3 scripts/update_data.py   # optional: pull fresh data
python3 scripts/build.py         # regenerate every page
python3 -m http.server 8000      # preview at http://localhost:8000
```

Only the Python standard library is needed.

## Forms

All forms submit privately through FormSubmit's AJAX endpoint; the destination inbox is assembled at runtime and never appears on any page. The first submission triggers a one-time FormSubmit activation email — click **Activate** once. Optionally paste the private alias FormSubmit provides into `assets/js/config.js` (`formAlias`).

## Publishing on GitHub Pages

1. Settings → Pages → Build and deployment → **Deploy from a branch** → `main` / `(root)`.
2. Custom domain: add DNS at the registrar — `A` records for the apex to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, and a `CNAME` for `www` to `webworksa1.github.io` — then enter `home.watch` under Settings → Pages → Custom domain and tick **Enforce HTTPS**.

## Monetization

- Google AdSense Auto ads script in every page head; `ads.txt` at the root.
- Lead generation (`find-a-pro.html`), provider listings (`for-pros.html`), sponsorships (`advertise.html`), support pledges (`support.html`), monthly contest (`contests.html`) and talent applications (`careers.html`).

## Data credits

National Weather Service (live alerts and US forecasts), FEMA OpenFEMA, U.S. Consumer Product Safety Commission, MET Norway (CC BY 4.0), Google News RSS, YouTube.

© Home.Watch. All rights reserved. Not affiliated with any business, franchise or association using similar names — see `trademark.html`.
