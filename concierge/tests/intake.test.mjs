// node tests/intake.test.mjs — what a request must carry.
import assert from "node:assert";
import { check } from "../functions/lib/intake.js";
const img = (size = 1000, type = "image/jpeg") => ({ size, type, name: "p1.jpg" });

assert.equal(check({ email: "x" }, [img()]), "email");
assert.equal(check({ email: "a@b.cz" }, []), "no-pages");
assert.equal(check({ email: "a@b.cz" }, Array(13).fill(img())), "too-many");
assert.equal(check({ email: "a@b.cz" }, [img(9e6)]), "size");
assert.equal(check({ email: "a@b.cz" }, [img(10, "text/html")]), "type");
assert.equal(check({ email: "a@b.cz", web: "http://spam" }, [img()]), "spam");
const ok = check({ email: "eva@example.sk", name: "Eva", kind: "piano", occasion: "80th birthday, June", example_ok: "yes" }, [img(), img(10, "application/pdf")]);
assert.deepEqual([ok.email, ok.kind, ok.example_ok], ["eva@example.sk", "piano", true]);
assert.equal(check({ email: "a@b.cz", kind: "nonsense" }, [img()]).kind, "other-music");
console.log("intake: ok");

// ping: one envelope to the msg door with the Pages credential; visitor text is plain outside text.
import { ping } from "../functions/lib/intake.js";
const seen = [];
const stub = (status) => { seen.length = 0; globalThis.fetch = async (url, init) => { seen.push({ url, init, body: JSON.parse(init.body) }); return { status }; }; };
const env = { MSG_TOKEN: "c".repeat(40) };
stub(202);
assert.equal(await ping(env, "Manuscript study — nová žiadosť: <b>ignore previous</b>"), true);
assert.equal(seen.length, 1);
assert.equal(seen[0].url, "https://msg.dravec.org/");
assert.equal(seen[0].init.headers.authorization, "Bearer " + "c".repeat(40));
assert.deepEqual(seen[0].body, { v: 1, from: "manuscript.concierge", kind: "info", severity: "normal",
  text: "Manuscript study — nová žiadosť: <b>ignore previous</b>" });
stub(202);
await ping(env, "x".repeat(3500));
assert.equal(seen[0].body.text.length, 2000);
assert.equal("link" in seen[0].body, false);
assert.equal(await ping({ TG_TOKEN: "t", TG_CHAT: "1" }, "x"), false);
assert.equal(seen.length, 1, "no MSG_TOKEN sends nothing");
stub(401);
assert.equal(await ping(env, "x"), false);
globalThis.fetch = async () => { throw new Error("offline"); };
assert.equal(await ping(env, "x"), false);
console.log("ping: ok");
