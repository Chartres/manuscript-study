// Owner only: GET ?id=<request>&n=<page> returns the uploaded page.
import { verifiedEmail } from "../../lib/access.js";

export async function onRequestGet({ request, env }) {
  const owners = String(env.OWNERS || "").split(",").map((s) => s.trim());
  if (!owners.includes(await verifiedEmail(request))) return new Response("owner only", { status: 403 });
  const u = new URL(request.url), id = u.searchParams.get("id"), n = u.searchParams.get("n");
  if (!/^[\w-]+$/.test(id || "") || !/^\d+$/.test(n || "")) return new Response("bad", { status: 400 });
  const { value, metadata } = await env.REQUESTS.getWithMetadata(`req:${id}:${n}`, "arrayBuffer");
  if (!value) return new Response("not found", { status: 404 });
  return new Response(value, { headers: { "content-type": metadata?.type || "application/octet-stream", "cache-control": "private, max-age=3600" } });
}
