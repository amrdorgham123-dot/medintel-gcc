"""
Specs batch continuing product specs_json population. Covers Chrono-log
Model 490 4+4 Optical Aggregometer (platelet aggregation).

Run once: python3 populate_specs_batch_2025i.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    94: {  # Model 490 4+4 Optical Aggregometer
        "Configuration": "Modular optical aggregation system -- Model 490 4+ (4-channel base module) expandable to a full 8-channel system (490 4+4) with the 490 +4 expansion module and a single interconnecting cable",
        "Sample requirement": "Standard 500 uL platelet-rich plasma (PRP) sample, or a micro-volume 250 uL sample -- reducing blood draw from the standard 20-30 mL down to 8-10 mL, with reagent costs cut in half at the lower volume",
        "Software": "Internal AGGRO/LINK Opti8 computer interface running two software packages: AGGRO/LINK Opti8 for aggregation testing and vW CoFactor Opti8 for the Ristocetin CoFactor assay; supports up to 8 simultaneous platelet aggregation tests",
        "Standard test panel": "A complete panel in one run typically includes Collagen, ADP (x2), Arachidonic Acid, Epinephrine, Ristocetin (x2), and one other reagent",
        "Regulatory status": "FDA-cleared for in-vitro diagnostic use measuring platelet aggregation in platelet-rich plasma via light transmission aggregometry",
        "Output": "Results via a strip chart recorder or Chrono-log-provided computer software",
        "Source": "Chrono-log Corporation official product pages (chronolog.com/Model490_4-4.html; chronolog.com/spec.htm) and FDA 510(k) summary for the Model 490 4+4 (accessdata.fda.gov/cdrh_docs/pdf16/K161329.pdf)",
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
