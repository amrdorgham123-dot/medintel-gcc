"""
Session 2b batch continuing specs_json population. Covers Abbott i-STAT
System, BD FACSLyric flow cytometer, Bio-Rad IH-1000 immunohematology
analyzer, and Beckman Coulter DxH 800 hematology analyzer.

Run once: python3 populate_specs_session2b.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    169: {  # Abbott i-STAT System
        "Format": "Handheld, portable point-of-care blood analyzer using single-use i-STAT test cartridges",
        "Sample volume": "2-3 drops of whole blood per test",
        "Result time": "A few minutes per test, at the patient's side",
        "Test menu": "Broad single-platform menu: blood gases, electrolytes, chemistries, lactate, cardiac markers, coagulation, hematology, and endocrine assays (cartridge-dependent)",
        "Dimensions": "Approximately 23.5 cm (L) x 7.7 cm (W) x 7.2 cm (D)",
        "Weight": "Approximately 650 g with rechargeable battery installed",
        "Connectivity": "Data management integration with Abbott Info HQ or AEGISPOC for LIS/EMR connectivity, operator control, and device oversight",
        "Source": "Abbott official i-STAT 1 product page (globalpointofcare.abbott/ww/en/product-details/apoc/i-stat-system.html); Abbott i-STAT 1 System Manual",
    },
    174: {  # BD FACSLyric
        "Classification": "Class 1 laser product flow cytometer",
        "Diagnostic configuration": "For In Vitro Diagnostic use with BD FACSuite Clinical Application, up to 6 colors",
        "Research configuration": "For Research Use Only with BD FACSuite Application, up to 12 colors (not for diagnostic/therapeutic use)",
        "Application areas": "Clinical and research immunophenotyping (e.g., lymphocyte subsetting, leukemia/lymphoma immunophenotyping) depending on configuration and reagents used",
        "Source": "BD Biosciences official technical specifications document (bdbiosciences.com/content/dam/bdb/marketing-documents/BD-FACSLyric-Tech-Specs.pdf)",
    },
    1: {  # Bio-Rad IH-1000
        "Format": "Fully automated, walk-away immunohematology (blood grouping/antibody) analyzer for ID-Cards",
        "Capacity": "180 samples, 240 ID-Cards, and 28 reagent vials onboard",
        "Workflow": "Continuous sample and reagent loading with random access (load samples at any time) and an automated backup system for continuous processing",
        "Automation": "6-axis industrial robot arm with maintenance-free transport technology",
        "Application": "ABO/Rh typing, antibody screening/identification, and extended phenotyping in transfusion medicine laboratories",
        "Source": "Bio-Rad official IH-1000 product page (c-e.am/en/product/ih-1000/) and Bio-Rad Immunohematology Systems overview (bio-rad.com/en-us/applications-technologies/immunohematology-systems)",
    },
    107: {  # Beckman Coulter DxH 800
        "Reagents": "Uses only 5 reagents for all analyses (including NRBC and reticulocytes), reducing inventory management",
        "Sample handling": "165 uL aspiration volume (open/closed vial system); 20 cassettes of 5-tube sample storage; handheld barcode scanner for specimen labels",
        "Detection technology": "Coulter Principle impedance combined with multi-angle laser light scatter and Automated Intelligent Morphology technology for first-pass accuracy",
        "Workcell configuration (DxH 2401)": "Up to 3 DxH 800 modules plus 1 Slidemaker Slidestainer; peak performance up to 300 samples and 140 slides per hour",
        "Additional testing": "Automatic reticulocyte and body fluid analysis without added personnel",
        "Source": "Beckman Coulter official DxH 800 product page (beckmancoulter.com/products/hematology/dxh-800); GMI technical listing confirming workcell throughput",
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
