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
