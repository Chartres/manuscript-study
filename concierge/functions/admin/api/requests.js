// Owner only (also behind Cloudflare Access): GET lists requests; POST {id, status} updates one.
import { verifiedEmail } from "../../lib/access.js";
const owner = async (request, env) => String(env.OWNERS || "").split(",").map((s) => s.trim()).includes(await verifiedEmail(request));

export async function onRequestGet({ request, env }) {
  if (!(await owner(request, env))) return new Response("owner only", { status: 403 });
  const ids = JSON.parse((await env.REQUESTS.get("index")) || "[]");
  const recs = await Promise.all(ids.map(async (id) => JSON.parse((await env.REQUESTS.get(`req:${id}`)) || "null")));
  return Response.json(recs.filter(Boolean), { headers: { "cache-control": "no-store" } });
}

export async function onRequestPost({ request, env }) {
  if (!(await owner(request, env))) return new Response("owner only", { status: 403 });
  const { id, status } = await request.json();
  const rec = JSON.parse((await env.REQUESTS.get(`req:${id}`)) || "null");
  if (!rec || !["new", "working", "delivered", "declined"].includes(status)) return new Response("bad", { status: 400 });
  rec.status = status; rec.updated = new Date().toISOString();
  await env.REQUESTS.put(`req:${id}`, JSON.stringify(rec));
  return Response.json(rec);
}
