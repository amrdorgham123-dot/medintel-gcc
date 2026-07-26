"""
Specs batch continuing product specs_json population. Covers
Diagnostica Stago STA Compact (base) and STA Compact Max coagulation
analyzers.

Run once: python3 populate_specs_batch_2025e.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    24: {  # STA Compact
        "Platform family": "STA Compact line -- base STA Compact and higher-throughput STA Compact Max models",
        "Throughput (base STA Compact)": "Up to 100 tests/hour, 19-assay menu, 96 sample positions, 45 reagent positions",
        "Throughput (STA Compact Max)": "Up to 150 tests/hour with an expanded test menu, same 96 sample / 45 reagent position capacity",
        "Detection method": "Colorimetric spectrophotometric optical system with tungsten-halogen lamp illumination",
        "Sample handling": "Direct STAT sample access with no impact on time-to-result for routine samples; optional cap-piercing system available (Compact Max) to reduce biohazard exposure",
        "Software (Compact Max)": "STA Coag Expert software -- full auto-verification, repeat/reflex testing, comprehensive QC package, accreditation tools, automated maintenance logs, TAT monitoring, and 5-year onboard patient archive",
        "Sample volume": "5-8 uL per test (base model)",
        "Target setting": "Small to mid-sized laboratories needing a benchtop coagulation solution with STAT prioritization",
        "Source": "Stago official STA Compact Max product page (stago-us.com/products-services/hemostasis-systems/sta-compact-max/); Diamond Diagnostics and STEMart refurbisher technical listings confirming throughput/capacity figures for both STA Compact and STA Compact Max",
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
