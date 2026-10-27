#!/usr/bin/env node
// GoldBrief browser QA: horizontal overflow, JS errors, mobile drawer behaviour.
// Usage: node tests/browser_check.js [--json out.json]   (needs `playwright` + chromium)
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const root = path.resolve(__dirname, "..");
const pages = ["index","resources","ui-ux","news","lake","leaderboards","usa","international","visuals","markets","apps","index-directory","glossary","encyclopedia","trust","about"];
const widths = [320, 375, 390, 430, 768, 1023, 1024, 1280, 1440, 1920];
const types = { ".html":"text/html", ".css":"text/css", ".js":"text/javascript", ".json":"application/json", ".svg":"image/svg+xml" };
const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split("?")[0]).replace(/^\/+$/, "/index.html"));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": types[path.extname(p)] || "application/octet-stream" }); fs.createReadStream(p).pipe(res);
});
(async () => {
  await new Promise(r => server.listen(0, r));
  const base = `http://127.0.0.1:${server.address().port}/`;
  const browser = await chromium.launch();
  const failures = [];
  const fail = (check, page, detail) => failures.push({ check, page, detail });
  for (const w of widths) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
    for (const name of pages) {
      const page = await ctx.newPage();
      page.on("pageerror", e => fail("js-error", `${name}@${w}`, String(e)));
      page.on("console", m => { if (m.type() === "error" && !/daily\.json|Failed to load resource/.test(m.text())) fail("console-error", `${name}@${w}`, m.text()); });
      await page.goto(`${base}${name}.html`, { waitUntil: "networkidle" });
      const over = await page.evaluate(() => {
        const d = document.documentElement, bad = [];
        if (d.scrollWidth > d.clientWidth + 1) {
          for (const el of document.body.querySelectorAll("*")) { const r = el.getBoundingClientRect(); if (r.width && r.right > d.clientWidth + 1 && !el.closest("[hidden]")) { bad.push(el.tagName.toLowerCase() + "." + String(el.className).split(" ")[0]); if (bad.length > 3) break; } }
          return { scrollWidth: d.scrollWidth, clientWidth: d.clientWidth, offenders: bad };
        }
        return null;
      });
      if (over) fail("horizontal-overflow", `${name}@${w}`, JSON.stringify(over));
      if (w >= 1024) {
        const h = await page.evaluate(() => { const l = document.querySelector(".site-header .nav__list"); return l ? { h: l.getBoundingClientRect().height, over: document.querySelector(".site-header__inner").scrollWidth - document.querySelector(".site-header__inner").clientWidth } : null; });
        if (!h || h.h > 50 || h.over > 0) fail("header-fit", `${name}@${w}`, JSON.stringify(h));
      }
      if (w >= 1024 && name === "index") {
        const btns = page.locator(".nav-group__btn");
        for (let i = 0; i < await btns.count(); i++) {
          await btns.nth(i).click();
          const box = await page.locator(".nav-group").nth(i).locator(".nav-panel").boundingBox();
          if (!box || box.x < 0 || box.x + box.width > w + 1) fail("menu-panel", `${name}@${w}`, `group ${i} panel ${JSON.stringify(box)}`);
          await page.keyboard.press("Escape");
          if (await page.locator(".nav-group").nth(i).locator(".nav-panel").isVisible()) fail("menu-panel", `${name}@${w}`, `group ${i} Escape did not close`);
        }
      }
      if (w < 1024 && name === "index") {
        const toggle = page.locator(".nav-toggle");
        await toggle.click();
        if (await page.locator("#nav-drawer").isHidden()) fail("drawer", `${name}@${w}`, "did not open");
        await page.keyboard.press("Escape");
        if (await page.locator("#nav-drawer").isVisible()) fail("drawer", `${name}@${w}`, "Escape did not close");
        if ((await page.evaluate(() => document.activeElement && document.activeElement.className)) !== "nav-toggle") fail("drawer", `${name}@${w}`, "focus not returned to toggle");
      }
      await page.close();
    }
    await ctx.close();
  }
  await browser.close(); server.close();
  const report = { result: failures.length ? "FAIL" : "PASS", pages: pages.length, widths, failures };
  const i = process.argv.indexOf("--json"); if (i > 0) fs.writeFileSync(process.argv[i + 1], JSON.stringify(report, null, 2) + "\n");
  console.log(JSON.stringify(report, null, 2)); process.exit(failures.length ? 1 : 0);
})();
