#!/usr/bin/env python3
"""Būvē vietni no avota failiem.

Rediģē tikai:  src.html  (LV teksts + EN/RU tulkojumi I18N objektā)  un  privacy.src.html
Palaid:        python3 build.py

Ģenerē (vietnei, GitHub Pages):
  index.html, en/index.html, ru/index.html   — katrai valodai sava indeksējama lapa (SEO/GEO)
  privacy.html, 404.html, robots.txt, sitemap.xml, llms.txt, og-cover.jpg, favicon-*.png
Ģenerē (sūtīšanai, NAV repo):
  Arsenala5-Tris-Maisi.html — viens pašpietiekams fails ar iešūtiem attēliem (LV/EN/RU pārslēgs)

Ja mainās domēns — nomaini tikai BASE.
"""
import base64, re, json, pathlib, datetime

BASE = "https://arsenala5.lv/"
LANGS = ["lv", "en", "ru"]
OFFLINE_NAME = "Arsenala5-Tris-Maisi.html"

root = pathlib.Path(__file__).parent
today = datetime.date.today().isoformat()

META = {
    "lv": dict(
        title="Trīs Maisi — Arsenāla iela 5, Vecrīga | Vēsturiskas noliktavas rekonstrukcija",
        desc="Trīs Maisi — 18. gs. noliktavu komplekss Arsenāla ielā 5, Vecrīgā (UNESCO). ~1 850 m² rekonstrukcijas projekts: 27–32 dzīvokļi, 351 m² komercplatību, GDV €8.3M, IRR 24.5%.",
        og_title="Trīs Maisi — Arsenāla iela 5, Vecrīga",
        og_desc="18. gs. noliktavu kompleksa rekonstrukcija Vecrīgā: ~1 850 m², 27–32 dzīvokļi, komercplatības. GDV €8.3M, IRR 24.5%.",
        tw_desc="18. gs. noliktavu kompleksa rekonstrukcija Vecrīgā: ~1 850 m², 27–32 dzīvokļi.",
        keywords="Arsenāla iela 5, Trīs Maisi, Vecrīga, nekustamais īpašums Rīgā, noliktavas rekonstrukcija, investīciju projekts, vēsturiska ēka, UNESCO",
        locale="lv_LV", img_alt="Trīs Maisi — Arsenāla iela 5, Vecrīga"),
    "en": dict(
        title="Trīs Maisi — Arsenāla Street 5, Old Riga | Historic Warehouse Redevelopment",
        desc="Trīs Maisi — an 18th-century warehouse complex at Arsenāla Street 5 in Old Riga (UNESCO). ~1,850 m² redevelopment: 27–32 apartments, 351 m² commercial, GDV €8.3M, IRR 24.5%.",
        og_title="Trīs Maisi — Arsenāla Street 5, Old Riga",
        og_desc="Redevelopment of an 18th-century warehouse complex in Old Riga: ~1,850 m², 27–32 apartments, commercial space. GDV €8.3M, IRR 24.5%.",
        tw_desc="Redevelopment of an 18th-century warehouse complex in Old Riga: ~1,850 m², 27–32 apartments.",
        keywords="Arsenala Street 5, Tris Maisi, Old Riga real estate, Riga investment property, historic building for sale Riga, warehouse redevelopment, Latvia real estate, UNESCO",
        locale="en_GB", img_alt="Trīs Maisi — Arsenāla Street 5, Old Riga"),
    "ru": dict(
        title="Trīs Maisi — ул. Арсенала, 5, Старая Рига | Реконструкция исторического склада",
        desc="Trīs Maisi — складской комплекс XVIII века на ул. Арсенала, 5 в Старой Риге (ЮНЕСКО). ~1 850 м²: 27–32 апартамента, 351 м² коммерции, GDV €8,3 млн, IRR 24,5%.",
        og_title="Trīs Maisi — ул. Арсенала, 5, Старая Рига",
        og_desc="Реконструкция складского комплекса XVIII века в Старой Риге: ~1 850 м², 27–32 апартамента, коммерческие помещения. GDV €8,3 млн, IRR 24,5%.",
        tw_desc="Реконструкция складского комплекса XVIII века в Старой Риге: ~1 850 м², 27–32 апартамента.",
        keywords="Арсенала 5, Trīs Maisi, недвижимость Старая Рига, инвестиционная недвижимость Рига, историческое здание продажа, реконструкция склада, недвижимость Латвия, ЮНЕСКО",
        locale="ru_RU", img_alt="Trīs Maisi — ул. Арсенала, 5, Старая Рига"),
}

def url(lang):
    return BASE if lang == "lv" else f"{BASE}{lang}/"

def attr(v):
    return v.replace("&", "&amp;").replace('"', "&quot;")

src = (root / "src.html").read_text(encoding="utf-8")

# --- tulkojumi no I18N objekta ---
def js_obj(name, nxt):
    a = src.index(f"\n{name}:{{") + len(f"\n{name}:{{")
    b = src.index(nxt, a)
    return json.loads("{" + src[a:b].strip().rstrip(",") + "}")
