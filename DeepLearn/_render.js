const fs = require('fs');
const path = require('path');
const { Resvg } = require('@resvg/resvg-js');

const dir = 'C:/WorkBuddy/DeepLearn/assets';
const out = 'C:/WorkBuddy/DeepLearn/_preview';
fs.mkdirSync(out, { recursive: true });

const files = fs.readdirSync(dir).filter(f => f.endsWith('.svg'));
let ok = 0;
for (const f of files) {
  try {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const r = new Resvg(svg, {
      fitTo: { mode: 'width', value: 1000 },
      font: {
        loadSystemFonts: true,
        defaultFontFamily: 'Microsoft YaHei',
      },
      background: '#ffffff',
    });
    const png = r.render().asPng();
    fs.writeFileSync(path.join(out, f.replace('.svg', '.png')), png);
    ok++;
  } catch (e) {
    console.log('FAIL', f, String(e).slice(0, 200));
  }
}
console.log('rendered', ok, '/', files.length);
