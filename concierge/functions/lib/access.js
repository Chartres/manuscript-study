// Copied from logseq-graph/think/lib/access.js; only the audience differs.
// Who is calling, checked rather than assumed: a note posted to /api/say can start an agent on
// the mini, so the Access token's signature, audience, issuer and expiry are verified here
// instead of trusting that every hostname in front of this project stays gated.
const TEAM = "https://chartres.cloudflareaccess.com";
const AUD = "145b866a3bf876f59a6ca14441091e83a9981e7a9a4e4c3cab18f36886f32357"; // Access app "manuscript-study-admin" (manuscript-study.dravec.org/admin)

let keys = null; // the team's public signing keys, cached per isolate
const bytes = (b64url) => Uint8Array.from(atob(b64url.replace(/-/g, "+").replace(/_/g, "/")), (c) => c.charCodeAt(0));
const parse = (b64url) => JSON.parse(new TextDecoder().decode(bytes(b64url)));
const certs = async () => (await (await fetch(TEAM + "/cdn-cgi/access/certs")).json()).keys || [];

// The verified e-mail of the caller, or "" when anything about the token does not hold.
export async function verifiedEmail(request, now = Date.now()) {
  const jwt = request.headers.get("Cf-Access-Jwt-Assertion") || (request.headers.get("cookie") || "").match(/CF_Authorization=([^;]+)/)?.[1];
  if (!jwt) return "";
  try {
    const [h, p, s] = jwt.split(".");
    const header = parse(h), claims = parse(p);
    if (header.alg !== "RS256") return "";
    keys ??= await certs();
    let jwk = keys.find((k) => k.kid === header.kid);
    if (!jwk) { keys = await certs(); jwk = keys.find((k) => k.kid === header.kid); } // keys rotate
    if (!jwk) return "";
    const key = await crypto.subtle.importKey("jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["verify"]);
    const signed = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", key, bytes(s), new TextEncoder().encode(h + "." + p));
    const fresh = typeof claims.exp === "number" && claims.exp * 1000 > now;
    if (!signed || !fresh || claims.iss !== TEAM || ![].concat(claims.aud || []).includes(AUD)) return "";
    return String(claims.email || "").toLowerCase();
  } catch {
    return "";
  }
}

