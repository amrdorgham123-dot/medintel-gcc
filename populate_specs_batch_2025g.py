"""
Specs batch continuing product specs_json population. Covers Abbott
CellDyn Ruby / CellDyn Emerald hematology analyzers and Beckman Coulter
AU/DXC (AU5800 series) chemistry analyzers.

Run once: python3 populate_specs_batch_2025g.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    32: {  # CellDyn Ruby / CellDyn Emerald
        "Platform family": "Abbott CELL-DYN hematology line -- Ruby (medium-volume labs) and Emerald (physician office/small-volume labs)",
        "CellDyn Ruby": "5-part WBC differential, 22 assays, up to 84 CBCs/differentials per hour, open reagent system",
        "CellDyn Emerald": "3-part WBC differential, 18 assays, up to 57 tests/hour, open reagent system, designed for physician office or small-volume clinical labs",
        "Detection technology (Ruby)": "MAPSS (Multi-Angle Polarized Scatter Separation) optical laser light scatter technology for WBC differentiation, cell-by-cell analysis from a single dilution",
        "Connectivity": "Can integrate with AlinIQ AMS (Analyzer Management System) for centralized data flow management across the laboratory",
        "Source": "Abbott Core Laboratory official product pages (corelaboratory.abbott/int/en/offerings/brands/cell-dyn/cell-dyn-ruby.html; corelaboratory.abbott/us/en/offerings/brands/cell-dyn/cell-dyn-emerald.html); Diamond Diagnostics and GMI refurbisher technical listings confirming throughput/assay-menu figures",
    },
    17: {  # Beckman Coulter AU/DXC (AU5800 series)
        "Platform family": "AU5800 series -- AU5810 (entry-level, no ISE module), AU5820, AU5830, AU5840 -- modular high/ultra-high-volume clinical chemistry analyzers",
        "Throughput": "Up to 2,000 tests/hour per module (highest-throughput model in the AU5800 series)",
        "Modularity": "Connect up to 4 analytical modules to scale capacity as volume grows",
        "Test menu": "Full clinical chemistry menu including Therapeutic Drug Monitoring (TDM) and Drugs of Abuse (DOA) panels",
        "Workflow features": "Intelligent sample management system optimizes rack processing based on tests ordered; STAT priority testing with auto-repeat of abnormal results",
        "Integration": "Can be configured with pre-analytical automation, immunoassay systems, and clinical IT for a total laboratory solution",
        "Source": "Beckman Coulter official AU5800 product page (beckmancoulter.com/products/chemistry/au5800); Block Scientific technical/market comparison listing (blockscientific.com/beckman-au-5810) confirming AU5810 throughput and positioning within the series",
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
