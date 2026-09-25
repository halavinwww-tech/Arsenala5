# Trīs Maisi — Arsenāla iela 5, Rīga

Vietne: **https://arsenala5.lv/** (LV) · **/en/** · **/ru/** — GitHub Pages, īpašnieks SIA «Arsenāla 5».

## Faili
- `src.html` — **vienīgais lapas avots**: LV teksts HTML, EN/RU tulkojumi `I18N` objektā skriptā, plānu tabulas `PLANS`.
- `privacy.src.html` — privātuma politika (LV/EN/RU vienā lapā, `?lang=en|ru`).
- `build.py` — ģenerē visu pārējo (nelabo ģenerētos failus ar roku):
  - `index.html`, `en/index.html`, `ru/index.html` — katrai valodai sava indeksējama lapa ar hreflang;
  - `privacy.html`, `404.html`, `robots.txt`, `sitemap.xml` (ar hreflang), `llms.txt`, `og-cover.jpg`, favicon faili;
  - `Arsenala5-Tris-Maisi.html` — **viens pašpietiekams fails sūtīšanai** (attēli iešūti, valodu pārslēgs strādā bez interneta). Nav repo (.gitignore).
- `assets/` — attēli (vietnē tiek ielādēti kā atsevišķi faili — ātrāka lapa, labāks SEO).
- `CNAME` — domēns arsenala5.lv.
- `<atslēga>.txt` + `.indexnow-key` — IndexNow atslēga (Bing/Yandex/Seznam ātrai indeksēšanai).

## Rediģēšana
1. Labo `src.html` / `privacy.src.html`.
2. `python3 build.py`
3. Lokāli: `python3 -m http.server 8765` → http://localhost:8765
4. `git add -A && git commit && git push`

## SEO / GEO
- Atsevišķi URL katrai valodai, `hreflang` + `x-default`, lokalizēti title/description/OG/Twitter.
- JSON-LD: Organization, WebSite, LandmarksOrHistoricalBuildings, FAQPage (katrā valodā).
- Redzama BUJ sadaļa, `llms.txt` ar faktiem AI meklētājiem, `sitemap.xml`, `robots.txt`, alt teksti attēliem.
- Jāizdara īpašniekam: Google Search Console un Bing Webmaster Tools — pievienot arsenala5.lv un iesniegt `https://arsenala5.lv/sitemap.xml`.

## DNS (NIC.LV)
4× A 185.199.108–111.153 · 4× AAAA 2606:50c0:8000–8003::153 · CNAME www → halavinwww-tech.github.io
