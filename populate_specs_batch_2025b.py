"""
Specs batch continuing product specs_json population. Covers Dymind
DH76 (5-part hematology) and DH36 (3-part hematology) analyzers.

Run once: python3 populate_specs_batch_2025b.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    70: {  # Dymind DH76
        "Differential": "5-part WBC differential",
        "Throughput": "Up to 90 tests/hour",
        "Detection technology": "Flow cytometry (semiconductor laser) + tri-angle laser scatter + electrical impedance (RBC/PLT) + cyanide-free HGB method",
        "Parameters": "29 parameters (25 reportable + 4 research: ALY#/%, LIC#/%)",
        "Sample modes": "Whole blood, capillary whole blood, and pre-diluted modes",
        "Independent verification": "A published comparison study (PMC) found excellent correlation with the Sysmex XN-1000 (R2: WBC 1.000, RBC 0.999, hemoglobin 0.999, PLT >50x10^9/L 0.994) and within-run CVs of 0.02-2.5% for most parameters",
        "Source": "Dymind official product page (dymind.com/en-US/products/105); MedicalExpo technical listing (medicalexpo.com/prod/shenzhen-dymind-biotechnology-co-ltd/product-104253-679187.html); PMC independent evaluation study (pmc.ncbi.nlm.nih.gov/articles/PMC8451233/)",
    },
    71: {  # Dymind DH36
        "Differential": "3-part WBC differential",
        "Throughput": "Up to 60 tests/hour",
        "Detection technology": "Electrical impedance method (WBC/RBC/PLT) + cyanide-free HGB method, with pulse baseline tracking and digital sheath flow technology",
        "Parameters": "Up to 50 parameters (some listings cite 21 core reportable parameters depending on configuration)",
        "Sample volume": "Only 9 uL sample required",
        "Sample modes": "Venous whole blood, anticoagulated peripheral whole blood, and pre-diluted blood",
        "Data storage": "Up to 50,000 sample results including parameters, histograms, and patient information",
        "Source": "Dymind official product page (dymind.com/en-US/products/91); MedicalExpo technical listing (trends.medicalexpo.com/shenzhen-dymind-biotechnology-co-ltd/project-104253-413069.html)",
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
