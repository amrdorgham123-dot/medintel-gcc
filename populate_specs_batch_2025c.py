"""
Specs batch continuing product specs_json population. Covers Beckman
Coulter DxH 500 (compact low-volume hematology analyzer).

Run once: python3 populate_specs_batch_2025c.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    16: {  # Beckman Coulter DxH 500
        "Target setting": "Low-volume labs -- physician offices, small/specialty clinics, pediatric and geriatric patients where sample draw is difficult",
        "Throughput": "Up to 60 samples/hour",
        "Sample volume": "12 uL of venous or micro-collected (fingerstick) whole blood; 20 uL for pre-dilute analysis",
        "Sample handling": "Open-vial sampling (no cap-piercing model available)",
        "Parameters": "CBC + full 5-part WBC differential: WBC, RBC, HGB, HCT, MCV, MCH, MCHC, RDW-SD, RDW-CV, PLT, MPV, and 5-part differential (LY/MO/NE/EO/BA, % and #)",
        "Reagents": "Cyanide-, azide-, and formaldehyde-free reagents; uses ~50% less reagent than comparable analyzers, with all 3 reagents changeable in under 5 minutes",
        "Interface": "Simplified touchscreen interface (any function in 3 touches or less); bi-directional LIS interface for paperless workflow",
        "Platform family": "First model in the DxH 500 Series (DxH 500, DxH 520, DxH 560), sharing Beckman Coulter's multidimensional high-definition flow cytometric cellular analysis technology used across the broader DxH line",
        "Validation": "Multi-site clinical reliability study: 36,000 samples run across 26 sites on 5 continents prior to launch",
        "Source": "Beckman Coulter official product page (beckmancoulter.com/products/hematology/dxh-500); SelectScience launch coverage (selectscience.net/article/beckman-coulter-releases-compact-dxh-500-hematology-system-with-ce-mark); LabWrench technical listing (labwrench.com/equipment/25316/beckman-coulter-dxh-500)",
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
