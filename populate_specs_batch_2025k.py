"""
Specs batch continuing product specs_json population. Covers BD
Multitest / BD Trucount Tubes (flow cytometry reagent), Azbil Telstar
Bio II Advance biosafety cabinet, and Telstar LyoBeta freeze dryer.

Run once: python3 populate_specs_batch_2025k.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    175: {  # BD Multitest Reagents / BD Trucount Tubes
        "Function": "Reagent + bead-based reference system for absolute lymphocyte subset counting (immunophenotyping) by flow cytometry",
        "Application": "BD Multitest 6-Color TBNK -- determines percentages and absolute counts of T, B, and NK lymphocyte subsets in peripheral whole blood; used with BD FACSLyric, BD FACSCanto II, and BD FACSCanto flow cytometers",
        "Trucount Tubes": "Contain a known, pouch-labeled count of lyophilized fluorescent reference beads; suspended in the sample upon reagent/blood addition, letting the flow cytometer software calculate absolute cell counts directly from bead:cell ratio",
        "Kit format": "Supplied as 2 pouches of 25 tubes each (50 tests total per kit)",
        "Storage": "2-8 degC",
        "Regulatory note": "FDA Class 2 recall history (Z-0173-2023, initiated Oct 2022) for partial label detachment on Trucount tubes causing automation/pouch-sticking issues -- corrected via lot-specific customer notification; relevant for any facility auditing lot numbers 11568, 45905, 53637, 88003, 89111, 31905",
        "Source": "BD official Trucount Tubes product page and package insert (bdbiosciences.com; 23-3483.pdf) and FDA recall record (accessdata.fda.gov/scripts/cdrh/cfdocs/cfRES/res.cfm?id=196097)",
    },
    213: {  # Bio II Advance Biosafety Cabinet
        "Class": "Class II Biological Safety Cabinet",
        "Biosafety levels": "Suitable for work with biological agents at levels 1, 2, and 3",
        "Protection": "Triple protection design -- protects the user, the product/sample, and the environment simultaneously",
        "Manufacturer": "Azbil Telstar (Terrassa, Spain)",
        "Configurations": "Available in multiple width/model variants (e.g. Bio II Advance 6) to fit different bench footprints",
        "Source": "Telstar official Class II biosafety cabinet page (telstar.com/en/laboratory-equipment/biological-laminar-flow-cabinets/class-ii-microbiological-safety-cabinet/) and distributor listings (medsolut.com, geminibv.com)",
    },
    214: {  # LyoBeta Freeze Dryer Series
        "Function": "Freeze-drying (lyophilization) unit for biological, pharmaceutical, and food product formulation and scale-up work, supporting technology transfer to R&D centers",
        "Design": "GLP-compliant design; fully automated freeze-drying process with accurate monitoring; compact, casters-mounted, self-standing unit for easy installation",
        "Model range": "Four different models available, up to 0.9 m2 of shelf area, with air- or water-cooled condenser options",
        "Performance": "Shelf heating/cooling rate of approximately 1 degC/min; temperature uniformity via shelf flatness and high-quality shelf/product/condenser temperature sensors",
        "Features": "Recipe optimization and development capability; temperature, pressure, and time control system; option to sterilize with VHP (vaporized hydrogen peroxide); adaptable for use with solvents",
        "Target applications": "R&D biotech, clinical, and pharmaceutical formulation studies; scale-up recipe development for different vial sizes and bulk product",
        "Source": "Telstar official LyoBeta product page (telstar.com/en/laboratory-equipment/laboratory-freeze-dryers/advance-reserach-scale-up-freeze-dryer/) and News-Medical manufacturer listing (news-medical.net/LyoBeta-Laboratory-Freeze-Dryer-from-Telstar)",
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
