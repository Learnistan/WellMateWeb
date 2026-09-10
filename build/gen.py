# -*- coding: utf-8 -*-
"""Generates the SCENES + MINIS blocks for WellMate's journey artwork.
Deterministic: every random draw is seeded, so output is stable across runs."""
import random, math

def f(x):
    s = '%.1f' % x
    s = s.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s

def P(*xy):
    return ' '.join('%s %s' % (f(a), f(b)) for a, b in xy)

def lerp(a, b, t): return a + (b - a) * t

# ---------------------------------------------------------------- palettes
RED   = '#8E2C3B'; RED_D = '#6E1F2C'; RED_L = '#A5384A'
NAVY  = '#1E3348'; CREAM = '#EFDCB8'; OCHRE = '#C8893A'; IVORY = '#F6EBD6'
TEAL  = '#2E8F91'

# ================================================================= CARPET
def carpet():
    o = []
    x0, x1, yT, yB = 150, 370, 58, 326
    fx0, fx1, fy0, fy1 = x0 + 30, x1 - 30, yT + 30, yB - 30   # field rect

    o.append('<svg viewBox="0 0 520 380" preserveAspectRatio="xMidYMid slice">')
    o.append('<defs>')
    # --- workshop light
    o.append('<linearGradient id="cwall" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#F4EADA"/><stop offset="1" stop-color="#E6D8C0"/></linearGradient>')
    o.append('<linearGradient id="cbeam" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#C69C63"/><stop offset="0.45" stop-color="#A87C48"/>'
             '<stop offset="1" stop-color="#8A6238"/></linearGradient>')
    o.append('<linearGradient id="cpost" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#8A6238"/><stop offset="0.35" stop-color="#C69C63"/>'
             '<stop offset="0.7" stop-color="#A87C48"/><stop offset="1" stop-color="#7A5530"/></linearGradient>')
    # --- the woven field: one gul tile, repeated
    o.append('<pattern id="cfield" width="48" height="52" patternUnits="userSpaceOnUse" '
             'patternTransform="translate(%s %s)">' % (f(fx0), f(fy0)))
    o.append('<rect width="48" height="52" fill="%s"/>' % RED)
    # octagonal Turkmen gul, centred in the tile
    cx, cy, w, h = 24, 26, 40, 44
    oct_pts = [(cx-w/2, cy-h/5), (cx-w/5, cy-h/2), (cx+w/5, cy-h/2), (cx+w/2, cy-h/5),
               (cx+w/2, cy+h/5), (cx+w/5, cy+h/2), (cx-w/5, cy+h/2), (cx-w/2, cy+h/5)]
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.6"/>'
             % (' '.join('%s,%s' % (f(a), f(b)) for a, b in oct_pts), NAVY, CREAM))
    w2, h2 = w*0.6, h*0.6
    oct2 = [(cx-w2/2, cy-h2/5), (cx-w2/5, cy-h2/2), (cx+w2/5, cy-h2/2), (cx+w2/2, cy-h2/5),
            (cx+w2/2, cy+h2/5), (cx+w2/5, cy+h2/2), (cx-w2/5, cy+h2/2), (cx-w2/2, cy+h2/5)]
    o.append('<polygon points="%s" fill="%s"/>' % (' '.join('%s,%s' % (f(a), f(b)) for a, b in oct2), OCHRE))
    # quartering cross + hooked arms (the "elephant foot" interior)
    o.append('<path d="M%s V%s M%s H%s" stroke="%s" stroke-width="1.4"/>'
             % (P((cx, cy-h2/2)), f(cy+h2/2), P((cx-w2/2, cy)), f(cx+w2/2), NAVY))
    for sx in (-1, 1):
        for sy in (-1, 1):
            hx, hy = cx + sx*7.5, cy + sy*8.5
            o.append('<path d="M%s h%s v%s h%s" fill="none" stroke="%s" stroke-width="1.5" stroke-linecap="square"/>'
                     % (P((hx - sx*4, hy)), f(sx*4), f(sy*4), f(-sx*3), CREAM))
    o.append('<polygon points="%s" fill="%s"/>' % (
        ' '.join('%s,%s' % (f(a), f(b)) for a, b in
                 [(cx, cy-6), (cx+5, cy), (cx, cy+6), (cx-5, cy)]), CREAM))
    # interstitial star motifs at the tile corners
    for (sx, sy) in [(0, 0), (48, 0), (0, 52), (48, 52)]:
        o.append('<g transform="translate(%s %s)"><path d="M0 -6 L2 -2 L6 0 L2 2 L0 6 L-2 2 L-6 0 L-2 -2 Z" '
                 'fill="%s"/><circle r="1.6" fill="%s"/></g>' % (f(sx), f(sy), CREAM, OCHRE))
    o.append('</pattern>')

    # --- main border: repeating hooked diamond on ivory ground
    def guard(idn, a, b):
        return ('<pattern id="%s" width="7" height="7" patternUnits="userSpaceOnUse">'
                '<rect width="7" height="7" fill="%s"/>'
                '<path d="M0 3.5 L3.5 0 L7 3.5 L3.5 7 Z" fill="%s"/></pattern>' % (idn, a, b))
    o.append(guard('cg1', RED_D, CREAM))
    o.append('<pattern id="cborder" width="26" height="26" patternUnits="userSpaceOnUse">')
    o.append('<rect width="26" height="26" fill="%s"/>' % IVORY)
    o.append('<path d="M13 2 L24 13 L13 24 L2 13 Z" fill="none" stroke="%s" stroke-width="2"/>' % NAVY)
    o.append('<path d="M13 6.5 L19.5 13 L13 19.5 L6.5 13 Z" fill="%s"/>' % RED)
    o.append('<path d="M13 9.5 L16.5 13 L13 16.5 L9.5 13 Z" fill="%s"/>' % OCHRE)
    o.append('<path d="M2 13 h-2 M24 13 h2 M13 2 v-2 M13 24 v2" stroke="%s" stroke-width="2"/>' % NAVY)
    o.append('</pattern>')
    o.append('<clipPath id="weave"><rect id="weaveRect" x="150" y="316" width="220" height="10"/></clipPath>')
    o.append('</defs>')

    # ---- room
    o.append('<rect width="520" height="380" fill="url(#cwall)"/>')
    o.append('<rect y="338" width="520" height="42" fill="#D9C7A6"/>')
    o.append('<path d="M0 338 H520" stroke="#C6B08A" stroke-width="2"/>')
    # soft window light from the left
    o.append('<path d="M0 0 L150 0 L250 380 L0 380 Z" fill="#FFF8E8" opacity=".45"/>')

    # ---- loom frame
    o.append('<rect x="104" y="30" width="312" height="20" rx="6" fill="url(#cbeam)"/>')
    o.append('<rect x="104" y="34" width="312" height="4" fill="#D8B37B" opacity=".55"/>')
    o.append('<rect x="104" y="330" width="312" height="18" rx="6" fill="url(#cbeam)"/>')
    o.append('<rect x="122" y="26" width="20" height="322" rx="6" fill="url(#cpost)"/>')
    o.append('<rect x="378" y="26" width="20" height="322" rx="6" fill="url(#cpost)"/>')
    # peg detail
    for py in (70, 170, 270):
        o.append('<circle cx="132" cy="%d" r="3.4" fill="#6E4B29" opacity=".55"/>' % py)
        o.append('<circle cx="388" cy="%d" r="3.4" fill="#6E4B29" opacity=".55"/>' % py)

    # ---- warp threads (the undressed loom)
    warps = []
    for wx in range(154, 367, 8):
        warps.append('M%s %s V%s' % (f(wx), f(yT - 4), f(yB + 6)))
    o.append('<path d="%s" stroke="#EFE7D5" stroke-width="2.2"/>' % ' '.join(warps))
    o.append('<path d="%s" stroke="#FFFFFF" stroke-width="0.9" opacity=".8"/>' % ' '.join(warps))

    # ---- the carpet itself, revealed bottom-up by #weaveRect
    o.append('<g clip-path="url(#weave)">')
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>'
             % (f(x0), f(yT), f(x1-x0), f(yB-yT), RED))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#cg1)"/>'
             % (f(x0), f(yT), f(x1-x0), f(yB-yT)))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#cborder)"/>'
             % (f(x0+6), f(yT+6), f(x1-x0-12), f(yB-yT-12)))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>'
             % (f(fx0-4), f(fy0-4), f(fx1-fx0+8), f(fy1-fy0+8), NAVY))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#cfield)"/>'
             % (f(fx0), f(fy0), f(fx1-fx0), f(fy1-fy0)))
    # abrash — the natural dye-lot banding of a hand-dyed carpet
    rnd = random.Random(7)
    for by in range(int(fy0), int(fy1), 17):
        op = rnd.uniform(0.03, 0.10)
        col = '#000000' if rnd.random() > .5 else '#FFFFFF'
        o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" opacity="%s"/>'
                 % (f(fx0), f(by), f(fx1-fx0), f(rnd.uniform(7, 16)), col, f(op)))
    # knot texture: fine horizontal weft lines over everything
    lines = ['M%s %s H%s' % (f(x0), f(ly), f(x1)) for ly in range(int(yT), int(yB), 3)]
    o.append('<path d="%s" stroke="#000000" stroke-width="0.6" opacity=".07"/>' % ' '.join(lines))
    # kilim end + fringe at the bottom (woven first)
    o.append('<rect x="%s" y="%s" width="%s" height="10" fill="%s"/>' % (f(x0), f(yB-10), f(x1-x0), IVORY))
    o.append('<path d="%s" stroke="%s" stroke-width="1.6"/>'
             % (' '.join('M%s %s v10' % (f(kx), f(yB-10)) for kx in range(int(x0)+3, int(x1), 6)), RED_D))
    o.append('</g>')
    # fringe hangs below the finished end — appears once weaving is truly under way
    o.append('<g class="st" data-at="0.12"><path d="%s" stroke="#F2E8D4" stroke-width="2.2" stroke-linecap="round"/></g>'
             % ' '.join('M%s %s v%s' % (f(kx), f(yB), f(10 + (kx % 7) * 0.8)) for kx in range(int(x0)+3, int(x1), 5)))

    # ---- beater comb + shuttle, parked at the working edge (JS moves this group)
    o.append('<g id="shuttle">')
    o.append('<rect x="136" y="-7" width="248" height="11" rx="4" fill="#A9865A"/>')
    o.append('<rect x="136" y="-5" width="248" height="3" fill="#8A6A3F"/>')
    o.append('<path d="%s" stroke="#8A6A3F" stroke-width="1.6"/>'
             % ' '.join('M%d 4 v5' % tx for tx in range(142, 380, 7)))
    o.append('<g transform="translate(386 -2)"><ellipse rx="9" ry="5.5" fill="#3E5A52"/>'
             '<ellipse rx="5" ry="3" fill="#557A6E"/>'
             '<path d="M-8 2 q-16 8 -10 22" stroke="#3E5A52" stroke-width="1.8" fill="none"/></g>')
    o.append('</g>')

    # ---- a basket of yarn on the floor: warmth, always present
    o.append('<g transform="translate(64 330)">')
    o.append('<path d="M-30 0 h60 l-7 26 q-23 6 -46 0 z" fill="#C89A5E"/>')
    o.append('<path d="M-30 0 h60 l-2 6 q-28 7 -56 0 z" fill="#B0844A"/>')
    o.append('<path d="%s" stroke="#A9793F" stroke-width="1.2" opacity=".7"/>'
             % ' '.join('M%d 3 v22' % bx for bx in range(-24, 25, 7)))
    for (bx, by, r, c) in [(-14, -6, 11, '#A5384A'), (6, -8, 12, '#2E8F91'), (-2, -16, 9, '#C8893A')]:
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (bx, by, r, c))
        o.append('<path d="M%d %d a%d %d 0 0 1 %d %d" stroke="#FFFFFF" stroke-width="1.1" '
                 'fill="none" opacity=".35"/>' % (bx-r+2, by, r-2, r-2, (r-2)*1.4, -(r-3)))
    o.append('</g>')
    o.append('</svg>')
    return ''.join(o)

