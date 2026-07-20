"""
Session 7 batch continuing specs_json population. Covers Siemens
Healthineers Atellica Solution and ADVIA 2120i, Hologic Panther molecular
system, and bioMerieux VITEK 2 Compact.

Run once: python3 populate_specs_session7.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    18: {  # Siemens Atellica (general Analyzer record)
        "Platform": "Atellica Solution -- integrated immunoassay (IM) and clinical chemistry (CH) analyzer family, over 300 customizable configurations",
        "Throughput (immunoassay)": "Up to 440 tests/hour",
        "Assay menu": "170+ assays (Atellica IM), with several key cardiac, reproductive, and thyroid assays delivering results in about 10 minutes",
        "Sample transport": "Atellica Magline Transport -- patented bi-directional magnetic sample transport, reported up to 10x faster than conventional conveyors; aspiration occurs within 60 seconds of barcode reading",
        "Automation": "Individual sample routing/sorting, automatic QC and calibration, multi-camera vision system, AI-powered workflow intelligence",
        "Connectivity": "Can operate stand-alone or connect to Aptio Automation for a multidisciplinary lab solution (chemistry, immunoassay, hemostasis, hematology, plasma protein)",
        "Source": "Siemens Healthineers official Atellica Solution product page (siemens-healthineers.com/en-us/laboratory-diagnostics/clinical-chemistry-and-immunoassay-systems/atellica-solution-analyzers); BioSpace launch press release",
    },
    109: {  # Atellica Solution (IM + CH) -- same platform, chemistry+immunoassay combined record
        "Platform": "Atellica Solution -- integrated immunoassay (IM) and clinical chemistry (CH) modules on a shared automation track",
        "Throughput (immunoassay)": "Up to 440 tests/hour",
        "Assay menu": "170+ assays across IM and CH, with 50+ additional assays historically noted as in development",
        "Water/waste management": "Onboard water and waste management system designed to reduce environmental footprint",
        "Electrolyte testing": "Integrated Multi Sensor Technology (IMT) for maintenance-free electrolyte testing with automated calibration",
        "Source": "Siemens Healthineers official Atellica Solution product page (siemens-healthineers.com/en-us/laboratory-diagnostics/clinical-chemistry-and-immunoassay-systems/atellica-solution-analyzers)",
    },
    110: {  # Atellica IM 1300 (specific immunoassay module)
        "Module type": "Single immunoassay (IM) analyzer module within the Atellica Solution family",
        "Sample transport": "Atellica Magline Transport, shared with the broader Atellica Solution platform",
        "Assay menu": "Part of the 170+ assay Atellica IM menu, including fast (~10 minute) turnaround for select cardiac, reproductive, and thyroid tests",
        "Scalability": "Can be configured as a stand-alone module or combined with additional IM/CH modules for higher-throughput configurations",
        "Source": "Siemens Healthineers official Atellica Solution product page (siemens-healthineers.com/en-us/laboratory-diagnostics/clinical-chemistry-and-immunoassay-systems/atellica-solution-analyzers)",
    },
    19: {  # ADVIA 2120i / ADVIA 560
        "Throughput": "Up to 120 samples/hour",
        "Detection technology": "Laser light scatter combined with cytochemical (peroxidase) staining -- the gold-standard methodology for WBC differentials",
        "Test menu": "CBC with differential, reticulocyte analysis, 2-dimensional platelet analysis, and CSF analysis with reduced manual intervention",
        "Slide automation (optional)": "ADVIA Autoslide Slide Maker Stainer -- up to 120 high-quality slides/hour",
        "Sampling modes": "Autosampler, open mode, and closed-tube (manual) sampling",
        "Fluidics": "Unifluidics Technology -- reduced fluidics, no pinch valves, automated daily cleaning and completely automated start-up",
        "Connectivity": "ADVIA CentraLink Networking Solution for centralized data management and QC across client workstations",
        "Source": "Siemens Healthineers official ADVIA 2120i product page (siemens-healthineers.com/en-iq/hematology/systems/advia-2120-hematology-system-with-autoslide); MedWrench technical listing",
    },
    47: {  # Hologic Panther
        "Platform": "Fully automated molecular diagnostics system with true sample-to-result automation",
        "Throughput (TMA assays)": "Up to 275 samples in 8 hours",
        "Throughput (real-time TMA assays)": "Up to 320 samples in 8 hours, or up to 750 samples in 15.2 hours",
        "Workflow": "Random access (load samples in any order without batch constraints); processes multiple assays from one patient sample in a single run",
        "Assay menu": "Aptima assay menu covering STIs, women's health, and virology on a single integrated instrument",
        "Automation": "Programmable/automated maintenance scheduling for off-hours operation; STAT sample prioritization",
        "Scalability": "Panther Scalable Solutions allows expansion of testing menu, capacity, and walkaway time; Panther Fusion adds an open-access PCR module",
        "Source": "Hologic official Panther System product page (hologic.com/hologic-products/diagnostic-solutions/panther-system); SelectScience verified throughput listing",
    },
    151: {  # bioMerieux VITEK 2 Compact
        "Function": "Automated bacterial/yeast identification (ID) and antimicrobial susceptibility testing (AST) system, available in multiple sizes for labs of different volumes",
        "Technology": "Advanced Colorimetry for identification; ADVANCED EXPERT SYSTEM (AES) -- a second-generation expert system analyzing MIC patterns and detecting resistance phenotypes",
        "Cards": "Uses the same sealed, compact ID/AST cards as the larger VITEK 2 instrument, minimizing waste and biohazard risk",
        "Software": "Windows-based PC software with icon-driven workflow; OBSERVA information management module for epidemiology/statistical reporting and data export",
        "Ergonomics": "Reduced set-up time and manual steps versus manual ID/AST methods; ergonomic workflow to reduce repetitive-motion injury risk",
        "Source": "bioMerieux official VITEK 2 product page (biomerieux.com/us/en/our-offer/clinical-products/vitek-2.html)",
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