TR = {"en": js_obj("en", "\n},\nru:{"), "ru": js_obj("ru", "\n}};")}
LV = dict(re.findall(r'data-i18n="([^"]+)"[^>]*>([^<]*)<', src))

hreflang = "\n".join(
    [f'<link rel="alternate" hreflang="{l}" href="{url(l)}">' for l in LANGS]
    + [f'<link rel="alternate" hreflang="x-default" href="{BASE}">'])

def localize(html, lang):
    m = META[lang]
    html = html.replace('<html lang="lv">', f'<html lang="{lang}">', 1)
    html = re.sub(r"<title>.*?</title>", f"<title>{m['title']}</title>", html, 1)
    for sel, val in [('name="description"', m["desc"]), ('name="keywords"', m["keywords"]),
                     ('property="og:title"', m["og_title"]), ('property="og:description"', m["og_desc"]),
                     ('name="twitter:title"', m["og_title"]), ('name="twitter:description"', m["tw_desc"]),
                     ('property="og:locale"', m["locale"]), ('property="og:image:alt"', m["img_alt"])]:
        html = re.sub(rf'(<meta {sel} content=")[^"]*(")', lambda x: x.group(1) + attr(val) + x.group(2), html, 1)
    alts = [l for l in ("lv_LV", "en_GB", "ru_RU") if l != m["locale"]]
    html = re.sub(r'(<meta property="og:locale:alternate" content=")[^"]*(">)\n(<meta property="og:locale:alternate" content=")[^"]*(">)',
                  lambda x: f"{x.group(1)}{alts[0]}{x.group(2)}\n{x.group(3)}{alts[1]}{x.group(4)}", html, 1)
    html = html.replace('<link rel="canonical" href="__BASE__">', f'<link rel="canonical" href="{url(lang)}">', 1)
    html = html.replace('<meta property="og:url" content="__BASE__">', f'<meta property="og:url" content="{url(lang)}">', 1)
    html = html.replace("__HREFLANG__", hreflang)
    if lang == "lv":
        return html
    tr = TR[lang]
    # redzamais teksts
    def sub_el(x):
        k = x.group(2)
        return x.group(1) + (tr.get(k, x.group(3)).replace("<", "&lt;")) + "<"
    html = re.sub(r'(data-i18n="([^"]+)"[^>]*>)([^<]*)<', sub_el, html)
    # galerijas alt teksti
    for k, v in LV.items():
        if k.startswith("gal.c") and k in tr:
            html = html.replace(f'alt="{v} — Arsenāla 5"', f'alt="{attr(tr[k])} — Arsenāla 5"')
    # JSON-LD: BUJ teksti
    for i in range(1, 6):
        for kind in ("q", "a"):
            k = f"faq.{kind}{i}"
            html = html.replace(json.dumps(LV[k], ensure_ascii=False), json.dumps(tr[k], ensure_ascii=False))
    return html

def inline(m):
    return "data:image/jpeg;base64," + base64.b64encode((root / m.group(1)).read_bytes()).decode()

# --- vietnes lapas ---
for lang in LANGS:
    html = localize(src, lang).replace("__BASE__", BASE)
    html = html.replace("assets/", "/assets/").replace('href="privacy.html"', 'href="/privacy.html"')
    out = root / ("index.html" if lang == "lv" else f"{lang}/index.html")
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")

# --- sūtāmais fails (viens, ar iešūtiem attēliem) ---
off = localize(src, "lv").replace("__BASE__", BASE).replace('<html lang="lv">', '<html lang="lv" data-offline="1">', 1)
off = off.replace('href="privacy.html"', f'href="{BASE}privacy.html"')
off = re.sub(r"(assets/[\w\-]+\.jpg)", inline, off)
(root / OFFLINE_NAME).write_text(off, encoding="utf-8")

# --- privātuma politika ---
priv = (root / "privacy.src.html").read_text(encoding="utf-8").replace("__BASE__", BASE)
(root / "privacy.html").write_text(priv, encoding="utf-8")

# --- 404 ---
(root / "404.html").write_text("""<!DOCTYPE html>
<html lang="lv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lapa nav atrasta — Trīs Maisi</title><meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="/favicon-192.png">
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0f1c2e;color:#f4f2ec;font:16px/1.6 Georgia,serif;text-align:center;padding:24px}
h1{font-weight:400;font-size:44px;margin:0 0 8px}p{color:rgba(244,242,236,.7);margin:4px 0}a{color:#d4b46a}</style></head>
<body><div><h1>404</h1><p>Lapa nav atrasta · Page not found · Страница не найдена</p>
<p style="margin-top:22px"><a href="/">Trīs Maisi — Arsenāla iela 5</a></p></div></body></html>
""", encoding="utf-8")

