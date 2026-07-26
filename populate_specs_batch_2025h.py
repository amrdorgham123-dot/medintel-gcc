"""
Specs batch continuing product specs_json population. Covers Bio-Rad
IH-500 fully automated blood typing/immunohematology system.

Run once: python3 populate_specs_batch_2025h.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    2: {  # Bio-Rad IH-500
        "Function": "Fully automated, random-access blood typing and antibody screening system for small-to-medium-size transfusion medicine laboratories",
        "Test menu": "ABO blood grouping, reverse typing, Rh(D) including weak D and partial D, Rh phenotype and Kell blood grouping, antibody screening and identification of RBC alloantibodies, single antigen testing, crossmatch, auto control, and direct antiglobulin testing (DAT)",
        "Technology": "Uses Bio-Rad's ID-Card gel card technology; automates pipetting of samples/reagents, incubation, centrifugation, and provides reaction grading/interpretation from gel card images",
        "Automation": "6-axis industrial robot transport arm for maintenance-free sample/reagent handling; designed for 24/7 walk-away operation",
        "Form factor": "Compact benchtop system; can be paired with an optional stand-alone table for added flexibility",
        "Newer variant": "IH-500 NEXT System adds automated titration for gel cards, the IH-AbID software module for antibody identification, and up to 7-day/24-hour onboard liquid reagent storage with improved stability",
        "Regulatory status": "FDA-cleared via 510(k) (BK180274); in the US, Rx only, for use by trained personnel only, with Bio-Rad-authorized gel cards and reagents",
        "Source": "Bio-Rad official IH-500 and IH-500 NEXT product pages (bio-rad.com/en-us/product/ih-500-system; bio-rad.com/en-us/product/ih-500-next-system); FDA 510(k) summary (fda.gov/files/vaccines,%20blood%20&%20biologics/published/BK180274Summary.pdf); SelectScience launch coverage",
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
