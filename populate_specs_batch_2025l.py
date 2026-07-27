"""
Specs batch continuing product specs_json population. Covers Alba
Bioscience ALBAclone blood grouping antisera, Demophorius blood
collection bags (single/double/triple/quadruple), and DiaSorin LIAISON
QuantiFERON-TB Gold Plus.

Run once: python3 populate_specs_batch_2025l.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    135: {  # ALBAclone blood grouping antisera
        "Product range": "Broad FDA-licensed range of monoclonal/polyclonal blood grouping antisera, including Anti-A, Anti-B, Anti-A,B, Anti-D (Alpha and Beta clone blends), Anti-M, Anti-N, Anti-Le(b), and others",
        "Format": "For slide and tube agglutination techniques",
        "Regulatory status": "FDA-licensed (individual STN license numbers per antigen specificity) via the US Vaccines, Blood & Biologics pathway",
        "Application": "ABO/Rh forward grouping and extended antigen typing in transfusion medicine and immunohematology laboratories",
        "Manufacturer": "Alba Bioscience Limited (Scotland, UK) -- part of the ALBAclone/ALBAcyte/ALBAsera reagent families for blood grouping, screening, and antibody identification",
        "Source": "FDA official package inserts for individual ALBAclone reagents (fda.gov/files/vaccines,%20blood%20&%20biologics/published/Package-Insert---ALBAclone-...) and FDA Blood Grouping Reagents product listings (fda.gov/vaccines-blood-biologics/blood-grouping-reagents-anti-wra-albasera)",
    },
    59: {  # Blood collection bags (general/Demophorius)
        "Product family": "Demotek blood collection bag range -- single (BBS), double (BBD), triple (BBT/BBTTB), and quadruple (BBQ) configurations",
        "Anticoagulant": "CPDA-1 (Citrate Phosphate Dextrose Adenine) anticoagulant solution in the primary collection bag",
        "Function": "Collection, separation (via centrifugation and extraction), preservation, and transfer of whole human blood and its components (red cells, plasma, platelets depending on configuration)",
        "Source": "Demophorius Healthcare official product listings via MedicalExpo (medicalexpo.com/prod/demophorius-healthcare/product-68185-845550.html and related Demotek bag listings)",
    },
    132: {  # Demotek Quadruple Blood Bag (BBQ)
        "Configuration": "Quadruple bag system -- separates whole blood into up to four components (e.g. red cells, plasma, platelet concentrate, and a satellite/additive bag)",
        "Anticoagulant": "CPDA-1 anticoagulant in the primary collection bag",
        "Application": "Full-service blood banks performing component separation (red cells, plasma, platelets) from a single donation",
        "Source": "Demophorius Healthcare official Demotek product listings (medicalexpo.com/prod/demophorius-healthcare/)",
    },
    133: {  # Demotek Triple Blood Bag (BBT/BBTTB)
        "Configuration": "Triple bag system -- separates whole blood into three components (typically red cells, plasma, and platelet concentrate)",
        "Anticoagulant": "CPDA-1 anticoagulant in the primary collection bag",
        "Application": "Blood banks needing red cell, plasma, and platelet component separation from a single donation",
        "Source": "Demophorius Healthcare official Demotek product listings (medicalexpo.com/prod/demophorius-healthcare/)",
    },
    134: {  # Demotek Single/Double Blood Bag (BBS/BBD)
        "Configuration": "Single bag (BBS, whole blood collection/storage only) or double bag (BBD, separates into red cells and plasma via centrifugation)",
        "Anticoagulant": "CPDA-1 anticoagulant in the primary collection bag",
        "Application": "Smaller-scale blood collection or facilities needing only red cell/plasma separation rather than full component processing",
        "Source": "Demophorius Healthcare official Demotek Double Blood Bag listing (medicalexpo.com/prod/demophorius-healthcare/product-68185-845550.html)",
    },
    165: {  # LIAISON QuantiFERON-TB Gold Plus
        "Function": "Interferon-Gamma Release Assay (IGRA) for detection of Mycobacterium tuberculosis infection (latent or active), run on the DiaSorin LIAISON XL or LIAISON XS Analyzer",
        "Methodology": "Chemiluminescence immunoassay (CLIA) measuring interferon-gamma (IFN-gamma) released by sensitized T cells in heparinized whole blood after stimulation with a QIAGEN QFT-Plus peptide cocktail simulating ESAT-6 and CFP-10 M. tuberculosis antigens",
        "Collection tubes": "4-tube collection: Nil (gray, background control), TB1 (green, CD4+ T cell antigens), TB2 (yellow, CD4+ and CD8+ T cell antigens), and Mitogen (purple, positive assay control); 1 mL blood per tube",
        "Sample handling": "Tubes must be at room temperature (17-25 degC) at collection and shaken 10 times immediately after filling; specimens must reach the laboratory/incubation within 16 hours (some protocols cite up to 53 hours total stability) of collection",
        "Kit configuration": "200 tests/50 patient results per kit (magnetic particles, diluent, assay buffer, calibrators A/B, buffer R, ready-to-use conjugate); separate control kit (2 levels x 2 vials, up to 40 runs)",
        "Clinical note": "Published comparative studies note that automated CLIA (LIAISON) can read borderline IFN-gamma results higher than manual ELISA, and recommend confirmatory ELISA retesting for borderline-positive results (TB1-Nil/TB2-Nil between 0.35-1.0 IU/mL) to reduce false positives",
        "Source": "QIAGEN official LIAISON QuantiFERON-TB Gold Plus product page (qiagen.com/us/products/diagnostics-and-clinical-research/tb-management/liaison-quantiferon-tb-gold-plus-us); QFT-Plus Blood Collection Tubes Package Insert (12/2024); PMC comparative study on LIAISON CLIA accuracy (ncbi.nlm.nih.gov/pmc/articles/PMC11898571/)",
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
