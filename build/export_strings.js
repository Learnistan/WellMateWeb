#!/usr/bin/env node
/* Exports every user-facing string from index.html and help.html into one CSV,
   English beside Dari beside Pashto, so a native reviewer can work in a
   spreadsheet without touching code. Reviewed text goes back in the same file.

   Usage:  node build/export_strings.js > build/strings-for-review.csv          */
const fs = require('fs');
const path = require('path');

function pullI18N(file) {
  const src = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
  const open = src.indexOf('<script>', src.indexOf('</style>')) + 8;
  const js = src.slice(open, src.indexOf('</script>', open));
  const start = js.indexOf('const I18N');
  const ctx = {};
  // evaluate only the data, never the rest of the page script
  const decl = js.slice(start, js.indexOf('\n};', start) + 3);
  new Function('g', 'with(g){' + decl + '; g.I18N = I18N;}')(ctx);
  return ctx.I18N;
}

const rows = [];
function walk(file, langs, node, trail) {
  const en = node.en;
  for (const key of Object.keys(en)) {
    const p = trail ? trail + '.' + key : key;
    const v = en[key];
    if (typeof v === 'string') {
      rows.push([file, p, v, get(langs.fa, p), get(langs.ps, p)]);
    } else if (typeof v === 'function') {
      rows.push([file, p + '()', String(v).slice(0, 300), fnOf(langs.fa, p), fnOf(langs.ps, p)]);
    } else if (Array.isArray(v)) {
      v.forEach((item, i) => {
        if (typeof item === 'string') rows.push([file, `${p}[${i}]`, item, get(langs.fa, `${p}[${i}]`), get(langs.ps, `${p}[${i}]`)]);
        else if (item && typeof item === 'object')
          Object.keys(item).forEach(k2 =>
            rows.push([file, `${p}[${i}].${k2}`, item[k2], get(langs.fa, `${p}[${i}].${k2}`), get(langs.ps, `${p}[${i}].${k2}`)]));
      });
    } else if (v && typeof v === 'object') {
      walk(file, langs, { en: v }, p);
    }
  }
}
const get = (root, dotted) => {
  try {
    return dotted.split(/[.\[\]]+/).filter(Boolean).reduce((a, k) => a[k], root) ?? '';
  } catch (e) { return ''; }
};
const fnOf = (root, dotted) => { const f = get(root, dotted); return typeof f === 'function' ? String(f).slice(0, 300) : ''; };

for (const file of ['index.html', 'help.html']) {
  const I = pullI18N(file);
  // help.html keeps English in the markup, so seed it from the fa key list
  const en = I.en && Object.keys(I.en).length ? I.en : Object.fromEntries(Object.keys(I.fa).map(k => [k, '(in markup)']));
  walk(file, I, { en }, '');
}

const esc = s => '"' + String(s).replace(/"/g, '""').replace(/\r?\n/g, ' ') + '"';
const out = [['file', 'key', 'english', 'dari_current', 'pashto_current', 'dari_corrected', 'pashto_corrected', 'reviewer_note']
  .map(esc).join(',')];
for (const r of rows) out.push([...r, '', '', ''].map(esc).join(','));
process.stdout.write('﻿' + out.join('\n') + '\n');
console.error(`${rows.length} strings exported for review`);
