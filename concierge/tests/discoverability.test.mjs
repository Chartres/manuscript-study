// node concierge/tests/discoverability.test.mjs — the Flywheel discoverability kit on the served root
// (flywheel docs/standards/discoverability.md). Serves concierge/site locally with the content types
// Cloudflare Pages sends and checks what crawlers, unfurlers and AI agents read.
import assert from "node:assert";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../site");
const HOST = "https://manuscript-study.dravec.org";
const TYPES = { ".html": "text/html", ".txt": "text/plain", ".xml": "application/xml", ".png": "image/png", ".svg": "image/svg+xml" };

const server = createServer(async (req, res) => {
  let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
  if (p.endsWith("/")) p += "index.html";
  const file = path.join(ROOT, p);
  if (!file.startsWith(ROOT)) return res.writeHead(403).end();
  try {
    const body = await readFile(file);
    res.writeHead(200, { "content-type": TYPES[path.extname(file)] || "application/octet-stream" }).end(body);
  } catch { res.writeHead(404).end(); }
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}`;
const get = async p => { const r = await fetch(base + p); assert.equal(r.status, 200, p); return r; };

try {
  let r = await get("/robots.txt");
  assert.match(r.headers.get("content-type"), /^text\/plain/);
  const robots = await r.text();
  assert.match(robots, /^User-agent: \*\nAllow: \/$/m);
  assert.ok(robots.includes(`Sitemap: ${HOST}/sitemap.xml`));
  assert.doesNotMatch(robots, /Disallow/);

  r = await get("/sitemap.xml");
  assert.match(r.headers.get("content-type"), /xml/);
  const sitemap = await r.text();
  assert.match(sitemap, /^<\?xml/);
  assert.ok(sitemap.includes(`<loc>${HOST}/</loc>`));

  r = await get("/llms.txt");
  assert.match(r.headers.get("content-type"), /^text\/plain/);
  assert.ok((await r.text()).startsWith("# "));

  r = await get("/og.png");
  assert.equal(r.headers.get("content-type"), "image/png");
  const png = Buffer.from(await r.arrayBuffer());
  assert.ok(png.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])), "PNG signature");
  assert.deepEqual([png.readUInt32BE(16), png.readUInt32BE(20)], [1200, 630]);
  assert.ok(png.length <= 300_000, `og.png ${png.length} bytes`);

  r = await get("/.well-known/security.txt");
  const sec = await r.text();
  assert.match(sec, /^Contact: https:\/\/github\.com\/Chartres\/manuscript-study\/issues$/m);
  const expires = new Date(sec.match(/^Expires: (.+)$/m)[1]);
  assert.ok(expires > new Date() && expires - new Date() <= 366 * 864e5, "Expires within a year");

  r = await get("/9cc2dcb0952bc859471bd181b22e3dcb.txt");
  assert.equal(await r.text(), "9cc2dcb0952bc859471bd181b22e3dcb");

  const html = await (await get("/")).text();
  const head = html.slice(0, html.indexOf("</head>"));
  const meta = (attr, key) => head.match(new RegExp(`<meta ${attr}="${key}" content="([^"]*)"`))?.[1];
  assert.match(html, /<html lang="en">/);
  assert.match(meta("property", "og:image"), /^https:\/\/.+\/og\.png$/);
  assert.equal(meta("name", "twitter:card"), "summary_large_image");
  assert.ok(meta("property", "og:title").length <= 45, "og:title ≤ 45");
  assert.ok(meta("name", "description"));
  assert.ok(head.includes(`<link rel="canonical" href="${HOST}/">`));
  const ld = JSON.parse(head.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  assert.equal(ld.isAccessibleForFree, true);
  assert.equal(ld.mainEntity.offers.price, "0");
} finally {
  server.close();
}
console.log("discoverability: ok");
