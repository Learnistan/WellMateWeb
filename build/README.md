# Journey artwork generator

`gen.py` generates the `MINIS` and `SCENES` blocks inside `index.html` — the five
journey illustrations (Mazar carpet, Herat minarets, Afghan women's dress,
Kandahari ghara, pomegranate tree) and the small chip icons.

The art is procedural so the detail is real: carpet güls, Timurid tilework,
embroidery knot-grids and tree foliage are generated rather than hand-typed.
Every random draw is seeded, so output is byte-stable across runs.

## Regenerating

    python3 build/gen.py            # writes build/scenes.js and build/minis.js

Then splice those two blocks into `index.html`, replacing everything between
`/* ---------- mini icons for the selector chips ---------- */` and
`/* ---------- daily activities + bubbles game ... */`.

## How a scene animates

Each scene is one SVG at `viewBox="0 0 520 380"`. There are two mechanisms.

**Staged reveal** — groups carry `class="st"` and `data-at="<fraction>"`;
`updateGrow()` adds `.on` when `day/14 >= data-at` and CSS fades them in. Used
for things that simply appear (the chador, the birds, the pomegranate harvest).

**Continuous growth** — the `BUILD` table in `index.html` drives a clip rect per
scene, so the thing is genuinely *made* rather than revealed whole:

| journey | clip | what moves with it |
|---|---|---|
| `carpet` | `#weaveRect` grows **up** from the finished end (`y = 326 - h`) | `#shuttle`, the beater comb, rides the working edge |
| `minarets` | `#mrectA..D` grow up, each over its own stretch of the fortnight | `#mlineA..D`, the mason's plank, rides the top course |
| `dress`, `ghara` | `#sewRect` grows **down** from the shoulders | `#needle` rides the seam, stitches trailing behind |

The clip rects carry `data-base`/`data-top` (minarets) or `data-top`/`data-bot`
(garments), so `index.html` needs no hard-coded geometry except the carpet's
`326` / `254`. CSS transitions on `y`/`height` make the growth animate; they are
disabled under `prefers-reduced-motion`.

Sleeves are swept by `_sweep()` along a bowed centreline with a width taper, so
they are widest at the armhole and narrowest at the cuff, and the cuff band is
rotated square to the sleeve axis. Don't hand-tune sleeve beziers.