# ================================================================ MINARETS
SAND_D = '#B08652'; SAND = '#D9B784'; SAND_L = '#EAD0A6'; TURQ = '#4BA0A6'; TURQ_D = '#33818A'

def _arch(cx, y, w, h):
    return ('M%s %s V%s A%s %s 0 0 1 %s %s V%s Z'
            % (f(cx-w), f(y), f(y-h+w), f(w), f(w), f(cx+w), f(y-h+w), f(y)))

def _minaret(cx, baseY, topY, wb, wt, idn):
    """Returns (art, clipTop, halfWidthAtBase) — the art is meant to be clipped
    by a rect that rises from baseY, so the tower is laid course by course."""
    o = []
    span = baseY - topY
    def hw(y): return lerp(wt, wb, (y - topY) / span)

    o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#8A7048" opacity=".16"/>'
             % (f(cx + wb * .5), f(baseY + 3), f(wb * 2.0), f(wb * .38)))
    o.append('<rect x="%s" y="%s" width="%s" height="9" rx="1.5" fill="%s"/>'
             % (f(cx - wb * 1.65), f(baseY - 9), f(wb * 3.3), SAND_D))
    o.append('<rect x="%s" y="%s" width="%s" height="10" rx="1.5" fill="url(#mshaft)"/>'
             % (f(cx - wb * 1.42), f(baseY - 19), f(wb * 2.84)))
    o.append('<rect x="%s" y="%s" width="%s" height="2.5" fill="%s" opacity=".5"/>'
             % (f(cx - wb * 1.42), f(baseY - 19), f(wb * 2.84), SAND_L))

    shaft = [(cx-wb, baseY-19), (cx-wt, topY), (cx+wt, topY), (cx+wb, baseY-19)]
    pts = ' '.join('%s,%s' % (f(a), f(b)) for a, b in shaft)
    o.append('<clipPath id="%s"><polygon points="%s"/></clipPath>' % (idn, pts))
    o.append('<polygon points="%s" fill="url(#mshaft)"/>' % pts)
    o.append('<g clip-path="url(#%s)">' % idn)
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#mlat)"/>'
             % (f(cx-wb-2), f(topY), f(wb*2+4), f(span)))
    # the brick courses — this is what makes it read as masonry going up
    o.append('<g stroke="#9A7442" stroke-width="0.7" opacity=".38">%s</g>' % ''.join(
        '<path d="M%s %s H%s"/>' % (f(cx-wb-2), f(y), f(cx+wb+2))
        for y in range(int(topY), int(baseY-18), 6)))
    o.append('<g stroke="#F0DDBC" stroke-width="0.6" opacity=".3">%s</g>' % ''.join(
        '<path d="M%s %s H%s"/>' % (f(cx-wb-2), f(y+3), f(cx+wb+2))
        for y in range(int(topY), int(baseY-18), 12)))
    ay = baseY - 22
    for k in range(-2, 3):
        o.append('<path d="%s" fill="#7A5C36" opacity=".55"/>'
                 % _arch(cx + k * (wb * .58), ay, wb * .2, wb * .78))
    o.append('<rect x="%s" y="%s" width="%s" height="3" fill="%s" opacity=".5"/>'
             % (f(cx-wb-2), f(ay - wb*.92), f(wb*2+4), SAND_D))
    for frac, thick in ((0.12, 8), (0.42, 6.5), (0.72, 8)):
        by = lerp(baseY - 24, topY + 26, frac); h1 = hw(by) + 2.5
        o.append('<polygon points="%s" fill="%s"/>' % (
            ' '.join('%s,%s' % (f(a), f(b)) for a, b in
                     [(cx-h1, by), (cx+h1, by), (cx+h1, by-thick), (cx-h1, by-thick)]), TURQ))
        o.append('<polygon points="%s" fill="#BFEAEC" opacity=".5"/>' % (
            ' '.join('%s,%s' % (f(a), f(b)) for a, b in
                     [(cx-h1, by-thick*.62), (cx+h1, by-thick*.62),
                      (cx+h1, by-thick*.38), (cx-h1, by-thick*.38)])))
    for frac in (0.22, 0.44, 0.66):
        wy = lerp(baseY - 30, topY + 30, frac); ww = max(1.8, hw(wy) * .17)
        for sx in (-1, 1):
            o.append('<path d="%s" fill="#3E2C18"/>' % _arch(cx + sx*hw(wy)*.38, wy, ww, ww*3.4))
    o.append('</g>')
    o.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="1.1" opacity=".5"/>'
             % (pts, SAND_D))

    bw = wt * 1.9
    o.append('<polygon points="%s" fill="%s"/>' % (
        ' '.join('%s,%s' % (f(a), f(b)) for a, b in
                 [(cx-wt-1, topY+2), (cx-bw, topY-7), (cx+bw, topY-7), (cx+wt+1, topY+2)]), SAND_D))
    o.append('<rect x="%s" y="%s" width="%s" height="6" rx="1" fill="url(#mshaft)"/>'
             % (f(cx-bw), f(topY-13), f(bw*2)))
    o.append('<path d="%s" fill="#9A7442" opacity=".7"/>' % ''.join(
        'M%s %s l%s 4 l%s -4' % (f(cx-bw+i*(bw*2/6)), f(topY-7), f(bw/6), f(bw/6)) for i in range(6)))
    o.append('<rect x="%s" y="%s" width="%s" height="2" fill="%s" opacity=".6"/>'
             % (f(cx-bw), f(topY-13), f(bw*2), TURQ))

    dh = span * 0.20; dwb, dwt = wt*.82, wt*.68; dTop = topY - 13 - dh
    dpts = ' '.join('%s,%s' % (f(a), f(b)) for a, b in
                    [(cx-dwb, topY-13), (cx-dwt, dTop), (cx+dwt, dTop), (cx+dwb, topY-13)])
    o.append('<clipPath id="%sd"><polygon points="%s"/></clipPath>' % (idn, dpts))
    o.append('<polygon points="%s" fill="url(#mshaft)"/>' % dpts)
    o.append('<g clip-path="url(#%sd)"><rect x="%s" y="%s" width="%s" height="%s" fill="url(#mnet)"/>'
             % (idn, f(cx-dwb-2), f(dTop), f(dwb*2+4), f(dh+14)))
    o.append('<g stroke="#9A7442" stroke-width="0.6" opacity=".35">%s</g>' % ''.join(
        '<path d="M%s %s H%s"/>' % (f(cx-dwb-2), f(y), f(cx+dwb+2))
        for y in range(int(dTop), int(topY-13), 6)))
    o.append('<path d="%s" fill="#3E2C18"/></g>' % _arch(cx, topY-13-dh*.42, dwt*.26, dwt*.95))
    o.append('<rect x="%s" y="%s" width="%s" height="4" rx="1" fill="%s"/>'
             % (f(cx-dwt-1.5), f(dTop-4), f(dwt*2+3), SAND_D))
    o.append('<rect x="%s" y="%s" width="%s" height="1.6" fill="%s" opacity=".45"/>'
             % (f(cx-dwt-1.5), f(dTop-4), f(dwt*2+3), SAND_L))
    return ''.join(o), dTop - 6, wb * 1.7

def _cloud(cx, cy, s, op):
    return ('<g transform="translate(%s %s) scale(%s)" fill="#FFFFFF" opacity="%s">'
            '<ellipse cx="-26" cy="6" rx="26" ry="13"/><ellipse cx="4" cy="-6" rx="30" ry="20"/>'
            '<ellipse cx="30" cy="4" rx="24" ry="14"/><rect x="-50" y="6" width="82" height="12" rx="6"/>'
            '</g>' % (f(cx), f(cy), f(s), f(op)))

