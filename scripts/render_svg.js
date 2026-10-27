// Usage: node scripts/render_svg.js in.svg out.png size   (transparent background)
const { chromium } = require("playwright"); const fs = require("fs");
(async () => {
  const [, , input, out, sizeArg] = process.argv, size = +sizeArg;
  const svg = fs.readFileSync(input, "utf8").replace("<svg ", `<svg width="${size}" height="${size}" `);
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: size, height: size } });
  await p.setContent(`<body style="margin:0;background:transparent">${svg}`);
  await p.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: size, height: size } }); await b.close();
})();
