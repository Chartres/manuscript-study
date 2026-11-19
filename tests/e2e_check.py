"""Browser check of a built study: the index lists pieces and plays; the study page aligns every
line, the cursor follows the audio and clicking a bar seeks. Uses the installed Chrome.
Run: python -I tests/e2e_check.py <base-url> <piece-slug> <bar-seconds>"""
import sys, time
from playwright.sync_api import sync_playwright

B, slug, per_bar = sys.argv[1], sys.argv[2], float(sys.argv[3])
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs = []
    pg = b.new_context(**p.devices["iPhone 13"]).new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"{B}/"); pg.wait_for_selector(".hraj button")
    pg.screenshot(path="/tmp/ms-index.png")
    pg.goto(f"{B}/study.html?k={slug}"); pg.wait_for_selector(".prepis svg"); time.sleep(1)
    aligned, total = pg.evaluate("() => [document.querySelectorAll('.sken.zarovnane').length, document.querySelectorAll('.system').length]")
    assert aligned == total, (aligned, total)
    pg.click("#hraj button"); time.sleep(per_bar * 3.5)
    bar = pg.evaluate("() => document.querySelector('.takt.teraz')?.title")
    assert bar and bar.split()[-1] in ("3", "4"), bar
    pg.click("#r2 .takt >> nth=0"); time.sleep(.6)
    first2 = pg.evaluate("() => document.querySelector('#r2 .takt').title")
    assert pg.evaluate("() => document.querySelector('.takt.teraz')?.title") == first2
    assert pg.evaluate("() => document.documentElement.scrollWidth <= innerWidth"), "horizontal overflow"
    pg.screenshot(path="/tmp/ms-study.png")
    assert not errs, errs
    b.close()
print("e2e: ok")