def minarets():
    o = []
    o.append('<svg viewBox="0 0 520 380" preserveAspectRatio="xMidYMid slice">')
    o.append('<defs>')
    o.append('<linearGradient id="msky" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#A8D8EC"/><stop offset="0.55" stop-color="#CDE8F5"/>'
             '<stop offset="1" stop-color="#EAF6FB"/></linearGradient>')
    o.append('<linearGradient id="mshaft" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#AD8250"/><stop offset="0.18" stop-color="#D2AE7C"/>'
             '<stop offset="0.44" stop-color="#EAD0A6"/><stop offset="0.72" stop-color="#D2AE7C"/>'
             '<stop offset="1" stop-color="#A87C4A"/></linearGradient>')
    o.append('<linearGradient id="mground" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#EFE0C4"/><stop offset="1" stop-color="#E0CBA2"/></linearGradient>')
    o.append('<pattern id="mlat" width="6.4" height="6.4" patternUnits="userSpaceOnUse">'
             '<path d="M0 3.2 L3.2 0 L6.4 3.2 L3.2 6.4 Z" fill="none" stroke="%s" '
             'stroke-width="0.7" opacity=".55"/>'
             '<rect x="2.35" y="2.35" width="1.7" height="1.7" fill="%s" opacity=".8" '
             'transform="rotate(45 3.2 3.2)"/></pattern>' % (TURQ_D, TURQ))
    o.append('<pattern id="mnet" width="4.6" height="4.6" patternUnits="userSpaceOnUse">'
             '<path d="M0 2.3 L2.3 0 L4.6 2.3 L2.3 4.6 Z" fill="none" stroke="%s" '
             'stroke-width="0.7" opacity=".7"/></pattern>' % TURQ)
    o.append('<pattern id="mgrit" width="26" height="19" patternUnits="userSpaceOnUse">'
             '<circle cx="4" cy="5" r="1.2" fill="#C4A97B" opacity=".55"/>'
             '<circle cx="17" cy="3" r="0.9" fill="#FFFFFF" opacity=".5"/>'
             '<circle cx="11" cy="12" r="1.4" fill="#C4A97B" opacity=".45"/>'
             '<circle cx="22" cy="15" r="1" fill="#FFFFFF" opacity=".45"/>'
             '<circle cx="2" cy="16" r="0.8" fill="#B79B6F" opacity=".4"/></pattern>')

    TOWERS = [(92, 330, 150, 24, 13, 'mA', 'A'), (206, 338, 108, 28, 15, 'mB', 'B'),
              (326, 334, 128, 27, 14.5, 'mC', 'C'), (442, 328, 162, 23, 12.5, 'mD', 'D')]
    art = []
    for cx, baseY, topY, wb, wt, idn, key in TOWERS:
        a, ctop, halfw = _minaret(cx, baseY, topY, wb, wt, idn)
        o.append('<clipPath id="mgrow%s"><rect id="mrect%s" x="%s" y="%s" width="%s" height="0" '
                 'data-base="%s" data-top="%s"/></clipPath>'
                 % (key, key, f(cx-halfw-6), f(baseY+8), f(halfw*2+12), f(baseY+8), f(ctop)))
        art.append((key, cx, baseY, halfw, a))
    o.append('</defs>')

    o.append('<rect width="520" height="380" fill="url(#msky)"/>')
    o.append('<circle cx="452" cy="46" r="76" fill="#FFF6DC" opacity=".55"/>')
    o.append('<circle cx="452" cy="46" r="34" fill="#FFFBEC" opacity=".8"/>')
    o.append(_cloud(96, 74, 1.0, .92)); o.append(_cloud(392, 112, 0.78, .8))
    o.append(_cloud(250, 52, 0.55, .6))
    o.append('<path d="M0 268 C36 240 70 234 104 248 C134 260 154 238 188 230 C226 221 250 246 284 256 '
             'C312 264 332 252 360 244 C398 233 424 248 456 258 C486 267 506 260 520 252 '
             'L520 300 L0 300 Z" fill="#B7CBDA" opacity=".5"/>')
    o.append('<path d="M0 284 C42 264 82 260 122 272 C160 283 192 264 232 258 C274 252 304 272 344 278 '
             'C384 284 418 268 454 264 C486 260 506 270 520 276 L520 300 L0 300 Z" '
             'fill="#C6D6E1" opacity=".6"/>')
    rnd = random.Random(21); bl=[]; bx=-10
    while bx < 530:
        bw_ = rnd.uniform(22, 46); bh = rnd.uniform(12, 30)
        bl.append('<rect x="%s" y="%s" width="%s" height="%s" rx="1.5"/>'
                  % (f(bx), f(300-bh), f(bw_), f(bh+4)))
        bx += bw_ + rnd.uniform(3, 12)
    o.append('<g fill="#DCC8A8" opacity=".45">%s</g>' % ''.join(bl))
    o.append('<rect y="298" width="520" height="82" fill="url(#mground)"/>')
    o.append('<path d="M0 298 H520" stroke="#D2BC93" stroke-width="2"/>')
    o.append('<rect y="298" width="520" height="82" fill="url(#mgrit)"/>')

    # each tower rises through its own clip; the mason's plank rides the top course
    for key, cx, baseY, halfw, a in art:
        o.append('<g clip-path="url(#mgrow%s)">%s</g>' % (key, a))
        o.append('<g id="mline%s" style="opacity:0">'
                 '<rect x="%s" y="-3" width="%s" height="3.4" rx="1.2" fill="#EFDCB8" opacity=".9"/>'
                 '<rect x="%s" y="-6.4" width="%s" height="4" rx="1.4" fill="#9A6E3C"/>'
                 '<rect x="%s" y="-6.4" width="%s" height="1.4" fill="#C69455"/>'
                 '<path d="M%s -2.4 v9 M%s -2.4 v9" stroke="#9A6E3C" stroke-width="2" '
                 'stroke-linecap="round"/>'
                 '<circle cx="%s" cy="-9.6" r="2.6" fill="#7E6A4A"/>'
                 '<path d="M%s -9.6 v11" stroke="#7E6A4A" stroke-width="1.1"/>'
                 '</g>'
                 % (key,
                    f(cx-halfw*.8), f(halfw*1.6),
                    f(cx-halfw*1.15), f(halfw*2.3),
                    f(cx-halfw*1.15), f(halfw*2.3),
                    f(cx-halfw*1.0), f(cx+halfw*1.0),
                    f(cx+halfw*1.05), f(cx+halfw*1.05)))
    o.append('<g class="st" data-at="0.96" fill="none" stroke="#6B7C89" stroke-width="1.8" '
             'stroke-linecap="round" opacity=".8">'
             '<path d="M56 96 q7 -6 13 0 q6 -6 13 0"/>'
             '<path d="M96 88 q5 -4.5 10 0 q5 -4.5 10 0"/>'
             '<path d="M150 126 q4 -3.5 8 0 q4 -3.5 8 0"/></g>')
    o.append('</svg>')
    return ''.join(o)


def _sweep(x0, y0, x1, y1, w0, w1, bow=0.0, n=12):
    """A tapering tube swept along a bowed centreline — used for sleeves, which
    must be widest at the armhole and narrowest at the cuff."""
    dx, dy = x1-x0, y1-y0
    L = math.hypot(dx, dy) or 1.0
    px, py = -dy/L, dx/L            # perpendicular
    c1 = (x0 + dx*0.33 + px*bow, y0 + dy*0.33 + py*bow)
    c2 = (x0 + dx*0.70 + px*bow*0.7, y0 + dy*0.70 + py*bow*0.7)
    pts=[]
    for i in range(n+1):
        pts.append(_cub((x0,y0), c1, c2, (x1,y1), i/n))
    left=[]; right=[]
    for i,(qx,qy) in enumerate(pts):
        if i < n: ax, ay = pts[i+1][0]-qx, pts[i+1][1]-qy
        else:     ax, ay = qx-pts[i-1][0], qy-pts[i-1][1]
        m = math.hypot(ax, ay) or 1.0
        nx, ny = -ay/m, ax/m
        h = lerp(w0, w1, i/n)/2
        left.append((qx+nx*h, qy+ny*h)); right.append((qx-nx*h, qy-ny*h))
    ring = left + right[::-1]
    d = 'M' + ' L'.join('%s %s' % (f(a), f(b)) for a, b in ring) + ' Z'
    ex, ey = pts[-1][0]-pts[-2][0], pts[-1][1]-pts[-2][1]
    return d, math.degrees(math.atan2(ex, -ey))   # cuff angle, from vertical

# =================================================================== DRESS
MAG='#BE2062'; MAG_D='#9A1650'; MAG_L='#D34C82'
DTEAL='#255A50'; DTEAL_D='#1B463E'; GOLD='#D9A62E'; GOLD_L='#F0CB63'
CRM='#F7EFDF'; PINKV='#F3C2CE'
DCX = 250

def _cub(p0,p1,p2,p3,t):
    mt=1-t
    return (mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0],
            mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1])

SL = [(222,116),(202,192),(160,264),(124,332)]
SR = [(2*DCX-x, y) for x, y in SL]
def _L(t): return _cub(*SL, t=t)
def _R(t): return _cub(*SR, t=t)
def _sag(t): return 24*t*t
def _ctrl(t):
    l,r=_L(t),_R(t)
    return ((l[0]+r[0])/2, (l[1]+r[1])/2 + _sag(t)*2)
def _cross(t, u):
    l,r,c=_L(t),_R(t),_ctrl(t); mt=1-u
    return (mt*mt*l[0]+2*mt*u*c[0]+u*u*r[0], mt*mt*l[1]+2*mt*u*c[1]+u*u*r[1])

def _band(t0, t1, fill):
    o=['M%s ' % P(_L(t0)), 'Q%s %s ' % (P(_ctrl(t0)), P(_R(t0)))]
    for i in range(1,9): o.append('L%s ' % P(_R(lerp(t0,t1,i/8))))
    o.append('Q%s %s ' % (P(_ctrl(t1)), P(_L(t1))))
    for i in range(1,9): o.append('L%s ' % P(_L(lerp(t1,t0,i/8))))
    o.append('Z')
    return '<path d="%s" fill="%s"/>' % (''.join(o), fill)

def _mirror(inner, cx):
    return '<g transform="translate(%s 0) scale(-1 1)">%s</g>' % (f(cx*2), inner)

