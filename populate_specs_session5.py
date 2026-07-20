"""
Session 5 batch continuing specs_json population. Covers BD Bruker MALDI
Biotyper CA System (microbial identification) and BD Phoenix M50
(automated identification/antimicrobial susceptibility testing).

Run once: python3 populate_specs_session5.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    144: {  # BD Bruker MALDI Biotyper CA System
        "Technology": "MALDI-TOF mass spectrometry (matrix-assisted laser desorption/ionization time-of-flight) for microbial identification",
        "Available configurations": "Sirius and Sirius One bench top models -- improved throughput and reduced footprint versus prior generations",
        "Reference library": "Over 400 organisms in the FDA-approved identification library",
        "Result time": "Identification in minutes; with the MBT Sepsityper IVD kit, results directly from positive blood cultures in under 30 minutes",
        "Testing modes": "Batch or random-access testing",
        "Connectivity": "Connects to the BD Phoenix M50 system and BD BACTEC FX Blood Culture System via BD informatics for an integrated microbiology workflow; supported by BD EpiCenter Microbiology Data Management System for MALDI plate mapping",
        "Source": "BD official product page (bd.com/en-us/products-and-solutions/products/product-families/bd-bruker-maldi-biotyper-ca-system); Cardinal Health technical listing",
    },
    143: {  # BD Phoenix M50
        "Function": "Automated bacterial/yeast identification (ID) and antimicrobial susceptibility testing (AST) system",
        "AST methodology": "True minimum inhibitory concentration (MIC) results from doubling antibiotic concentration dilutions, with every well read (no extrapolated results)",
        "Performance": "Demonstrated approximately 50% lower rate of Very Major Errors (VMEs) for gram-negative organisms compared to a competing ID/AST platform in BD-reported comparisons",
        "Integration": "Connects with the BD Bruker MALDI Biotyper CA System and BD BACTEC FX Blood Culture System via BD informatics/EpiCenter for an integrated microbiology workflow",
        "Source": "BD official Automated Identification and Susceptibility Testing Solutions page (bd.com/en-us/products-and-solutions/solutions/capabilities/bd-automated-identification-and-susceptibility-testing-solutions)",
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
