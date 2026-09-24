#!/usr/bin/env python3
"""Būvē vietni:
  src.html         -> index.html   (assets/*.jpg iešūti base64, __BASE__ aizstāts)
  privacy.src.html -> privacy.html
  + robots.txt, sitemap.xml, llms.txt, og-cover.jpg
Ja mainās domēns — nomaini tikai BASE zemāk un palaid `python3 build.py`.
"""
import base64, re, pathlib, datetime

BASE = "https://halavinwww-tech.github.io/Arsenala5/"

root = pathlib.Path(__file__).parent
today = datetime.date.today().isoformat()

def inline(m):
    return "data:image/jpeg;base64," + base64.b64encode((root / m.group(1)).read_bytes()).decode()

src = (root / "src.html").read_text(encoding="utf-8").replace("__BASE__", BASE)
out = re.sub(r"(assets/[\w\-]+\.jpg)", inline, src)
(root / "index.html").write_text(out, encoding="utf-8")

priv = (root / "privacy.src.html").read_text(encoding="utf-8").replace("__BASE__", BASE)
(root / "privacy.html").write_text(priv, encoding="utf-8")

(root / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")

(root / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{BASE}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>1.0</priority></url>
  <url><loc>{BASE}privacy.html</loc><lastmod>{today}</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>
</urlset>
""", encoding="utf-8")

(root / "llms.txt").write_text(f"""# Trīs Maisi — Arsenāla iela 5, Rīga

> 18th-century warehouse complex in Riga Old Town (Latvia), offered as a reconstruction / development project. Owner and website operator: SIA "Arsenāla 5". Site languages: Latvian, English, Russian.

## Key facts
- Address: Arsenāla iela 5, Rīga, LV-1050, Latvia (Old Riga / Vecrīga). Coordinates: 56.95107, 24.10304.
- Heritage: formed from three historic warehouses — "Nastu nesējs" (Burden Carrier), "Trīs brāļi" (Three Brothers), "Cukura vārītājs" (Sugar Cooker). State architectural monument No. 6578; within the Historic Centre of Riga urban monument (No. 7442) and UNESCO World Heritage Site No. 852.
- Size: ~1,850 m² net lettable area — 1,390 m² residential (27–32 apartments, floors 2–4), 351 m² ground-floor commercial (3 units: restaurant/wine bar, co-working/office, beauty/SPA), 108 m² basement technical/storage.
- Concept: street façade and volume preserved; each of the three parts becomes a separate house with its own entrance, new inner courtyard and stairwell; historic goods hoists restored.
- Financials (business plan, indicative): CAPEX €5.05M (construction €4.81M at €2,600/m² + design/legal €0.24M); GDV €8.32M; gross profit ~€3.27M; ROI 64.7%; IRR 24.5% p.a.; cycle 24–30 months; rental-scenario NOI ~€420,000/year.
- Exit strategies: phased presale/retail; aparthotel + commercial rental via single operator; single-lot sale to an institutional investor or fund.
- Location: 2 min walk to Riga Castle / Castle Square; near Art Museum "Riga Bourse", Dome Square and the Daugava embankment.

## Contact
- Contact person: Aleksejs Halavins, +371 29 205 417, info@arsenala5.lv (SIA "Arsenāla 5").

## Pages
- [Home]({BASE}): full project overview (LV/EN/RU)
- [Privacy policy]({BASE}privacy.html)
""", encoding="utf-8")

# og-cover.jpg (1200x630)
og = root / "og-cover.jpg"
try:
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(root / "assets/photo-2.jpg").convert("RGB")
    w, h = 1200, 630
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    top = int(im.height * 0.28); im = im.crop((0, top, w, top + h))
    shade = Image.new("RGB", (w, h), (15, 28, 46))
    mask = Image.linear_gradient("L").resize((w, h)).point(lambda v: 70 + v * 0.62)
    im = Image.composite(shade, im, mask)
    d = ImageDraw.Draw(im)
    F = "/System/Library/Fonts/Supplemental/"
    big = ImageFont.truetype(F + "Georgia.ttf", 108); ital = ImageFont.truetype(F + "Georgia Italic.ttf", 108)
    small = ImageFont.truetype(F + "Georgia.ttf", 30)
    d.text((70, 330), "Trīs ", font=big, fill=(244, 242, 236))
    d.text((70 + d.textlength("Trīs ", font=big), 330), "Maisi", font=ital, fill=(212, 180, 106))
    d.text((72, 290), "ARSENĀLA IELA 5  ·  VECRĪGA  ·  UNESCO", font=small, fill=(212, 180, 106))
    d.text((72, 480), "~1 850 m²   ·   27–32 dzīvokļi   ·   GDV €8.3M", font=small, fill=(244, 242, 236))
    im.save(og, quality=86, optimize=True)
except Exception as e:
    print("og-cover skipped:", e)

print(f"index.html: {len(out)/1e6:.2f} MB · BASE = {BASE}")