def _needle(cx, thread, stitch):
    return ('<g id="needle" data-cx="%s" style="opacity:0">'
            '<path d="M-62 0 h50" stroke="%s" stroke-width="2.2" stroke-dasharray="5 4.5" '
            'stroke-linecap="round" opacity=".95"/>'
            '<path d="M0 1 l15 -23" stroke="#B9BFC6" stroke-width="2.8" stroke-linecap="round"/>'
            '<path d="M13 -19 l4 -6" stroke="#EDF0F3" stroke-width="2.8" stroke-linecap="round"/>'
            '<path d="M16 -26 a3.6 3.6 0 1 1 -3.4 -4.4" stroke="#9BA3AB" stroke-width="2" fill="none"/>'
            '<path d="M14 -28 C34 -38 40 -60 26 -72" stroke="%s" stroke-width="2" fill="none" '
            'opacity=".9"/></g>' % (f(cx), stitch, thread))

def dress():
    o=[]
    o.append('<svg viewBox="0 0 520 380" preserveAspectRatio="xMidYMid slice">')
    o.append('<defs>')
    o.append('<radialGradient id="dbg" cx="0.42" cy="0.32" r="0.86">'
             '<stop offset="0" stop-color="#FFFCF6"/><stop offset="1" stop-color="#EFE4D6"/></radialGradient>')
    o.append('<linearGradient id="dcloth" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#94134C"/><stop offset="0.2" stop-color="#BE2062"/>'
             '<stop offset="0.48" stop-color="#D23974"/><stop offset="0.78" stop-color="#BB1F60"/>'
             '<stop offset="1" stop-color="#8A1146"/></linearGradient>')
    o.append('<linearGradient id="dsleeve" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#9A1650"/><stop offset="0.55" stop-color="#C82A6C"/>'
             '<stop offset="1" stop-color="#A81A56"/></linearGradient>')
    o.append('<linearGradient id="dveil" x1="0.1" y1="0" x2="0.9" y2="1">'
             '<stop offset="0" stop-color="#F8D6DE" stop-opacity="0.5"/>'
             '<stop offset="0.5" stop-color="#F1BCCB" stop-opacity="0.36"/>'
             '<stop offset="1" stop-color="#F7CFDA" stop-opacity="0.46"/></linearGradient>')
    o.append('<linearGradient id="dpant" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#1B463E"/><stop offset="0.45" stop-color="#2E6B5E"/>'
             '<stop offset="1" stop-color="#1B463E"/></linearGradient>')
    o.append('<clipPath id="sew"><rect id="sewRect" x="0" y="44" width="520" height="0" '
             'data-top="44" data-bot="368"/></clipPath>')
    o.append('</defs>')
    o.append('<rect width="520" height="380" fill="url(#dbg)"/>')
    o.append('<ellipse cx="250" cy="356" rx="140" ry="14" fill="#C9B49F" opacity=".32"/>')

    o.append('<g clip-path="url(#sew)">')

    # --- skirt is laid first; the sleeves hang in front of it, as arms do
    # --- bodice
    o.append('<path d="M222 62 C228 55 238 51 250 51 C262 51 272 55 278 62 '
             'L280 119 C264 123 236 123 220 119 Z" fill="url(#dcloth)"/>')

    # --- skirt
    o.append('<path d="M%s C%s %s %s Q%s %s C%s %s %s Z" fill="url(#dcloth)"/>'
             % (P(SL[0]), P(SL[1]), P(SL[2]), P(SL[3]), P(_ctrl(1)), P(SR[3]),
                P(SR[2]), P(SR[1]), P(SR[0])))
    pl=[]; n=19
    for i in range(1,n):
        u=i/n
        p0=(lerp(224,276,u),117); p3=_cross(1.0,u)
        p1=(lerp(p0[0],p3[0],0.13), p0[1]+74); p2=(lerp(p0[0],p3[0],0.64), p3[1]-78)
        pl.append('<path d="M%s C%s %s %s" stroke="%s" stroke-width="%s" fill="none" opacity="%s"/>'
                  % (P(p0),P(p1),P(p2),P(p3), MAG_D if i%2 else MAG_L,
                     f(2.8 if i%2 else 1.9), '.30' if i%2 else '.20'))
    o.append(''.join(pl))

    # --- the embroidered yoke
    o.append('<path d="M224 60 C230 54 239 50 250 50 C261 50 270 54 276 60 L278 116 '
             'C264 120 236 120 222 116 Z" fill="#151C33"/>')
    cols=['#2E7D4F','#E0B33C','#C0392B','#2E6DA4','#F2E6C8','#7BBE6A']
    y=63; row=0
    while y < 114:
        h = 4.4 if row%2 else 6
        cs, cs2 = cols[row%len(cols)], cols[(row+3)%len(cols)]
        seg=[]; x=224
        while x < 276:
            if row % 3 == 0:
                seg.append('<path d="M%s %s l2.6 %s l2.6 -%s Z" fill="%s"/>'%(f(x),f(y+h),f(-h),f(h),cs))
                seg.append('<path d="M%s %s l2.6 %s l2.6 -%s Z" fill="%s"/>'%(f(x+5.2),f(y),f(h),f(h),cs2))
            elif row % 3 == 1:
                seg.append('<rect x="%s" y="%s" width="2.8" height="%s" fill="%s"/>'%(f(x),f(y),f(h),cs))
                seg.append('<rect x="%s" y="%s" width="2.8" height="%s" fill="%s"/>'%(f(x+3.6),f(y),f(h),cs2))
            else:
                seg.append('<path d="M%s %s l%s %s l-%s %s l-%s -%s Z" fill="%s"/>'
                           %(f(x+2.6),f(y),f(h*.5),f(h*.5),f(h*.5),f(h*.5),f(h*.5),f(h*.5),cs))
            x += 7 if row%3 else 10.4
        o.append(''.join(seg)); y += h + 2.2; row += 1
    o.append('<path d="M224 60 C230 54 239 50 250 50 C261 50 270 54 276 60 L278 116 '
             'C264 120 236 120 222 116 Z" fill="none" stroke="%s" stroke-width="2"/>' % GOLD_L)
    o.append('<path d="M243 50 C243 48 257 48 257 48 L255 72 C255 80 245 80 245 72 Z" fill="#F0DFC9"/>')
    o.append('<path d="M243 50 C243 48 257 48 257 48 L255 72 C255 80 245 80 245 72 Z" '
             'fill="none" stroke="%s" stroke-width="2"/>' % GOLD)

    # --- sleeves, in front of the skirt, with the cuff square to the sleeve
    sd, sang = _sweep(222, 76, 148, 206, 44, 34, bow=11)
    cuffx, cuffy = 148, 201
    cuff = ('<g transform="rotate(%s %s %s)">'
            '<rect x="%s" y="%s" width="38" height="9" fill="#151C33"/>'
            '<rect x="%s" y="%s" width="38" height="7" fill="%s"/>'
            '<rect x="%s" y="%s" width="38" height="8" fill="#151C33"/>'
            '<rect x="%s" y="%s" width="38" height="5" fill="%s"/>'
            '<polyline points="%s" fill="none" stroke="%s" stroke-width="1.5"/>'
            '%s</g>') % (
        f(sang), f(cuffx), f(cuffy),
        f(cuffx-19), f(cuffy-22), f(cuffx-19), f(cuffy-11.5), DTEAL,
        f(cuffx-19), f(cuffy-3), f(cuffx-19), f(cuffy+6.5), GOLD,
        ' '.join('%s,%s' % (f(cuffx-19+i*3.8), f(cuffy-21.5 if i%2 else cuffy-13.5)) for i in range(11)),
        CRM,
        ''.join('<path d="M%s %s l2.4 -2.6 l2.4 2.6 l-2.4 2.6 Z" fill="%s"/>'
                % (f(cuffx-19+i*4.8), f(cuffy+1), ['#2E7D4F','#E0B33C','#C0392B','#2E6DA4'][i%4])
                for i in range(8)))
    sleeve = ('<path d="%s" fill="url(#dsleeve)"/>'
              '<path d="M212 98 C193 130 172 164 156 194 M222 108 C204 138 186 170 171 198" '
              'stroke="#8E1146" stroke-width="1.7" fill="none" opacity=".3"/>') % sd
    o.append(sleeve); o.append(_mirror(sleeve, DCX))
    o.append(cuff);   o.append(_mirror(cuff, DCX))

    # --- hem: ikat, then the bands
    o.append('<g opacity=".92">%s</g>' % ''.join(
        '<g transform="translate(%s) scale(%s)" fill="none" stroke="#FBEFE6" stroke-width="2" '
        'stroke-linecap="round"><path d="M0 6 V-26"/><path d="M0 0 L-9 -7 M0 0 L9 -7"/>'
        '<path d="M0 -9 L-11 -17 M0 -9 L11 -17"/><path d="M0 -18 L-7 -24 M0 -18 L7 -24"/>'
        '<path d="M-9 -7 l-2 -4 M9 -7 l2 -4 M-11 -17 l-2 -4 M11 -17 l2 -4"/><path d="M-5 7 h10"/>'
        '<circle cx="0" cy="-29" r="2.4" fill="#FBEFE6" stroke="none"/></g>'
        % (P(_cross(0.70,(i+0.5)/12)), f(0.92+0.2*math.sin(((i+0.5)/12)*math.pi)))
        for i in range(12)))
    o.append(_band(0.795, 0.845, GOLD))
    o.append(_band(0.845, 0.955, DTEAL))
    o.append(_band(0.955, 1.0, GOLD))
    o.append(''.join('<g transform="translate(%s)"><path d="M0 -4.5 L4 0 L0 4.5 L-4 0 Z" '
                     'fill="#8A5E12" opacity=".75"/><circle r="1.3" fill="%s"/></g>'
                     % (P(_cross(0.82,(i+0.5)/19)), GOLD_L) for i in range(19)))
    o.append(''.join('<g transform="translate(%s) scale(0.78)" fill="%s">'
                     '<path d="M0 11 C-10 6 -13 -5 -6 -12 C-3 -16 3 -16 6 -12 C13 -5 10 6 0 11 Z"/>'
                     '<g stroke="%s" stroke-width="1" fill="none" opacity=".85">'
                     '<path d="M0 9 V-13"/><path d="M0 2 L-6 -6 M0 2 L6 -6"/>'
                     '<path d="M0 -5 L-4 -10 M0 -5 L4 -10"/></g></g>'
                     % (P(_cross(0.90,(i+0.5)/11)), GOLD, DTEAL_D) for i in range(11)))
    o.append('<path d="M%s Q%s %s" fill="none" stroke="#8A5E12" stroke-width="2" '
             'stroke-dasharray="4 3" opacity=".8"/>'
             % (P(_L(0.978)), P(_ctrl(0.978)), P(_R(0.978))))

    # --- tunban, revealed last because it sits lowest
    o.append('<path d="M216 300 C207 330 205 352 209 364 C220 372 242 372 250 364 '
             'C250 342 254 320 256 306 C258 320 262 342 262 364 C270 372 292 372 302 364 '
             'C306 352 304 330 295 300 Z" fill="url(#dpant)"/>')
    o.append('<path d="M209 362 q21 8 41 2 M262 364 q21 6 41 -2" stroke="#143830" '
             'stroke-width="3" fill="none" opacity=".8"/>')
    o.append('</g>')

    # --- the needle: it rides the seam, and the stitches trail behind it
    o.append(_needle(DCX, MAG, MAG_L))

    # --- the chador is draped last, over everything
    o.append('<g class="st" data-at="0.96">')
    o.append('<path d="M266 50 C312 60 344 118 352 192 C358 250 350 306 336 348 '
             'L288 342 C304 298 314 248 310 194 C304 130 288 80 258 60 Z" fill="url(#dveil)"/>')
    o.append('<path d="M272 56 C312 74 336 128 340 194 C343 246 336 296 324 340" '
             'stroke="#FBE4EA" stroke-width="2" fill="none" opacity=".7"/>')
    o.append('<g fill="%s" opacity=".8">%s</g>' % (PINKV, ''.join(
        '<circle cx="%s" cy="%s" r="3.4"/>' % (f(lerp(288,336,i/10)), f(lerp(342,348,i/10)))
        for i in range(11))))
    o.append('</g>')
    o.append('</svg>')
    return ''.join(o)

