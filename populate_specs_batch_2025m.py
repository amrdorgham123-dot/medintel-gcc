"""
Specs batch continuing product specs_json population. Covers DiaSorin
LIAISON Calprotectin (fecal calprotectin immunoassay for IBD).

Run once: python3 populate_specs_batch_2025m.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    166: {  # LIAISON Calprotectin
        "Function": "Fecal calprotectin immunoassay -- non-invasive aid in the diagnosis of inflammatory bowel disease (IBD, specifically Crohn's disease and ulcerative colitis) and in differentiating IBD from irritable bowel syndrome (IBS)",
        "Platform": "Fully automated chemiluminescence immunoassay (CLIA), run on the DiaSorin LIAISON XL analyzer",
        "Analyte": "Calprotectin (S100A8/S100A9) -- a calcium/zinc-binding neutrophil protein elevated in intestinal inflammation",
        "Linearity": "Verified up to 2,000 ng/mL in independent validation studies",
        "Clinical performance": "Independent studies report significantly higher fecal calprotectin in IBD patients vs. controls (e.g. ulcerative colitis ~710 +/- 921 mg/kg, Crohn's disease ~967 +/- 1243 mg/kg, vs. ~11 +/- 8 mg/kg in controls), with good analytical agreement against ELISA-based comparator methods in comparative studies",
        "Interference note": "Presence of blood in the stool sample can interfere with calprotectin measurement, per independent validation research",
        "Workflow benefit": "Full automation on LIAISON XL allows harmonization of urgent, specialty, and routine immunoassay testing on one platform rather than a separate manual ELISA workflow",
        "Source": "DiaSorin official LIAISON Calprotectin product page (us.diasorin.com/en/immunodiagnostics/gastrointestinal-diseases/liaisonr-calprotectin) and independent peer-reviewed validation studies (PMC7327250, PMC10724856)",
    },
}

def main():
    conn = sqlite3.connect(DB_PATH)
    updated, skipped = 0, 0
    for pid, specs in SPECS.items():
        row = conn.execute("SELECT id, product_name, specs_json FROM products WHERE id = ?", (pid,)).fetchone()
        if not row:
            print(f"SKIP (not found): id={pid}")
            skipped += 1
            continue
        existing_specs = row[2]
        if existing_specs and existing_specs not in ("", "{}", "[]"):
            print(f"SKIP (already has specs_json): id={pid} ({row[1]})")
            skipped += 1
            continue
        conn.execute("UPDATE products SET specs_json = ? WHERE id = ?", (json.dumps(specs), pid))
        print(f"UPDATED: id={pid} ({row[1]})")
        updated += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Updated: {updated}, Skipped: {skipped}")

if __name__ == "__main__":
    main()
