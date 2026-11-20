// POST multipart: name, email, kind, occasion, message, example_ok, web (honeypot), pages (files).
import { check, telegram } from "../lib/intake.js";

export async function onRequestPost({ request, env }) {
  let form; try { form = await request.formData(); } catch { return Response.json({ error: "form" }, { status: 400 }); }
  const fields = Object.fromEntries([...form.entries()].filter(([, v]) => typeof v === "string"));
  const files = form.getAll("pages").filter((f) => typeof f !== "string");
  const r = check(fields, files);
  if (r === "spam") return Response.json({ ok: true });
  if (typeof r === "string") return Response.json({ error: r }, { status: 400 });
  const id = new Date().toISOString().slice(0, 10) + "-" + crypto.randomUUID().slice(0, 6);
  for (const [n, f] of files.entries()) {
    await env.REQUESTS.put(`req:${id}:${n}`, await f.arrayBuffer(), { metadata: { type: f.type, name: f.name.slice(0, 120) } });
  }
  const rec = { id, ...r, pages: files.length, at: new Date().toISOString(), status: "new" };
  await env.REQUESTS.put(`req:${id}`, JSON.stringify(rec));
  const index = JSON.parse((await env.REQUESTS.get("index")) || "[]");
  await env.REQUESTS.put("index", JSON.stringify([id, ...index]));
  await telegram(env, `Manuscript study — nová žiadosť: ${r.name || r.email}, ${files.length} str., ${r.kind}` +
    `${r.occasion ? ", príležitosť: " + r.occasion : ""}\nhttps://manuscript-study.dravec.org/admin/`);
  return Response.json({ ok: true, id });
}
