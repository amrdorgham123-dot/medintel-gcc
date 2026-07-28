"""
Specs batch continuing product specs_json population. Covers 77
Elektronika's Fully Automated Urine Analyzer + Test Strips (LabUMat 2 /
UriSed platform) and Diagnostica Stago sthemO hemostasis analyzer
family (sthemO 301 / 201).

Run once: python3 populate_specs_batch_2025n.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    147: {  # 77 Elektronika Fully Automated Urine Analyzer + Test Strips
        "Platform family": "LabUMat 2 (chemistry) + UriSed (sediment) -- combinable into a Complete Urine Laboratory System, plus the UriSed Cascade fully integrated configuration",
        "Chemistry throughput (LabUMat 2)": "Up to 240 tests/hour, evaluating 10 chemical parameters from LabStrip U11 Plus GL test strips plus 3 physical parameters of the urine sample",
        "Combined throughput (UriSed Cascade)": "Up to 200 urine samples/hour for combined chemistry + sediment results",
        "Sediment detection technology": "Patented UriSed technology -- automation of traditional manual microscopy; performs sample preparation, captures multiple whole-field-of-view images through a built-in microscope, and evaluates them via the Auto Image Evaluation Module (AIEM) image-processing software, without special liquid reagents",
        "Connectivity": "Unidirectional/bidirectional LIS interface; automated QC analysis and self-check; software/language upgrades via USB",
        "Manufacturer background": "77 Elektronika Kft., founded 1986 in Hungary (EU); ISO 9001, ISO 13485, and ISO 14001 certified; products CE-marked under IVD Directive 98/79/EC; 2018 revenue ~EUR 100 million with products distributed in ~100 countries (own brand plus OEM/ODM for multinational partners)",
        "Source": "77 Elektronika official site (en.e77.hu; en.e77.hu/products/urine-analyzers) and HealthManagement.org product/company listings (healthmanagement.org/products/view/automatic-urine-analyzer-labumat-2-77-elektronika; healthmanagement.org/site/p/77-elektronika-kft)",
    },
    25: {  # STheMO
        "Platform family": "sthemO family -- sthemO 301 and sthemO 201, sharing the same analytical core, reagents/consumables, and ergonomic software across both models (train once to operate either)",
        "Function": "Quantitative automated hemostasis (coagulation) analyzer platform for in vitro diagnostic use by clinical laboratory personnel",
        "Reagents": "Used exclusively with dedicated sthemO reagents and controls",
        "Data management": "sthemE Manager software -- manages data/information flow between one or several IVD analyzers and laboratory information systems (LIS)",
        "Manufacturer": "Diagnostica Stago (France)",
        "Source": "Diagnostica Stago official sthemO product site (sthemo.stago.com)",
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
