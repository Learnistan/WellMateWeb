# WellMate — learnistan.af (final launch build)

The official showcase site for **WellMate**, the private, gentle wellbeing companion in
Pashto, Dari and English. Built to the WellMate Brand Book (warm earth palette, Fraunces +
Inter + Vazirmatn, *"Heard, without being seen."*) and matched to the real app.

Everything is in **`index.html`** — one self-contained file. No build step, no dependencies,
no server code. The `assets/` folders are placeholders for future art swaps.

---

## What's on the page (all interactive)

1. **Hero** — mood check-in exactly like the app (Calm · Good · Tired · Anxious · Sad);
   each mood gets a gentle response + a "Take a slow breath →" exercise; live phone mockup.
2. **Journeys** *(the centerpiece)* — the five real journeys, each **building day by day**:
   - **Mazar Carpet** (Care & Rebuilding) — weaves row by row on the loom, shuttle moving
   - **Minarets of Herat** (Rebuilding & Strength) — four minarets rise one by one
   - **Afghan Women's Dress** (Expression & Identity) — sewn piece by piece, needle & thread
   - **Kandahari Ghara** (Identity & Pride) — sewn, embroidered chest panel appearing
   - **Pomegranate Tree** (Growth & Patience) — seed → sprout → full fruiting tree
   Tend by button or tap the scene; each journey has a "Read about…" story.
3. **Daily Check-in + Mindful Games** — the app's real activity list with tappable check
   circles and a progress bar, plus a **playable Positive Bubbles** demo; Visualizing and
   Emotions Sorting shown as in-app cards.
4. **Talk to WellMate** — private chat demo with typewriter replies.
5. **Why WellMate** — the four brand pillars as a slim strip.
6. **Get WellMate** — **Google Play internal testing** (live link, invite-only) + App Store
   coming soon.
7. **Footer** — crisis-safety note; LEARNistan stated quietly (per brand architecture).

Fully trilingual (EN / دری / پښتو) with native RTL, Persian numerals, keyboard-accessible
interactions, `prefers-reduced-motion` support, and SEO (canonical + JSON-LD app schema).

---

## Launch on learnistan.af (~5 minutes)

`learnistan.af` is registered at 101domain but its **DNS is on Cloudflare**
(`mike.ns.cloudflare.com` / `leanna.ns.cloudflare.com`), so use Cloudflare Pages:

1. Cloudflare dashboard → **Workers & Pages → Create → Pages → Upload assets**.
2. Name the project (e.g. `wellmate`) and drag in this **`learnistan-wellmate`** folder
   (or just `index.html`). Deploy — you get a `*.pages.dev` preview URL.
3. Project → **Custom domains → Set up a custom domain** → `learnistan.af`.
   Cloudflare wires the DNS record automatically; HTTPS is automatic.
4. (Optional) add `www.learnistan.af` the same way.

**To update the site later:** re-upload `index.html` to the same Pages project.

Do **not** change the nameservers at 101domain — they already point to Cloudflare correctly.

---

## Post-launch checklist

- [ ] **Native-speaker review** of the Dari and Pashto strings (all copy lives in the
      `I18N` object in `index.html`, organized by `en` / `fa` / `ps`).
- [ ] **Crisis line** — replace the generic footer safety text with a real local helpline.
- [ ] **Store links** — when the Android app goes public, swap the internal-testing URL for
      the public Play Store URL (search `internaltest` in `index.html`); add the App Store
      link when iOS ships.
- [ ] **Exact art swap (optional)** — drop official journey illustrations into
      `assets/journeys/` and logo files into `assets/logo/`, then ask Claude to wire them in
      (current visuals are careful SVG recreations).
- [ ] **Character video** — `carecter 1.mp4` can be embedded (hero greeter or chat section).
- [ ] **Social preview image** — add an `og.png` (1200×630) and a
      `<meta property="og:image" …>` tag for richer link sharing.

---

## Editing quick-reference

- **All text** (3 languages): the `I18N` object near the top of `<script>`.
- **Journeys**: names/themes/stories in `I18N[lang].journeys`; scene art in `SCENES`;
  chip icons in `MINIS`; build thresholds are the `data-at` values inside each scene SVG.
- **Daily activities**: the `ACTIVITIES` array + `I18N[lang].acts`.
- **Bubbles game words**: `I18N[lang].gPos` / `gNeg`.
- **Colors**: CSS variables in `:root` (`--rose`, `--saffron`, `--terra`, `--plum`,
  `--cotton`, `--rosewater`, `--walnut`).

WellMate is a wellbeing companion, **not** a clinical service — the copy is written to the
brand's "words we never use" rules. Created within **LEARNistan** (LEARN family).
