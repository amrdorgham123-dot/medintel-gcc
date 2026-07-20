"""
Session 2 batch toward filling specs_json for all 244 products. Covers
verified specs for major-brand analyzers: Sysmex XN series (family),
Radiometer ABL800/ABL90 FLEX blood gas analyzers, Tosoh HLC-723 G8 HbA1c
analyzer, Werfen ACL TOP Family coagulation analyzers, bioMerieux VIDAS
immunoassay analyzer, and Abbott Alinity hq/hs hematology system.

Run once: python3 populate_specs_session2.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    12: {  # Sysmex XN series (family-level record)
        "Platform family": "XN-Series (modular, scalable from single-module XN-550 to multi-module XN-9100 configurations)",
        "Detection principle": "Fluorescent flow cytometry (semiconductor laser, hydrodynamic focusing) + electrical impedance + SLS-Hb (cyanide-free)",
        "Throughput (CBC+DIFF, per module)": "Up to 100 samples/hour",
        "Throughput (Body Fluid mode, per module)": "Up to 40 samples/hour",
        "Key parameters": "WBC, RBC, HGB, HCT, MCV, MCH, MCHC, PLT (PLT-I/PLT-F), 5-part DIFF, IG#/%, NRBC#/%, RET#/%, IRF, RET-He, IPF#/%",
        "Modularity": "Individual modules can be combined into multi-instrument configurations for high-volume laboratories, sharing a common data management unit",
        "Source": "Sysmex America official XN-Series page (sysmex.com/en-us/lab-solutions/hematology/xn-series)",
    },
    168: {  # Radiometer ABL800 FLEX
        "Parameters measured": "Up to 18 STAT parameters per sample: pH, blood gas (pCO2, pO2), electrolytes (K+, Na+, Cl-, Ca++), CO-oximetry (ctHb, sO2, FO2Hb, FCOHb, FMetHb, FHHb, FHbF, ctBil), metabolites (glucose, lactate)",
        "Sample handling": "FLEXQ module automatically scans, mixes, and analyzes up to 3 successive blood gas samples",
        "Minimum sample volume": "Down to 35 uL using FLEXMODE/MICROMODE for capillary/neonatal samples",
        "CO-oximetry": "128-wavelength full CO-oximetry with automatic suppression of interference from fetal hemoglobin, bilirubin, intralipids, and sulfhemoglobin",
        "Workflow": "Drop'n'Go functionality -- syringe placed on FLEXQ module is automatically scanned, mixed, and analyzed",
        "Target setting": "Medium- to high-volume central lab testing sites",
        "Source": "Radiometer official product page (radiometer.com/en/products/blood-gas-testing/abl800-flex-blood-gas-analyzer)",
    },
    167: {  # Radiometer ABL90 FLEX
        "Parameters measured": "Up to 17-19 vital parameters (blood gas, electrolytes, CO-oximetry, metabolites; creatinine/urea/eGFR on PLUS configuration)",
        "Result time": "35 seconds per sample",
        "Sample volume": "Only 65 uL of whole blood",
        "Uptime": "More than 23.5 hours per day, only 60 seconds between successive sample measurements",
        "Quality management": "Automatic Quality Management (AQM) -- calibration, QC, analysis, system, and clot checks performed automatically",
        "Target setting": "Point-of-care / near-patient testing (ED, ICU) requiring fast turnaround from small sample volumes",
        "Source": "Radiometer official product page (radiometer.com/en/products/blood-gas-testing/abl90-flex-blood-gas-analyzer)",
    },
    101: {  # Tosoh HLC-723 G8
        "Methodology": "Ion-exchange HPLC (International Gold Standard for HbA1c analysis)",
        "Result time": "1.0 minutes (standard mode) or 1.6 minutes (variant mode) per HbA1c result; HbF and HbA2 results in 6 minutes",
        "Precision": "Inter- and intra-assay CV <2% (some sources cite <1%)",
        "Sample loader options": "90-sample loader (upgradable) or 290-sample loader / lab automation-compatible models",
        "Hemoglobin variant detection": "Presumptively identifies common Hb variants; simple mode change enables beta-thalassemia screening program",
        "Automation": "Fully automated maintenance, startup, and shutdown; primary tube sampling with cap piercing; integrated barcode reader",
        "Dimensions (90-sample loader model)": "530(W) x 515(D) x 482(H) mm, 34.0 kg",
        "Source": "Tosoh Bioscience official product page (tosohbioscience.com/US-EN-diagnostics/view-all-featured-analyzers/g8)",
    },
    52: {  # Werfen ACL TOP Family (general)
        "Platform family": "ACL TOP Family -- complete line of hemostasis testing systems (50 Series and 70 Series) scaling from routine to specialty coagulation testing",
        "Model range": "Includes 350, 550, and 750 model designations (50 Series) verified as a harmonized single instrument class across routine coagulation assays in multi-site studies",
        "Test menu": "Routine coagulation (PT/INR, aPTT, fibrinogen, D-dimer) through specialty hemostasis assays, using HemosIL reagents",
        "Automation": "Advanced automation and quality management designed to scale from mid-volume to high-volume laboratories",
        "Source": "Werfen North America official product pages (werfen.com/na/en/hemostasis-diagnostics/coagulation-instruments-system-acl-top-family-series); PMC verification study across 60 laboratories (pubmed.ncbi.nlm.nih.gov/33891005/)",
    },
    119: {  # Werfen ACL TOP Family 50/70 Series
        "Platform family": "ACL TOP Family 50 Series (350/550/750 models) and 70 Series -- next-generation hemostasis testing systems",
        "Verified harmonization": "A large multi-site study (60 laboratories, n=75 instruments) verified the 350, 550, and 750 models as a single harmonized instrument class with no to limited bias between models",
        "Reagents": "HemosIL reagent panel, compatible across the ACL TOP Family",
        "Test menu": "PT/INR, aPTT, thrombin time, fibrinogen, D-dimer, and specialty coagulation assays",
        "Source": "Werfen North America official product page (werfen.com/na/en/hemostasis-diagnostics/coagulation-analyzer-acl-top-family-70-series); PMC verification study (pubmed.ncbi.nlm.nih.gov/33891005/)",
    },
    53: {  # bioMerieux VIDAS
        "Technology": "ELFA (Enzyme-Linked Fluorescent Assay) -- single-test concept immunoassay format",
        "Assay menu": "More than 80 available tests spanning infectious disease, cardiovascular/critical care, cancer markers, fertility, pregnancy, and thyroid disease",
        "Throughput (VIDAS 3 model)": "Up to 36 tests/hour, measuring 55 assays",
        "Format": "Benchtop, single-test on-demand testing -- widely installed base of immunoanalyzers globally",
        "Source": "bioMerieux official VIDAS product page (biomerieux.com/corp/en/our-offer/hospital-laboratory/product-range/vidas-immunoassay-diagnostics-equipment-and-biomarkers.html); refurbisher technical listing confirming VIDAS 3 throughput (diamonddiagnostics.com/products/Biomerieux-Vidas-3-Immunology-Analyzer)",
    },
    29: {  # Abbott Alinity HQ
        "System": "Alinity h-series -- Alinity hq (automated hematology analyzer) integrated with Alinity hs (slide maker/stainer)",
        "Throughput": "Up to 119 CBC results per hour",
        "Detection technology": "Fully optical, multi-angle light scattering (MAPSS technology) with machine-learning cell classification (Gaussian Mixture Model, Graph Adaptive Clustering)",
        "CBC report": "6-part differential with reticulocyte analysis including immature reticulocyte fraction",
        "Sample loading": "Front-loading and laboratory automation (track) compatible, with urgent-sample priority",
        "Footprint": "Designed for reduced floor space versus prior-generation systems",
        "Maintenance": "Hands-off automated daily and weekly cleaning schedules",
        "Source": "Abbott official press release (abbott.mediaroom.com/2023-08-07-FDA-Clears-Abbotts-Alinity-h-series-Lab-Instruments); Abbott Core Laboratory official product page (corelaboratory.abbott/int/en/offerings/brands/alinity/Alinity-h-hematology-system.html)",
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
