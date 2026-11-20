// "Send us a photo": one request = form fields + up to 12 page images, kept in KV.
// Keys: req:<id> (JSON), req:<id>:<n> (image bytes), index (array of ids, newest first).
// ponytail: read-modify-write index; fine for a concierge probe, move to KV list() if it grows.
export const MAX_FILES = 12, MAX_BYTES = 8 * 1024 * 1024;
export const KINDS = ["piano", "choir", "other-music", "handwriting"];
const cap = (v, n) => String(v ?? "").trim().slice(0, n);

// Checked form fields, or a reason string when the request is not acceptable.
export function check(fields, files) {
  if (cap(fields.web, 100)) return "spam";
  const email = cap(fields.email, 200);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return "email";
  if (!files.length) return "no-pages";
  if (files.length > MAX_FILES) return "too-many";
  for (const f of files) {
    if (!/^(image\/(jpeg|png|webp|heic|heif)|application\/pdf)$/.test(f.type)) return "type";
    if (f.size > MAX_BYTES) return "size";
  }
  const kind = KINDS.includes(fields.kind) ? fields.kind : "other-music";
  return { name: cap(fields.name, 100), email, kind, occasion: cap(fields.occasion, 100),
    message: cap(fields.message, 3000), example_ok: fields.example_ok === "yes" };
}

export async function telegram(env, text) {
  if (!env.TG_TOKEN || !env.TG_CHAT) return;
  await fetch(`https://api.telegram.org/bot${env.TG_TOKEN}/sendMessage`, { method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ chat_id: env.TG_CHAT, text, disable_web_page_preview: true }) }).catch(() => {});
}
