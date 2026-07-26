"""
Specs batch continuing product specs_json population. Covers Beckman
Coulter DxFLEX (clinical flow cytometer) and the ClearLLab 10C Reagent
System used with it.

Run once: python3 populate_specs_batch_2025d.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    176: {  # Beckman Coulter DxFLEX
        "Configurations": "Seven configurations available, from a 3-laser/10-color system up to a 3-laser/13-color configuration",
        "Detector technology": "Avalanche photodiode (APD) detectors instead of traditional photomultiplier tubes (PMT) -- quantum efficiency >80%, especially for red/far-red wavelengths, giving higher sensitivity and less noise",
        "Regulatory status": "FDA 510(k)-cleared and CE-marked for 10-color IVD use with the ClearLLab 10C Reagent System (channels FL11-FL13 and other applications are Research Use Only in the US)",
        "Clinical application": "The only FDA-cleared and CE-marked integrated leukemia/lymphoma immunophenotyping solution combining quality controls, sample prep, antibody panels, analysis software, and training material -- supports workup of chronic leukemia, myeloma, acute leukemia, non-Hodgkin lymphoma, myeloproliferative neoplasm, and myelodysplastic syndrome",
        "Software": "CytExpert acquisition/analysis software with a dynamic compensation library that simplifies gain-independent compensation setup",
        "Form factor": "Compact benchtop design",
        "Source": "Beckman Coulter official DxFLEX product page (beckman.com/flow-cytometry/clinical-flow-cytometers/dxflex) and SelectScience FDA clearance coverage (selectscience.net/article/fda-clears-beckman-coulter-life-sciences-dxflex-flow-cytometer)",
    },
    177: {  # ClearLLab 10C Reagent System
        "Function": "FDA-cleared, CE-marked 10-color antibody reagent panel system for clinical immunophenotyping on the DxFLEX flow cytometer",
        "Application": "Leukemia and lymphoma immunophenotyping -- part of the only FDA-cleared and CE-marked integrated solution combining reagents, quality controls, sample preparation, analysis software, and training material for this workflow",
        "Clinical use": "Supports diagnostic workup of chronic leukemia, myeloma, acute leukemia, non-Hodgkin lymphoma, myeloproliferative neoplasm, and myelodysplastic syndrome",
        "Compatibility": "Validated specifically for 10-color IVD use on the DxFLEX Clinical Flow Cytometer",
        "Source": "Beckman Coulter official DxFLEX product page (beckman.com/flow-cytometry/clinical-flow-cytometers/dxflex) and Today's Clinical Lab FDA clearance coverage (clinicallab.com/fda-clears-beckman-coulter-life-sciences-dxflex-flow-cytometer-27797)",
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
