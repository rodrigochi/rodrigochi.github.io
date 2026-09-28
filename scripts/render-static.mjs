// Refresh readable HTML using the same content and paper renderer as the browser.
// Run from any directory: node scripts/render-static.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
const file = fileURLToPath(new URL('../index.html', import.meta.url));
let html = readFileSync(file, 'utf8');
const content = html.slice(html.indexOf('const ME ='), html.indexOf('const $ ='));
const escapeFn = html.slice(html.indexOf('const esc ='), html.indexOf('const store ='));
const renderers = html.slice(html.indexOf('function bib('), html.indexOf('function render(){'));
const lab = html.slice(html.indexOf('const LAB ='), html.indexOf('let tab ='));
const result = vm.runInNewContext(`${content}\n${escapeFn}\n${lab}
  const nodes = {}; const $ = s => nodes[s] ||= {};
  const lang = 'en', topic = 'all', open = {};
  ${renderers}
  renderPapers();
  ({papers: nodes['#papers'].innerHTML, bio:T.en.bio, now:T.en['now.p'],
    heading:T.en.topics.src[0], intro:T.en.intro.src, description:T.en.topics.src[1], caption:LAB.en.src.cap});
`, {}, { timeout: 1000 });
for (const [id, value] of Object.entries({ 'lab-h':result.heading, 'lab-intro':result.intro, 'lab-p':result.description, 'lab-cap':result.caption })) {
  const pattern = new RegExp(`(<(?:h3|p)[^>]*id="${id}"[^>]*>)[\\s\\S]*?(</(?:h3|p)>)`);
  html = html.replace(pattern, (_, start, end) => start + value + end);
}
html = html.replace(/(<p class="bio" data-th="bio">)[\s\S]*?(<\/p>)/, (_, a, b) => a + result.bio + b);
html = html.replace(/(<p data-th="now.p">)[\s\S]*?(<\/p>)/, (_, a, b) => a + result.now + b);
html = html.replace(/(<ol class="papers" id="papers">)[\s\S]*?(<\/ol>)/, (_, a, b) => a + result.papers + b);
writeFileSync(file, html);
console.log('Static biography, research introduction and publications refreshed.');
