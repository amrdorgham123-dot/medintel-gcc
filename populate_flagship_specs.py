"""
Populates specs_json for MedForsa GCC's flagship platform products with real,
sourced specifications pulled directly from official manufacturer pages
(snibe.com, sysmex.com, bd.com). No fabricated values -- every figure below
is drawn from the cited official source.

Run once: python3 populate_flagship_specs.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    # id 67: Snibe MAGLUMI X8 / X6 / X3 / X10 -- specs below are for the
    # flagship X8 model. Source: snibe.com official product page + Snibe
    # MedicalExpo listing (which mirrors the manufacturer's own spec sheet).
    67: {
        "Throughput (single module)": "Up to 600 tests/hour",
        "Throughput (4 modules combined)": "Up to 2,400 tests/hour",
        "Time to first result": "15 minutes",
        "Sample positions": "Up to 300",
        "Reagent positions": "42 on board",
        "Cuvette capacity": "Up to 2,912 (single-cup design)",
        "Test menu": "Up to 236 parameters",
        "Operating modes": "Random, Batch, and STAT",
        "Availability": "24 hours ready to use",
        "Reagent storage temp.": "2°C-8°C",
        "Source": "Snibe official product page (snibe.com/en/product/CLIA_analyzer/40.html)"
    },
    # id 104: Sysmex XN-1000 hematology analyzer.
    # Source: Sysmex America official product page (sysmex.com/en-us).
    104: {
        "Throughput (Whole Blood, CBC+DIFF)": "Up to 100 samples/hour per module",
        "Throughput (Body Fluid mode)": "Up to 40 samples/hour per module",
        "WBC linearity": "0.00-440.00 x10³/µL",
        "RBC linearity": "0.00-8.60 x10⁶/µL",
        "PLT linearity": "0-5,000 x10³/µL",
        "Detection principle": "Fluorescent flow cytometry (semiconductor laser, hydrodynamic focusing) + electrical impedance + SLS-Hb (cyanide-free)",
        "Key parameters": "WBC, RBC, HGB, HCT, MCV, MCH, MCHC, PLT (PLT-I/PLT-F), 5-part DIFF, IG#/%, NRBC#/%, RET#/%, IRF, RET-He, IPF#/%",
        "Source": "Sysmex America official product page (sysmex.com/en-us/lab-solutions/hematology/xn-series/xn-1000)"
    },
    # id 142: BD BACTEC FX / FX40 blood culture system.
    # Source: BD official product pages (bd.com).
    142: {
        "Configuration options": "FX40 (40 vials), FX Top Unit (200 vials), FX Stack (400 vials, 2 modules x 4 drawers x 100 vials)",
        "Max scalable capacity": "Up to 20 stack/top units integrated via BD EpiCenter (thousands of vials)",
        "Detection technology": "Fluorescence-based, continuous monitoring",
        "Workflow": "Vial-activated workflow with barcode scanner and LCD touchscreen per module",
        "Compatibility": "BD Vacutainer blood collection system-compatible bottles",
        "Design": "Compact, modular -- stackable for lab-size flexibility",
        "Source": "BD official product page (bd.com/en-us/products-and-solutions/products/product-families/bd-bactec-fx-blood-culture-system)"
    }
}

def main():
    conn = sqlite3.connect(DB_PATH)
    updated = 0
    for product_id, specs in SPECS.items():
        row = conn.execute("SELECT id, product_name FROM products WHERE id = ?", (product_id,)).fetchone()
        if not row:
            print(f"SKIP: product id {product_id} not found")
            continue
        conn.execute("UPDATE products SET specs_json = ? WHERE id = ?", (json.dumps(specs), product_id))
        print(f"UPDATED: id {product_id} -- {row[1]}")
        updated += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Updated: {updated}")

if __name__ == "__main__":
    main()
