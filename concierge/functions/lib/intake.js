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

// Messages to Pavol through the msg door (msg.dravec.org; logseq-graph think/msg/README.md),
// with this Pages project's own credential (secret MSG_TOKEN, prefix manuscript.). The mini delivers
// to Telegram, so the project holds no bot token. Visitor text is outside text: it goes as one
// plain info message (the mini escapes markup), never as a link or anything else.
export async function ping(env, text, from = "manuscript.concierge") {
  if (!env.MSG_TOKEN) return false;
  try {
    const res = await fetch("https://msg.dravec.org/", {
      method: "POST",
      headers: { authorization: `Bearer ${env.MSG_TOKEN}`, "content-type": "application/json" },
      body: JSON.stringify({ v: 1, from, kind: "info", severity: "normal", text: String(text).slice(0, 2000) }),
    });
    return res.status === 202;
  } catch {
    return false;
  }
}
