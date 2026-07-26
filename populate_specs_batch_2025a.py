"""
Specs batch continuing product specs_json population. Covers Abbott
Alinity s (blood/plasma donor screening system), Abbott Alinity hs
(hematology slide maker/stainer module), and Eppendorf 5810 R / MiniSpin
centrifuges.

Run once: python3 populate_specs_batch_2025a.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    30: {  # Abbott Alinity S
        "Application": "High-throughput blood and plasma donor screening -- detects antigens and antibodies (e.g. HIV Ag/Ab Combo, HBsAg + confirmatory, Anti-HCV, HTLV I/II, Chagas, Anti-HBc) to help protect the blood/plasma supply",
        "Throughput": "Up to 600 tests/hour",
        "Detection technology": "Chemiluminescent microparticle immunoassay (CMIA)",
        "Walkaway time": "Minimum 3 hours, with continuous access for the technician to refill/restock without pausing the system",
        "Workflow": "Continuous access and automated retesting; tracks all activities associated with testing/processing of each donation per regulatory requirements",
        "Regulatory status": "FDA-approved (2019) for screening the US blood and plasma supply",
        "Source": "Abbott official press releases (abbott.mediaroom.com/2019-07-11-Abbott-Announces-FDA-Approval-of-the-Alinity-TM-s-System; abbott.mediaroom.com covering the 2020 launch) and Abbott Transfusion Medicine harmonized systems page (transfusion.abbott/us/en/about-us/harmonized-systems.html)",
    },
    31: {  # Abbott Alinity HS (slide maker/stainer module)
        "Function": "Automated blood film slide maker and stainer module, paired with the Alinity hq hematology analyzer to form the Alinity h-series integrated system",
        "Integration": "Bi-directional internal conveyor links hq (CBC analysis) and hs (slide making/staining) into one workflow; can also stain externally prepared blood films",
        "Throughput (combined h-series system)": "125-133 complete blood counts (CBCs) per m2 of footprint -- reported as up to 20% faster per m2 than other integrated hematology systems available at launch",
        "Footprint": "Compact, space-efficient design intended to maximize throughput per unit of lab floor space",
        "Source": "Abbott official press release (abbott.mediaroom.com/2018-01-02-Abbott-Launches-Alinity-TM-h-series-Integrated-Hematology-System) and Abbott Core Laboratory Alinity h-series page (corelaboratory.abbott/int/en/offerings/brands/alinity/Alinity-h-hematology-system.html)",
    },
    201: {  # Eppendorf Centrifuge 5810 R
        "Type": "Refrigerated benchtop multipurpose centrifuge for medium-to-high-throughput labs",
        "Max speed / RCF": "Up to 14,000 rpm / 20,913 x g (rotor-dependent; swing-bucket rotor S-4-104 typically runs lower, e.g. ~4,000 rpm / ~3,220 x g)",
        "Capacity": "Rotor S-4-104 accommodates tubes and bottles from 0.2 mL to 750 mL, plus microplates (PCR, cell culture, deep-well); blood collection tube capacity up to 100 x 13mm or 80 x 16mm",
        "Rotor options": "Swing-bucket (S-4-104), fixed-angle, and plate rotors (581x) available for different sample formats",
        "Features": "Aerosol-tight Eppendorf QuickLock caps/lids available for biohazard containment",
        "Dimensions": "700 x 608 x 345 mm (W x D x H)",
        "Source": "NIST laboratory equipment listing (nist.gov/laboratories/tools-instruments/eppendorf-5810r-centrifuge) and Eppendorf official product page (eppendorf.com/us-en/Products/Centrifugation/Multipurpose-Centrifuges/Centrifuge-5810-5810R-p-PF-240994)",
    },
    202: {  # Eppendorf MiniSpin / MiniSpin plus
        "Type": "Entry-level personal microcentrifuge for molecular biology and small-volume clinical applications",
        "Max capacity": "12 x 2 mL tubes",
        "Max RCF": "MiniSpin: 12,100 x g; MiniSpin plus: 14,100 x g",
        "Max speed": "MiniSpin: 13,400 rpm; MiniSpin plus: 14,500 rpm",
        "Refrigeration": "Not refrigerated (room-temperature operation only)",
        "Noise level": "49 dB(A) (MiniSpin) / 52 dB(A) (MiniSpin plus)",
        "Source": "Eppendorf official centrifuges comparison guide (yumpu.com/en/document/view/12347208/eppendorfr-centrifuges-guide)",
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