# =================================================================== GHARA
SAGE='#8FA8A4'; SAGE_D='#75908B'; SAGE_L='#A9BEBA'; PNL='#142824'; DOT='#EDF3F0'
GCX = 258

def ghara():
    o=[]
    o.append('<svg viewBox="0 0 520 380" preserveAspectRatio="xMidYMid slice">')
    o.append('<defs>')
    o.append('<radialGradient id="gbg" cx="0.44" cy="0.3" r="0.88">'
             '<stop offset="0" stop-color="#FBFCFB"/><stop offset="1" stop-color="#E2E9E7"/></radialGradient>')
    o.append('<linearGradient id="gcloth" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#6A8580"/><stop offset="0.2" stop-color="#8CA5A1"/>'
             '<stop offset="0.48" stop-color="#ACC2BE"/><stop offset="0.8" stop-color="#88A19D"/>'
             '<stop offset="1" stop-color="#64807B"/></linearGradient>')
    o.append('<linearGradient id="gsleeve" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#6E8985"/><stop offset="0.55" stop-color="#9FB6B2"/>'
             '<stop offset="1" stop-color="#7A948F"/></linearGradient>')
    o.append('<linearGradient id="gpant" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#64807B"/><stop offset="0.5" stop-color="#98B0AC"/>'
             '<stop offset="1" stop-color="#64807B"/></linearGradient>')
    o.append('<pattern id="gd1" width="4" height="4" patternUnits="userSpaceOnUse">'
             '<circle cx="2" cy="2" r="0.85" fill="%s"/></pattern>' % DOT)
    o.append('<pattern id="gd2" width="6" height="6" patternUnits="userSpaceOnUse">'
             '<circle cx="1.5" cy="1.5" r="1" fill="%s"/><circle cx="4.5" cy="4.5" r="1" fill="%s"/>'
             '</pattern>' % (DOT, DOT))
    o.append('<pattern id="gchk" width="7" height="7" patternUnits="userSpaceOnUse">'
             '<rect width="3.5" height="3.5" fill="%s" opacity=".9"/>'
             '<rect x="3.5" y="3.5" width="3.5" height="3.5" fill="%s" opacity=".9"/></pattern>' % (DOT, DOT))
    o.append('<clipPath id="sew"><rect id="sewRect" x="0" y="42" width="520" height="0" '
             'data-top="42" data-bot="350"/></clipPath>')
    o.append('</defs>')
    o.append('<rect width="520" height="380" fill="url(#gbg)"/>')
    o.append('<ellipse cx="258" cy="348" rx="126" ry="13" fill="#B4C3C0" opacity=".35"/>')

    o.append('<g clip-path="url(#sew)">')

    # --- sleeves, wide at the armhole and tapering to the cuff
    gsd, gsang = _sweep(214, 84, 166, 198, 54, 38, bow=10)
    gsleeve = ('<path d="%s" fill="url(#gsleeve)"/>'
               '<path d="M204 104 C190 136 176 166 168 190 M214 112 C201 142 188 172 181 194" '
               'stroke="%s" stroke-width="1.7" fill="none" opacity=".34"/>') % (gsd, SAGE_D)
    o.append(gsleeve)
    o.append('<g transform="translate(%s 0) scale(-1 1)">%s</g>' % (f(GCX*2), gsleeve))

    # --- perahan body: sloped shoulders, straight fall, rounded hem with vents
    o.append('<path d="M216 54 C234 45 282 45 300 54 '
             'C304 104 307 168 309 226 L310 254 '
             'C310 272 297 282 279 285 C266 288 250 288 237 285 '
             'C219 282 206 272 206 254 L207 226 C209 168 212 104 216 54 Z" fill="url(#gcloth)"/>')
    o.append('<path d="M244 46 C249 65 267 65 272 46 C263 43 253 43 244 46 Z" fill="#E2E9E7"/>')
    o.append('<g stroke="%s" stroke-width="1.9" fill="none" opacity=".32">'
             '<path d="M226 92 C221 146 219 208 221 276"/>'
             '<path d="M290 92 C295 146 297 208 295 276"/>'
             '<path d="M244 172 C242 206 241 244 242 282"/>'
             '<path d="M272 172 C274 206 275 244 274 282"/></g>' % SAGE_D)
    o.append('<g stroke="%s" stroke-width="1.5" fill="none" opacity=".4">'
             '<path d="M236 96 C231 150 230 210 232 280"/>'
             '<path d="M280 96 C285 150 286 210 284 280"/></g>' % SAGE_L)

    # --- the ghara panel
    px0, py0, px1, py1 = 224, 48, 292, 168
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>'
             % (px0, py0, px1-px0, py1-py0, PNL))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="1.7"/>'
             % (px0+3, py0+3, px1-px0-6, py1-py0-6, DOT))
    o.append('<rect x="%s" y="%s" width="%s" height="5" fill="url(#gchk)"/>' % (px0+4, py0+4, px1-px0-8))
    o.append('<rect x="%s" y="%s" width="%s" height="5" fill="url(#gchk)"/>' % (px0+4, py1-9, px1-px0-8))
    o.append('<rect x="%s" y="%s" width="5" height="%s" fill="url(#gchk)"/>' % (px0+4, py0+4, py1-py0-8))
    o.append('<rect x="%s" y="%s" width="5" height="%s" fill="url(#gchk)"/>' % (px1-9, py0+4, py1-py0-8))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="1.2" '
             'opacity=".8"/>' % (px0+11, py0+11, px1-px0-22, py1-py0-22, DOT))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#gd1)"/>'
             % (px0+14, py0+14, px1-px0-28, py1-py0-28))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="1.1"/>'
             % (px0+19, py0+19, px1-px0-38, py1-py0-38, DOT))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#0E1F1B"/>'
             % (px0+22, py0+22, px1-px0-44, py1-py0-44))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#gd2)"/>'
             % (px0+22, py0+22, px1-px0-44, py1-py0-44))
    o.append('<path d="M254 46 L254 100 Q258 105 262 100 L262 46 Z" fill="#0B1614"/>')
    o.append('<path d="M252.6 50 L252.6 98 M263.4 50 L263.4 98" stroke="%s" stroke-width="1" '
             'stroke-dasharray="2 2.6" opacity=".8"/>' % DOT)
    o.append('<circle cx="258" cy="150" r="2.4" fill="#B33A32"/>')

    # --- cuffs, square to the sleeve
    gcx, gcy = 166, 194
    cuff = ('<g transform="rotate(%s %s %s)">'
            '<rect x="%s" y="%s" width="40" height="34" fill="%s"/>'
            '<rect x="%s" y="%s" width="40" height="4" fill="url(#gchk)"/>'
            '<rect x="%s" y="%s" width="40" height="4" fill="url(#gchk)"/>'
            '<rect x="%s" y="%s" width="40" height="15" fill="url(#gd2)"/>'
            '<rect x="%s" y="%s" width="40" height="34" fill="none" stroke="%s" stroke-width="1.3"/>'
            '</g>') % (f(gsang), f(gcx), f(gcy),
                       f(gcx-20), f(gcy-17), PNL,
                       f(gcx-20), f(gcy-14), f(gcx-20), f(gcy+11),
                       f(gcx-20), f(gcy-8), f(gcx-20), f(gcy-17), DOT)
    o.append(cuff)
    o.append('<g transform="translate(%s 0) scale(-1 1)">%s</g>' % (f(GCX*2), cuff))

    # --- hem finishing, then the tunban below it
    o.append('<path d="M207 226 L206 258 M309 226 L310 258" stroke="#5A7671" stroke-width="2.6" '
             'stroke-linecap="round" opacity=".7"/>')
    o.append('<path d="M206 254 C210 274 227 284 239 286 C251 289 265 289 277 286 '
             'C289 284 306 274 310 254" fill="none" stroke="#5A7671" stroke-width="1.7" '
             'stroke-dasharray="4 3.4" opacity=".75"/>')
    o.append('<path d="M216 250 C207 284 205 320 210 342 C222 352 246 352 256 342 '
             'C256 316 258 288 259 272 C260 288 262 316 262 342 C273 352 297 352 308 342 '
             'C313 320 311 284 302 250 Z" fill="url(#gpant)"/>')
    o.append('<path d="M210 340 q24 9 46 2 M262 342 q24 7 46 -2" stroke="#5A7671" '
             'stroke-width="3.4" fill="none" opacity=".65"/>')
    o.append('</g>')

    o.append(_needle(GCX, '#142824', '#22403A'))
    o.append('</svg>')
    return ''.join(o)

