"""
Session 3 batch continuing specs_json population. Covers the Cerus
INTERCEPT Blood System pathogen reduction technology across its platelet,
plasma, and cryoprecipitation components, plus the INT100 UVA Illuminator
that powers the treatment process.

Run once: python3 populate_specs_session3.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    46: {  # INTERCEPT (general/platform record)
        "Technology": "Photochemical pathogen reduction using amotosalen (a psoralen compound) plus controlled UVA illumination",
        "Platform": "Disposable processing sets (plastic, PVC tubing) combined with the INTERCEPT Illuminator for UVA light dosing",
        "Components covered": "Platelets, plasma, and cryoprecipitation processing sets, all treated on the same illuminator platform",
        "Pathogen coverage": "Broad-spectrum inactivation of bacteria, viruses, protozoa, and residual leukocytes; certain non-enveloped viruses (e.g., HAV, HEV, B19) and Bacillus cereus spores show demonstrated resistance",
        "Regulatory status": "FDA-approved (PMA) pathogen reduction system for apheresis platelet and plasma components",
        "Source": "Cerus Corporation official INTERCEPT USA resource pages (intercept-usa.com; intercept-usa.com/resources/); FDA approved blood products listing (fda.gov/vaccines-blood-biologics/approved-blood-products/intercept-blood-system-platelets)",
    },
    82: {  # INTERCEPT Blood System for Platelets
        "Indication": "Ex vivo preparation of pathogen-reduced apheresis platelet components to reduce transfusion-transmitted infection (TTI) risk, including sepsis, and as an alternative to gamma irradiation for preventing transfusion-associated graft-versus-host disease (TA-GVHD)",
        "Compatible platelet sources": "Amicus apheresis platelets suspended in 65% PAS-3/35% plasma; Trima apheresis platelets suspended in 100% plasma",
        "Processing window": "Platelets must be treated within 24 hours of collection",
        "Shelf life": "Current maximum expiration dating of 5 days in the U.S. (post-approval studies have evaluated extended storage up to 7 days)",
        "Device classification": "FDA Class III medical device (disposable processing sets + INT100 Illuminator)",
        "Source": "Cerus Corporation / FDA package insert and approved blood products documentation (fda.gov/vaccines-blood-biologics/approved-blood-products/intercept-blood-system-platelets)",
    },
    83: {  # INTERCEPT Blood System for Plasma
        "Indication": "Ex vivo preparation of pathogen-reduced plasma components to reduce transfusion-transmitted infection (TTI) risk",
        "Technology": "Same amotosalen + UVA illumination process as the platelet system, processed on the same INTERCEPT Illuminator platform",
        "Processing requirements": "Specific processing range requirements apply for plasma volume per the manufacturer's spec sheet",
        "Source": "Cerus Corporation official plasma spec sheet (cryopre.cerus.com/wp-content/uploads/sites/8/2024/02/MKT-EN-00732-v1.0-Plasma-Spec-Sheet.pdf)",
    },
    84: {  # INTERCEPT Blood System for Cryoprecipitation
        "Indication": "Pathogen-reduced processing pathway feeding into cryoprecipitate preparation, using the same INTERCEPT amotosalen/UVA platform applied to plasma prior to cryoprecipitation",
        "Technology": "Photochemical pathogen reduction (amotosalen + UVA), consistent with the broader INTERCEPT Blood System platform",
        "Source": "Cerus Corporation official INTERCEPT Blood System resource pages (intercept-usa.com)",
    },
    85: {  # INT100 Illuminator
        "Function": "Delivers a controlled dose of ultraviolet A (UVA) light to amotosalen-treated platelet and plasma components as part of the INTERCEPT pathogen reduction process",
        "Compatibility": "Must be used exclusively with INTERCEPT Processing Sets; no other UVA light source is approved for use in the process",
        "Regulatory note": "A newer INT100G2 Illuminator (with alternate processing set plastics/design) received FDA approval in May 2018",
        "Safety requirement": "Any platelet component not exposed to the complete INT100 illumination process must be discarded",
        "Source": "Cerus Corporation INTERCEPT USA resources and Illuminator Operator's Manual references (intercept-usa.com/resources/)",
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
