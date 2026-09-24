# Trīs Maisi — Arsenāla iela 5, Rīga

Vizītkartes lapa vēsturiskajam noliktavu kompleksam Arsenāla ielā 5 (Vecrīga). LV / EN / RU.

## Faili
- `index.html` — **gatavā lapa** (visi attēli iešūti base64, fails pašpietiekams — to var sūtīt vienu pašu).
- `src.html` — avota fails, ko rediģē (attēli norādīti kā `assets/*.jpg`).
- `build.py` — `src.html` → `index.html` (iešuj attēlus).
- `assets/` — oriģinālie attēli (fotogrāfijas, plāni, griezums, fasāde).

## Rediģēšana
1. Labo `src.html` (teksti LV — HTML; EN/RU — `I18N` objektā skriptā; plānu tabulas — `PLANS`).
2. `python3 build.py`
3. Lokāli apskatīt: `python3 -m http.server 8765` → http://localhost:8765

## Avoti
- *Arsenala_5_New Look.pdf* — skiču projekts.
- *Business_Plan_Tris_Maisi_RU.pdf* — CAPEX, GDV, ROI/IRR, stratēģijas.

## Aizvietojamie dati
- Kontakti: `info@arsenala5.lv`, `+371 20 000 000` — placeholder.
