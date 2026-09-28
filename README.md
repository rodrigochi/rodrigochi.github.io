# Personal website

The site is the single static page `index.html` with its files in `assets/`, served by GitHub Pages from the `main` branch. No build step is needed. The previous Wowchemy site lives in `legacy/` (served at https://rodrigochi.github.io/legacy/, not indexed by search engines) and, unchanged, in the `legacy` branch. `404.html` sends old URLs such as `/publication/...` to their `/legacy/` copies. `uploads/resume.pdf` stays at its old address because the new page links to it.

```bash
python -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765. The map reads its local JSON over HTTP.

## Editing content

The `T` object in `index.html` holds English/Spanish interface text, biography and research descriptions. `PAPERS` holds publications. After changing those, refresh the initial, JavaScript-free HTML with:

```bash
node scripts/render-static.mjs
```

This uses the same paper renderer as the browser. No packages or build framework are needed. Biography, publication links, research overview, background and contact remain readable without JavaScript; filtering, translation and interactive figures enhance the page when it is available.

## Colors and sharing

Theme tokens are at the beginning of the CSS. Keep the system-dark and explicit-dark blocks synchronized. The palette is cool: grey-blue paper, teal accent (`--seal`) and blue data color (`--trace`). Plot colors use their own diverging tokens, blue for negative and coral for positive values.

`assets/social-card.png` is the 1200 × 630 social preview. Regenerate it with `python3 scripts/make-social-card.py` (Pillow; fonts in `scripts/fonts/`). The canonical URL and social image URL assume the existing `https://rodrigochi.github.io/` domain; update both if deploying elsewhere.

## Visit statistics

This site also loads Google Analytics 4 (property `G-YWQTBECR75`, the same one the Wowchemy site used) in `<head>`. Both this site and Zupu (`~/website_zupu/index.html`) load GoatCounter just before `</body>` (account `rodrigochi`, dashboard at https://rodrigochi.goatcounter.com). It sets no cookies, so no consent banner is needed. Visits from `localhost` are not counted.