# --- robots / sitemap ---
(root / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{url(l)}"/>' for l in LANGS) + \
       f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
urls = "".join(f"""
  <url>
    <loc>{url(l)}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if l == "lv" else "0.9"}</priority>{alts}
  </url>""" for l in LANGS)
(root / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}
  <url>
    <loc>{BASE}privacy.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>
""", encoding="utf-8")

# --- llms.txt ---
(root / "llms.txt").write_text(f"""# Trīs Maisi — Arsenāla iela 5, Rīga

> 18th-century warehouse complex in Riga Old Town (Latvia), offered as a reconstruction / development project. Owner and website operator: SIA "Arsenāla 5". Site languages: Latvian, English, Russian.

## Key facts
- Address: Arsenāla iela 5, Rīga, LV-1050, Latvia (Old Riga / Vecrīga). Coordinates: 56.95107, 24.10304.
- Heritage: formed from three historic warehouses — "Nastu nesējs" (Burden Carrier), "Trīs brāļi" (Three Brothers), "Cukura vārītājs" (Sugar Cooker). State architectural monument No. 6578; within the Historic Centre of Riga urban monument (No. 7442) and UNESCO World Heritage Site No. 852.
- Building: total building area 2,500 m²; land plot 459 m²; 5 floors (incl. basement and attic). Authentic 18th-century façades, timber beams and columns, historic goods-hoist wheel preserved.
- Planned use: ~1,850 m² net lettable area — 1,390 m² residential (27–32 apartments, floors 2–4), 351 m² ground-floor commercial (3 units: restaurant/wine bar, co-working/office, beauty/SPA), 108 m² basement technical/storage.
- Concept: street façade and volume preserved; each of the three parts becomes a separate house with its own entrance, new inner courtyard and stairwell; historic goods hoists restored.
- Financials (business plan, indicative): CAPEX €5.05M (construction €4.81M at €2,600/m² + design/legal €0.24M); GDV €8.32M; gross profit ~€3.27M; ROI 64.7%; IRR 24.5% p.a.; cycle 24–30 months; rental-scenario NOI ~€420,000/year. Price on request.
- Exit strategies: phased presale/retail; aparthotel + commercial rental via single operator; single-lot sale to an institutional investor or fund.
- Location: 2 min walk to Riga Castle / Castle Square; near Art Museum "Riga Bourse", Dome Square and the Daugava embankment.

## Contact
- Contact person: Aleksejs Halavins, +371 29 205 417, info@arsenala5.lv (SIA "Arsenāla 5").

## Pages
- [Home — Latvian]({url("lv")})
- [Home — English]({url("en")})
- [Home — Russian]({url("ru")})
- [Privacy policy]({BASE}privacy.html)
""", encoding="utf-8")

# --- attēli: og-cover + favicon ---
try:
    from PIL import Image, ImageDraw, ImageFont
    F = "/System/Library/Fonts/Supplemental/"
    im = Image.open(root / "assets/hero.jpg").convert("RGB")
    w, h = 1200, 630
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    top = int(im.height * 0.30); im = im.crop((0, top, w, top + h))
    shade = Image.new("RGB", (w, h), (15, 28, 46))
    mask = Image.linear_gradient("L").resize((w, h)).point(lambda v: 70 + v * 0.62)
    im = Image.composite(shade, im, mask)
    d = ImageDraw.Draw(im)
    big = ImageFont.truetype(F + "Georgia.ttf", 108); ital = ImageFont.truetype(F + "Georgia Italic.ttf", 108)
    small = ImageFont.truetype(F + "Georgia.ttf", 30)
    d.text((70, 330), "Trīs ", font=big, fill=(244, 242, 236))
    d.text((70 + d.textlength("Trīs ", font=big), 330), "Maisi", font=ital, fill=(212, 180, 106))
    d.text((72, 290), "ARSENĀLA IELA 5  ·  VECRĪGA  ·  UNESCO", font=small, fill=(212, 180, 106))
    d.text((72, 480), "~1 850 m²   ·   27–32 dzīvokļi   ·   GDV €8.3M", font=small, fill=(244, 242, 236))
    im.save(root / "og-cover.jpg", quality=86, optimize=True)
    for size, name in [(192, "favicon-192.png"), (180, "apple-touch-icon.png"), (48, "favicon-48.png")]:
        s = 4 * size
        ic = Image.new("RGB", (s, s), (15, 28, 46)); dd = ImageDraw.Draw(ic)
        f = ImageFont.truetype(F + "Georgia.ttf", int(s * 0.62))
        dd.text((s / 2, s * 0.53), "5", font=f, fill=(212, 180, 106), anchor="mm")
        ic.resize((size, size), Image.LANCZOS).save(root / name)
    Image.open(root / "favicon-48.png").save(root / "favicon.ico", sizes=[(48, 48)])
except Exception as e:
    print("images skipped:", e)

print(f"built lv/en/ru + {OFFLINE_NAME} ({(root / OFFLINE_NAME).stat().st_size/1e6:.2f} MB) · BASE = {BASE}")
