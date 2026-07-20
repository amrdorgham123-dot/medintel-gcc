"""
Session 9 batch continuing specs_json population. Covers Terumo BCT Trima
Accel automated blood collection system and Spectra Optia apheresis
system.

Run once: python3 populate_specs_session9.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    40: {  # Trima Accel
        "Function": "Automated blood collection system for donor apheresis (platelets, plasma, red cells, and combination collections)",
        "Current generation": "Trima Accel 7 -- updated platelet collection software algorithms that better account for splenic platelet mobilization and more accurately predict post-collection donor platelet counts, supporting safe collection of more platelets per donor",
        "Workflow improvements": "Improved LRS chamber management and channel setup to help shorten procedure times",
        "Software/data": "Compatible with EMPOWERD Data Management Software and the Trima KPI Dashboard for operational efficiency tracking and compliance documentation",
        "Source": "Terumo BCT official Trima Accel product page (terumobct.com/en/gl/products-services/global-blood-solutions/global-blood-solutions-products/trima.html); Trima Accel 7 technical brochure (pdf.medicalexpo.com/pdf/terumo-bct/trima-accel-7/75244-207639.html)",
    },
    41: {  # Spectra Optia
        "Function": "Apheresis platform supporting a broad range of protocols: therapeutic plasma exchange (TPE), red blood cell exchange, and cell collection procedures (including for cell therapy manufacturing)",
        "Physical dimensions": "Weight 91.6 kg (220 lbs); height 115.6 cm (45.5 in) with IV pole lowered, 174 cm (68.5 in) with IV pole extended",
        "Mobility": "Folding screen for simplified moving/storage; large durable wheels on pivoting casters with an advanced wheel pedal for moving or securing the system",
        "Indications": "Used across therapeutic apheresis (e.g., sickle cell disease transfusion therapy) and cell collection applications supporting cell and gene therapy manufacturing",
        "Software": "Compatible with EMPOWERD Data Management Software for automated data capture and transfer",
        "Source": "Terumo BCT official Spectra Optia product page (terumobct.com/en/gl/products-services/therapeutic-apheresis/therapeutic-apheresis-products--indications--and-protocols/spectra-optia-apheresis-system.html); official technical catalog (pdf.medicalexpo.com/pdf/terumo-bct/spectra-optia/75244-236052.html); FDA-submitted Operator's Manual (fda.gov/media/136838/download)",
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