# ============================================================= POMEGRANATE
BARK='#6E5137'; BARK_D='#4E3826'; BARK_L='#8E6E4C'
G_DARK=['#2C5430','#365F33','#3E6B39']
G_MID =['#477A40','#4F8446','#58914B']
G_LITE=['#68A557','#77B463','#8CB955']

def _limb(x, y, ang, length, w0, w1, curve, rnd, n=6):
    pts=[]; wid=[]; a=ang; cx, cy = x, y
    for i in range(n+1):
        pts.append((cx, cy)); wid.append(lerp(w0, w1, i/n))
        a += curve/n + rnd.uniform(-0.04, 0.04)
        cx += math.sin(a) * (length/n); cy -= math.cos(a) * (length/n)
    left=[]; right=[]
    for i,(qx,qy) in enumerate(pts):
        if i < n: dx, dy = pts[i+1][0]-qx, pts[i+1][1]-qy
        else:     dx, dy = qx-pts[i-1][0], qy-pts[i-1][1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy/L, dx/L; h = wid[i]/2
        left.append((qx+nx*h, qy+ny*h)); right.append((qx-nx*h, qy-ny*h))
    ring = left + right[::-1]
    d = 'M' + ' L'.join('%s %s' % (f(px), f(py)) for px, py in ring) + ' Z'
    mid = pts[len(pts)//2]
    return d, (cx, cy), a, mid

def _tree(seed):
    """Constrained growth: limbs arc back toward vertical, so the tree opens
    into a vase the way an orchard pomegranate does instead of splaying."""
    rnd = random.Random(seed)
    limbs=[]; tips=[]; mids=[]
    def grow(x, y, ang, length, w, depth):
        ang = max(-1.15, min(1.15, ang))
        curve = -ang * 0.40 + rnd.uniform(-0.18, 0.18)
        d, end, a2, mid = _limb(x, y, ang, length, w, w*0.56, curve, rnd)
        limbs.append((d, depth))
        if depth >= 2:
            mids.append((mid[0], mid[1], w)); mids.append((end[0], end[1], w))
        if depth >= 3:
            tips.append((end[0], end[1], w)); return
        k = 3 if depth == 1 else rnd.choice([2, 2, 3])
        spread = [0.56, -0.01, -0.55] if k == 3 else [0.47, -0.45]
        for sp in spread:
            grow(end[0], end[1], a2 + sp + rnd.uniform(-0.13, 0.13),
                 length * rnd.uniform(0.70, 0.84), w * 0.58, depth + 1)
    d, end, a2, mid = _limb(246, 344, 0.0, 74, 30, 17, 0.03, rnd, 5)
    limbs.append((d, 0))
    for sp, ln, wd in ((-0.70, 90, 15), (-0.24, 100, 16), (0.24, 100, 16), (0.70, 90, 15)):
        grow(end[0], end[1], a2 + sp, ln, wd, 1)
    return limbs, tips, mids

def _pick_seed():
    """Choose the seed whose canopy sits best in the frame — deterministic."""
    best=None
    for sd in range(1, 500):
        limbs, tips, mids = _tree(sd)
        xs=[t[0] for t in tips]; ys=[t[1] for t in tips]
        if not xs: continue
        lo, hi, top, bot = min(xs), max(xs), min(ys), max(ys)
        if lo < 66 or hi > 428 or top < 84 or top > 132 or bot > 268: continue
        width = hi - lo
        if width < 250: continue
        cxm = sum(xs)/len(xs)
        left = sum(1 for x in xs if x < 246); right = len(xs)-left
        score = (abs(cxm-246)*3.0 + abs(left-right)*6.0
                 + abs(width-310)*0.5 + abs(top-104)*1.2)
        if best is None or score < best[0]: best=(score, sd)
    return best[1] if best else 91

def _ring(cx, cy, rnd, count, r, cols):
    out=[]
    for i in range(count):
        a = (i/count)*math.pi*2 + rnd.uniform(-0.35, 0.35)
        rr = r * rnd.uniform(0.82, 1.16)
        lx, ly = cx + math.cos(a)*rr, cy + math.sin(a)*rr*0.84
        L = rnd.uniform(5.4, 8.2); W = L * rnd.uniform(0.30, 0.40)
        rot = math.degrees(a) + rnd.uniform(-40, 40)
        out.append('<ellipse cx="%d" cy="%d" rx="%s" ry="%s" fill="%s" transform="rotate(%d %d %d)"/>'
                   % (round(lx), round(ly), f(L), f(W), rnd.choice(cols),
                      round(rot), round(lx), round(ly)))
    return ''.join(out)

def _clump(cx, cy, rnd, count, spread, cols, sq=0.86, lo=4.6, hi=7.6):
    out=[]
    for _ in range(count):
        a = rnd.uniform(0, math.pi*2); r = rnd.uniform(0, 1)**0.62 * spread
        lx, ly = cx + math.cos(a)*r, cy + math.sin(a)*r*sq
        L = rnd.uniform(lo, hi); W = L * rnd.uniform(0.30, 0.40)
        rot = rnd.uniform(-90, 90)
        out.append('<ellipse cx="%d" cy="%d" rx="%s" ry="%s" fill="%s" transform="rotate(%d %d %d)"/>'
                   % (round(lx), round(ly), f(L), f(W), rnd.choice(cols), round(rot), round(lx), round(ly)))
    return ''.join(out)

def _fruit(cx, cy, r, ripe=True):
    if not ripe:
        return ('<circle cx="%s" cy="%s" r="%s" fill="#A6BB70"/>'
                '<path d="M%s %s a%s %s 0 0 0 %s 0 Z" fill="#C08A4A" opacity=".4"/>'
                '<path d="M%s %s l1.6 -4 l1.6 4 Z" fill="#6B8A4E"/>'
                % (f(cx), f(cy), f(r), f(cx-r), f(cy), f(r), f(r), f(r*2),
                   f(cx-1.6), f(cy+r*0.95)))
    crown = ('<path d="M%s %s L%s %s L%s %s L%s %s L%s %s L%s %s L%s %s Z" fill="#8E2230"/>'
             % (f(cx-r*.30), f(cy+r*.66), f(cx-r*.36), f(cy+r*1.20), f(cx-r*.12), f(cy+r*.92),
                f(cx), f(cy+r*1.32), f(cx+r*.12), f(cy+r*.92), f(cx+r*.36), f(cy+r*1.20),
                f(cx+r*.30), f(cy+r*.66)))
    return ('<path d="M%s %s l1.4 -%s" stroke="#6E4F32" stroke-width="2" stroke-linecap="round"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="url(#pfruit)"/>'
            '<path d="M%s %s a%s %s 0 0 0 %s 0" fill="none" stroke="#7E1B26" stroke-width="1" opacity=".3"/>'
            % (f(cx), f(cy-r*.90), f(r*.6), f(cx), f(cy), f(r),
               f(cx-r*.7), f(cy+r*.2), f(r*.8), f(r*.9), f(r*1.4))
            ) + crown + ('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#FFFFFF" opacity=".3" '
                         'transform="rotate(-28 %s %s)"/>'
                         % (f(cx-r*.33), f(cy-r*.34), f(r*.30), f(r*.17), f(cx-r*.33), f(cy-r*.34)))

def pomegranate():
    rnd = random.Random(2024)
    o=[]
    o.append('<svg viewBox="0 0 520 380" preserveAspectRatio="xMidYMid slice">')
    o.append('<defs>')
    o.append('<linearGradient id="psky" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#F2DDB8"/><stop offset="0.45" stop-color="#FAECD2"/>'
             '<stop offset="1" stop-color="#FDF6E6"/></linearGradient>')
    o.append('<linearGradient id="pearth" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#E0C89E"/><stop offset="1" stop-color="#C9AB7B"/></linearGradient>')
    o.append('<radialGradient id="pfruit" cx="0.36" cy="0.3" r="0.8">'
             '<stop offset="0" stop-color="#E4634A"/><stop offset="0.42" stop-color="#C63A32"/>'
             '<stop offset="1" stop-color="#8E1F2A"/></radialGradient>')
    o.append('<radialGradient id="paril" cx="0.35" cy="0.3" r="0.8">'
             '<stop offset="0" stop-color="#F0576E"/><stop offset="1" stop-color="#B4102F"/></radialGradient>')
    o.append('<linearGradient id="ptrunk" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#4E3826"/><stop offset="0.38" stop-color="#7A5B3E"/>'
             '<stop offset="0.68" stop-color="#8E6E4C"/><stop offset="1" stop-color="#513A27"/></linearGradient>')
    o.append('<pattern id="pgrit" width="24" height="18" patternUnits="userSpaceOnUse">'
             '<ellipse cx="5" cy="4" rx="2.6" ry="1.3" fill="#B99A6C" opacity=".38"/>'
             '<ellipse cx="16" cy="9" rx="1.8" ry="1" fill="#B99A6C" opacity=".32"/>'
             '<ellipse cx="9" cy="14" rx="2.2" ry="1.1" fill="#C9AC80" opacity=".42"/>'
             '<ellipse cx="21" cy="2" rx="1.4" ry="0.8" fill="#B99A6C" opacity=".28"/></pattern>')
    o.append('</defs>')
    o.append('<rect width="520" height="380" fill="url(#psky)"/>')
    o.append('<circle cx="440" cy="62" r="92" fill="#FFF3D6" opacity=".5"/>')
    o.append('<circle cx="440" cy="62" r="40" fill="#FFFAEA" opacity=".85"/>')
    # rolling dry ranges, not pyramids
    o.append('<path d="M0 262 C34 232 64 224 96 238 C124 250 142 228 176 220 C214 211 236 236 268 246 '
             'C296 255 316 244 344 236 C382 225 408 240 440 250 C472 260 498 252 520 244 L520 300 L0 300 Z" '
             'fill="#CDB495" opacity=".5"/>')
    o.append('<path d="M0 278 C40 258 78 254 118 266 C156 277 188 258 228 252 C270 246 300 266 340 272 '
             'C380 278 414 262 450 258 C482 254 504 264 520 270 L520 300 L0 300 Z" '
             'fill="#D9C3A4" opacity=".62"/>')
    # orchard rows, varied
    for (ox, oy, s, tone) in [(38,272,1.0,'#41693B'),(88,268,.8,'#4C7644'),(132,273,.62,'#3E6238'),
                              (176,269,.5,'#4C7644'),(372,270,.72,'#41693B'),(414,274,.92,'#4C7644'),
                              (466,268,.6,'#3E6238'),(498,272,.8,'#456F3E')]:
        r2=random.Random(int(ox))
        o.append('<g transform="translate(%s %s) scale(%s)" opacity=".8">'
                 '<rect x="-2.2" y="-2" width="4.4" height="16" fill="#6E5137"/>'
                 '<ellipse cx="%s" cy="-12" rx="%s" ry="%s" fill="%s"/>'
                 '<ellipse cx="%s" cy="-6" rx="%s" ry="%s" fill="%s" opacity=".85"/>'
                 '<ellipse cx="%s" cy="-8" rx="%s" ry="%s" fill="%s" opacity=".7"/></g>'
                 % (f(ox), f(oy), f(s),
                    f(r2.uniform(-3,3)), f(r2.uniform(13,18)), f(r2.uniform(11,15)), tone,
                    f(r2.uniform(-11,-7)), f(r2.uniform(8,12)), f(r2.uniform(7,10)), tone,
                    f(r2.uniform(7,11)), f(r2.uniform(8,12)), f(r2.uniform(7,10)), '#5C8A50'))
    # the orchard wall
    o.append('<path d="M0 302 L0 282 Q42 274 84 282 Q134 272 180 282 Q234 273 284 282 '
             'Q338 272 390 282 Q444 273 490 282 Q508 278 520 282 L520 302 Z" fill="#D9BE94"/>')
    o.append('<path d="M0 288 Q120 280 260 288 Q400 296 520 288" stroke="#C4A57A" '
             'stroke-width="2" fill="none" opacity=".6"/>')
    o.append('<rect y="300" width="520" height="80" fill="url(#pearth)"/>')
    o.append('<path d="M0 300 H520" stroke="#BE9F72" stroke-width="2"/>')
    o.append('<rect y="300" width="520" height="80" fill="url(#pgrit)"/>')
    # the juy that keeps the orchard alive
    o.append('<path d="M0 352 Q130 344 260 354 Q390 364 520 356 L520 364 Q390 372 260 362 '
             'Q130 352 0 360 Z" fill="#B6C8C1" opacity=".7"/>')
    o.append('<path d="M0 354 Q130 346 260 356 Q390 366 520 358" stroke="#EAF2EF" '
             'stroke-width="1.6" fill="none" opacity=".75"/>')
    o.append('<g stroke="#7E9455" stroke-width="1.3" fill="none" opacity=".65">%s</g>' % ''.join(
        '<path d="M%s %s q%s -%s %s -%s"/>' % (f(gx), f(gy), f(rnd.uniform(-2,2)), f(rnd.uniform(4,9)),
                                               f(rnd.uniform(-4,4)), f(rnd.uniform(5,11)))
        for gx, gy in [(rnd.uniform(20,500), rnd.uniform(306,346)) for _ in range(22)]))
    o.append('<ellipse cx="252" cy="344" rx="104" ry="13" fill="#A5854F" opacity=".22"/>')

    limbs, tips, mids = _tree(_pick_seed())
    L0 = [d for d, dep in limbs if dep == 0]
    L1 = [d for d, dep in limbs if dep == 1]
    L2 = [d for d, dep in limbs if dep == 2]
    L3 = [d for d, dep in limbs if dep >= 3]
    clumps = list(tips) + list(mids[::6])
    # a drooping outer skirt, so the canopy is a vase and not a mushroom cap
    clumps += [(x + (10 if x > 246 else -10), y + 26, w)
               for x, y, w in tips if abs(x - 246) > 84]

    # 1. seed and first leaves
    o.append('<g class="st" data-at="0.05">')
    o.append('<ellipse cx="246" cy="342" rx="26" ry="7" fill="#C0A377" opacity=".5"/>')
    o.append('<path d="M246 342 V314" stroke="#6E9450" stroke-width="3" stroke-linecap="round"/>')
    o.append('<ellipse cx="235" cy="311" rx="9" ry="4" fill="#6E9450" transform="rotate(-22 235 311)"/>')
    o.append('<ellipse cx="257" cy="310" rx="9" ry="4" fill="#7CA85C" transform="rotate(20 257 310)"/>')
    o.append('</g>')
    # 2. sapling
    o.append('<g class="st" data-at="0.16">')
    o.append('<path d="M246 344 C243 314 244 290 248 266" stroke="%s" stroke-width="6" '
             'fill="none" stroke-linecap="round"/>' % BARK)
    o.append(_clump(248, 260, random.Random(11), 9, 14, G_MID, lo=4, hi=6))
    o.append('</g>')
    # 3. trunk and the low fork
    o.append('<g class="st" data-at="0.27">')
    o.append('<g fill="url(#ptrunk)">%s</g>' % ''.join('<path d="%s"/>' % d for d in L0))
    o.append('<g stroke="%s" stroke-width="1.3" fill="none" opacity=".5">'
             '<path d="M236 340 C235 320 236 300 240 280"/>'
             '<path d="M256 340 C258 318 257 300 254 278"/>'
             '<path d="M246 338 C245 318 246 300 247 282"/></g>' % BARK_D)
    o.append(_clump(248, 254, random.Random(13), 12, 18, G_MID))
    o.append('</g>')
    # 4. the frame of the tree
    o.append('<g class="st" data-at="0.38">')
    o.append('<g fill="url(#ptrunk)">%s</g>' % ''.join('<path d="%s"/>' % d for d in L1))
    o.append('<g fill="%s">%s</g>' % (BARK, ''.join('<path d="%s"/>' % d for d in L2)))
    o.append('</g>')
    o.append('<g class="st" data-at="0.48">')
    o.append('<g fill="%s">%s</g>' % (BARK_L, ''.join('<path d="%s"/>' % d for d in L3)))
    o.append('</g>')
    # 5. canopy: a solid mass, then leaves breaking its edge
    o.append('<g class="st" data-at="0.56">')
    o.append('<g fill="#2F5730">%s</g>' % ''.join(
        '<ellipse cx="%d" cy="%d" rx="%d" ry="%d"/>' % (round(x), round(y), 30, 24)
        for x, y, w in clumps))
    o.append('<g fill="#3E6B39">%s</g>' % ''.join(
        '<ellipse cx="%d" cy="%d" rx="%d" ry="%d"/>' % (round(x-4), round(y-5), 23, 19)
        for x, y, w in clumps))
    o.append('<g fill="#4C8144">%s</g>' % ''.join(
        '<ellipse cx="%d" cy="%d" rx="%d" ry="%d"/>' % (round(x+5), round(y-9), 15, 12)
        for x, y, w in clumps if y < 216))
    o.append(''.join(_ring(x, y, random.Random(400+i), 7, 31, G_DARK)
                     for i, (x, y, w) in enumerate(clumps)))
    o.append(''.join(_ring(x-4, y-6, random.Random(500+i), 5, 23, G_MID)
                     for i, (x, y, w) in enumerate(clumps)))
    o.append(''.join(_ring(x+5, y-10, random.Random(600+i), 4, 15, G_LITE)
                     for i, (x, y, w) in enumerate(clumps) if y < 216))
    o.append('</g>')
    # 6. blossoms
    o.append('<g class="st" data-at="0.68">')
    o.append(''.join(
        '<g transform="translate(%s %s) rotate(%s)">'
        '<path d="M0 0 C-6 -1 -7 -8 -3 -11 C0 -13 3 -13 6 -11 C10 -8 7 -1 0 0 Z" fill="#E2542B"/>'
        '<path d="M-3 -11 l-3 -4 M0 -12 v-5 M3 -11 l3 -4" stroke="#E2542B" stroke-width="2.2" '
        'stroke-linecap="round"/><path d="M-4 -1 q4 3 8 0" stroke="#9E3316" stroke-width="1.5" '
        'fill="none"/></g>'
        % (f(x + random.Random(700+i).uniform(-14, 14)),
           f(y + random.Random(800+i).uniform(-12, 12)),
           f(random.Random(900+i).uniform(-40, 40)))
        for i,(x,y,w) in enumerate(clumps[::3])))
    o.append('</g>')
    # fruit hangs on the outer, lower wood
    hang = sorted(tips, key=lambda t: -(t[1]*1.0 + abs(t[0]-246)*0.7))[:14]
    o.append('<g class="st" data-at="0.79">%s</g>' % ''.join(
        _fruit(x + random.Random(1000+i).uniform(-8, 8),
               y + random.Random(1100+i).uniform(20, 38), 5.6, ripe=False)
        for i,(x,y,w) in enumerate(hang[:7])))
    o.append('<g class="st" data-at="0.90">%s</g>' % ''.join(
        _fruit(x + random.Random(1000+i).uniform(-8, 8),
               y + random.Random(1100+i).uniform(20, 38),
               [13, 15.5, 12, 14.5][i % 4])
        for i,(x,y,w) in enumerate(hang)))
    # 9. the harvest
    o.append('<g class="st" data-at="0.98">')
    o.append('<ellipse cx="404" cy="352" rx="52" ry="11" fill="#9C7C48" opacity=".28"/>')
    o.append(_fruit(444, 338, 16))
    o.append('<g transform="translate(396 334)">')
    o.append('<circle r="26" fill="#A81F2B"/>')
    o.append('<path d="M-26 0 A26 26 0 0 1 26 0 Z" fill="#C13A33"/>')
    o.append('<circle r="21" fill="#F6E6CE"/>')
    o.append('<path d="M0 -21 A21 21 0 0 1 0 21 Z" fill="#FAF0DE"/>')
    ar = random.Random(77); seeds=[]
    for _ in range(40):
        a = ar.uniform(0, math.pi*2); rr = ar.uniform(0, 1)**0.55 * 16.6
        sx, sy = math.cos(a)*rr, math.sin(a)*rr
        rad = ar.uniform(2.0, 3.2)
        seeds.append('<circle cx="%s" cy="%s" r="%s" fill="url(#paril)"/>' % (f(sx), f(sy), f(rad)))
        seeds.append('<circle cx="%s" cy="%s" r="%s" fill="#FFD9DF" opacity=".5"/>'
                     % (f(sx-rad*.3), f(sy-rad*.32), f(rad*.3)))
    o.append(''.join(seeds))
    o.append('<g stroke="#F2E2C6" stroke-width="1.3" fill="none" opacity=".75">'
             '<path d="M0 -18 V18"/><path d="M-16 -7 L16 7"/><path d="M-16 7 L16 -7"/></g>')
    o.append('</g>')
    o.append('<g fill="#E2542B" opacity=".8">'
             '<path d="M336 352 c-5 -1 -6 -6 -2 -9 c3 -2 7 -1 8 2 c1 3 -2 7 -6 7 Z"/>'
             '<path d="M470 356 c-5 -1 -6 -6 -2 -9 c3 -2 7 -1 8 2 c1 3 -2 7 -6 7 Z"/></g>')
    o.append('</g>')
    o.append('</svg>')
    return ''.join(o)

# ================================================================== MINIS
MINIS = {
 'carpet': ('<svg viewBox="0 0 40 40">'
   '<rect x="7" y="5" width="26" height="30" rx="1.5" fill="#8E2C3B"/>'
   '<rect x="9" y="7" width="22" height="26" fill="none" stroke="#EFDCB8" stroke-width="1.5"/>'
   '<rect x="11.5" y="9.5" width="17" height="21" fill="none" stroke="#1E3348" stroke-width="1.2"/>'
   '<polygon points="20,12 25,15.5 25,20.5 20,24 15,20.5 15,15.5" fill="#1E3348" '
   'stroke="#EFDCB8" stroke-width="1"/>'
   '<polygon points="20,15 23,17 23,20 20,22 17,20 17,17" fill="#C8893A"/>'
   '<path d="M20 26.5 l2.5 2 -2.5 2 -2.5 -2 Z" fill="#EFDCB8"/>'
   '<path d="M8 35v3M12 35v3M16 35v3M20 35v3M24 35v3M28 35v3M32 35v3" '
   'stroke="#D9C7A6" stroke-width="1.3" stroke-linecap="round"/></svg>'),
 'minarets': ('<svg viewBox="0 0 40 40">'
   '<path d="M6 34 L8 14 L12 14 L14 34 Z" fill="#D9B784"/>'
   '<path d="M16 34 L18 7 L23 7 L25 34 Z" fill="#EAD0A6"/>'
   '<path d="M27 34 L29 16 L33 16 L35 34 Z" fill="#D9B784"/>'
   '<g fill="#3BA5B0"><rect x="6.8" y="22" width="6.4" height="2"/>'
   '<rect x="6.4" y="28" width="7.2" height="2"/>'
   '<rect x="16.9" y="16" width="7.2" height="2.2"/><rect x="16.4" y="24" width="8.2" height="2.2"/>'
   '<rect x="27.8" y="23" width="6.4" height="2"/><rect x="27.4" y="29" width="7.2" height="2"/></g>'
   '<g fill="#B08652"><rect x="6.6" y="12" width="6.8" height="2.4" rx="1"/>'
   '<rect x="16.6" y="5" width="7.8" height="2.6" rx="1"/>'
   '<rect x="27.6" y="14" width="6.8" height="2.4" rx="1"/></g>'
   '<rect x="4" y="34" width="32" height="2.6" fill="#E0CBA2"/></svg>'),
 'dress': ('<svg viewBox="0 0 40 40">'
   '<path d="M15 6 C17 4 23 4 25 6 L27 15 C24 16 16 16 13 15 Z" fill="#BE2062"/>'
   '<path d="M13.5 15 C11 22 8 30 6 35 L34 35 C32 30 29 22 26.5 15 Z" fill="#BE2062"/>'
   '<path d="M15 6 L9 9 C7.5 14 7.5 19 8.5 22 L12 21 C12.5 16 13 12 15 10 Z" fill="#A31A54"/>'
   '<path d="M25 6 L31 9 C32.5 14 32.5 19 31.5 22 L28 21 C27.5 16 27 12 25 10 Z" fill="#D34C82"/>'
   '<rect x="16" y="5.5" width="8" height="10" fill="#151C33"/>'
   '<path d="M18.5 5 h3 v4.5 h-3 z" fill="#F0DFC9"/>'
   '<g fill="#E0B33C"><rect x="16.6" y="7" width="1.6" height="1.6"/>'
   '<rect x="21.8" y="7" width="1.6" height="1.6"/><rect x="19.2" y="11" width="1.6" height="1.6"/></g>'
   '<path d="M7.4 28 C16 30.5 24 30.5 32.6 28 L33.6 32 C24.5 34.6 15.5 34.6 6.4 32 Z" fill="#255A50"/>'
   '<path d="M6.9 30 C16 32.6 24 32.6 33.1 30" stroke="#D9A62E" stroke-width="1.4" fill="none"/>'
   '<path d="M6 35 C15 37.4 25 37.4 34 35" stroke="#D9A62E" stroke-width="1.6" fill="none"/></svg>'),
 'ghara': ('<svg viewBox="0 0 40 40">'
   '<path d="M14 6 C17 4.6 23 4.6 26 6 C27 14 27.6 24 28 31 C25 33 15 33 12 31 '
   'C12.4 24 13 14 14 6 Z" fill="#8FA8A4"/>'
   '<path d="M14 6 L9 9 C8 15 8 21 8.6 25 L12 24 C12.2 17 12.8 11 14 8 Z" fill="#7A938E"/>'
   '<path d="M26 6 L31 9 C32 15 32 21 31.4 25 L28 24 C27.8 17 27.2 11 26 8 Z" fill="#A5BBB7"/>'
   '<rect x="14.6" y="5.2" width="10.8" height="15" fill="#0E1F1B"/>'
   '<rect x="16.2" y="6.8" width="7.6" height="11.8" fill="none" stroke="#EDF3F0" stroke-width="1"/>'
   '<g fill="#EDF3F0"><circle cx="17.9" cy="9.2" r="0.75"/><circle cx="22.1" cy="9.2" r="0.75"/>'
   '<circle cx="17.9" cy="12.4" r="0.75"/><circle cx="22.1" cy="12.4" r="0.75"/>'
   '<circle cx="17.9" cy="15.6" r="0.75"/><circle cx="22.1" cy="15.6" r="0.75"/></g>'
   '<path d="M20 4.8 V11" stroke="#0B1614" stroke-width="1.8"/>'
   '<rect x="8.4" y="22" width="4" height="4" fill="#142824"/>'
   '<rect x="27.6" y="22" width="4" height="4" fill="#142824"/></svg>'),
 'pomegranate': ('<svg viewBox="0 0 40 40">'
   '<ellipse cx="31" cy="11" rx="6" ry="2.6" fill="#4C8144" transform="rotate(-34 31 11)"/>'
   '<circle cx="20" cy="23" r="12.5" fill="#B4232C"/>'
   '<path d="M20 10.5 a12.5 12.5 0 0 0 -11.9 16.3 A12.5 12.5 0 0 1 20 10.5 Z" fill="#DA4A38"/>'
   '<ellipse cx="15.4" cy="18.2" rx="3.6" ry="2" fill="#FFFFFF" opacity=".3" '
   'transform="rotate(-28 15.4 18.2)"/>'
   '<path d="M14.6 10.4 L13.4 2.6 L17 6.6 L20 1 L23 6.6 L26.6 2.6 L25.4 10.4 '
   'C23.8 9.4 16.2 9.4 14.6 10.4 Z" fill="#7E1B26"/>'
   '</svg>'),
}

# =================================================================== EMIT
def js_obj(name, d, order):
    parts = []
    for k in order:
        parts.append('  %s:`%s`' % (k, d[k]))
    return 'const %s = {\n%s\n};\n' % (name, ',\n'.join(parts))

ORDER = ['carpet', 'minarets', 'dress', 'ghara', 'pomegranate']
scenes = {'carpet': carpet(), 'minarets': minarets(), 'dress': dress(),
          'ghara': ghara(), 'pomegranate': pomegranate()}

for k, v in list(scenes.items()) + list(MINIS.items()):
    assert '`' not in v and '${' not in v, 'template-literal hazard in ' + k
    assert '</svg>' in v, 'unterminated svg in ' + k

minis_block = ('/* ---------- mini icons for the selector chips ---------- */\n'
               + js_obj('MINIS', MINIS, ORDER) + '\n')
scenes_block = ('/* ---------- full scenes (progressive builds) ----------\n'
                '   Each scene fills the frame. Groups with class="st" and data-at\n'
                '   appear when day/14 >= data-at. "rise" groups rise into place.\n'
                '   Art is generated (see build/gen.py) so the density is real.  */\n'
                + js_obj('SCENES', scenes, ORDER) + '\n')

open('minis.js', 'w').write(minis_block)
open('scenes.js', 'w').write(scenes_block)
for k in ORDER:
    print('%-12s scene %6d chars   mini %5d chars' % (k, len(scenes[k]), len(MINIS[k])))
print('total scenes: %d chars' % sum(len(v) for v in scenes.values()))
