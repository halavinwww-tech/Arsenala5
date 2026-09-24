# Trīs Maisi — Arsenāla iela 5, Rīga

Vizītkartes lapa vēsturiskajam noliktavu kompleksam Arsenāla ielā 5 (Vecrīga). LV / EN / RU.

## Faili
- `index.html` — **gatavā lapa** (visi attēli iešūti base64, fails pašpietiekams — to var sūtīt vienu pašu).
- `src.html` — avota fails, ko rediģē (attēli norādīti kā `assets/*.jpg`).
- `privacy.src.html` → `privacy.html` — privātuma politika (LV/EN/RU).
- `build.py` — būvē visu: `index.html`, `privacy.html`, `robots.txt`, `sitemap.xml`, `llms.txt`, `og-cover.jpg`.
  Vietnes adrese ir mainīgajā `BASE` build.py sākumā — mainot domēnu, nomaini tikai to.
- `assets/` — oriģinālie attēli (fotogrāfijas, plāni, griezums, fasāde).

## Rediģēšana
1. Labo `src.html` / `privacy.src.html` (nekad nelabo ģenerētos failus tieši) (teksti LV — HTML; EN/RU — `I18N` objektā skriptā; plānu tabulas — `PLANS`).
2. `python3 build.py`
3. Lokāli apskatīt: `python3 -m http.server 8765` → http://localhost:8765

## Avoti
- *Arsenala_5_New Look.pdf* — skiču projekts.
- *Business_Plan_Tris_Maisi_RU.pdf* — CAPEX, GDV, ROI/IRR, stratēģijas.

## SEO / GEO
- Meta, Open Graph, Twitter kartīte, canonical, geo meta tagi.
- JSON-LD: Organization, WebSite, LandmarksOrHistoricalBuildings, FAQPage.
- Redzama BUJ sadaļa (LV/EN/RU), `llms.txt` ar faktiem AI meklētājiem, `sitemap.xml`, `robots.txt`.

## Aizvietojamie dati
- E-pasts pagaidām nav norādīts (tiks pievienots, kad būs īstais).
