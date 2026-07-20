"""
Populate specs_json for flagship analyzers/platforms across Attieh Medico's
core portfolio brands (Roche, Mindray, Snibe, Diagnostica Stago, Cepheid,
BioFire/bioMerieux, DiaSorin, Beckman Coulter, Grifols). This is the first
batch toward filling specs_json for the remaining products (3 -> 12 of 244
now have specs_json). Each entry follows the same flat key/value schema as
the existing 3 populated products, with a "Source" key citing the official
manufacturer page used.

Run once: python3 populate_specs_batch1.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    26: {  # Cobas 6800 / Cobas 5800 (Roche)
        "Platform family": "cobas 5800 / 6800 / 8800 -- shared reagent concept, assay menu, and user interface",
        "Time to first result (cobas 5800)": "2 hours 45 minutes (up to 24 tests)",
        "Throughput (cobas 5800, 8h / 24h)": "Up to 144 / 528 tests",
        "Throughput (cobas 6800, single analytic unit)": "Up to 1,056 tests/day",
        "Throughput (cobas 6800, dual analytic unit)": "Up to 2,112 tests/day",
        "Assays per run": "Up to 6 unique assays (software v2.0)",
        "Walkaway time": "Up to 8 hours",
        "Workflow": "Fully automated -- primary tube handling, nucleic acid extraction, real-time PCR amplification and detection",
        "Open channel support": "cobas omni Utility Channel for lab-developed tests (LDTs), up to 24 targets per plate",
        "Source": "Roche Diagnostics official product pages (diagnostics.roche.com/us/en/products/instruments/cobas-6800-v2-ins-7235.html; diagnostics.roche.com/global/en/products/instruments/cobas-5800-ins-6638.html)",
    },
    115: {  # BC-6800Plus (Mindray)
        "Throughput (CBC+DIFF)": "Up to 200 samples/hour",
        "Throughput (CBC+DIFF+RET)": "Up to 120 samples/hour",
        "Throughput (Body fluid mode)": "Up to 40 samples/hour",
        "Loading capacity": "Up to 100 sample tubes, autoloader",
        "Sample volume": "80 uL (autoloader, whole blood)",
        "WBC differential": "5-part (+ NRBC, basophils, WBC-N in WNB scattergram)",
        "Reportable parameters": "37 reportable + 42 research parameters (whole blood)",
        "Detection principle": "SF Cube (Scatter + Fluorescence + 3D Cube analysis) for WBC/DIFF/NRBC/RET/PLT-O; Focusing Flow-DC for RBC/PLT; cyanide-free HGB reagent",
        "Data storage": "Up to 100,000 results (numeric + graphical)",
        "Source": "Mindray official product page (mindray.com/en/products/laboratory-diagnostics/hematology/5-part-differential-analyzers/bc-6800-plus)",
    },
    23: {  # STA R Max (Diagnostica Stago)
        "Throughput": "Up to 250 tests/hour",
        "Sample capacity": "Up to 215 sample positions (STA R Max3)",
        "Reagent positions": "Up to 70 cooled reagent positions",
        "Detection method": "Viscosity-Based (Mechanical) Detection System (VBDS) -- not affected by optical interference (hemolysis, icterus, lipemia)",
        "Sample integrity check": "Integrated EPC module checks fill volume and detects hemolyzed/icteric/lipemic samples without extra plasma volume",
        "STAT handling": "True STAT priority -- emergency samples processed without interrupting running tests",
        "Software": "STA Coag Expert with auto-verification, 5-year onboard patient archive",
        "Connectivity": "Industry-leading total laboratory automation (TLA) connectivity",
        "Source": "Stago official product pages (stago-us.com/products-services/hemostasis-systems/sta-r-max-3/)",
    },
    150: {  # GeneXpert Platform (Cepheid)
        "Module configurations": "1, 2, 4, 16, 48, or 80 modules (GeneXpert Infinity line for higher throughput)",
        "Result time": "Most assays deliver results in about an hour, including automated sample preparation",
        "Workflow": "Fully integrated -- sample prep, nucleic acid purification, real-time PCR amplification and detection in a single-use disposable cartridge",
        "Targets per cartridge": "Up to 6 genes per cartridge via multiple calibrated fluorophore dyes",
        "Portable option": "GeneXpert Omni -- 1.0 kg handheld, single cartridge module, battery-powered (up to 4h + 12h supplemental), cloud connectivity",
        "Cross-contamination control": "Self-contained single-use cartridges minimize cross-contamination between samples",
        "Source": "Cepheid official test menu page (cepheid.com/en-US/tests.html); ClinicalTrials.gov protocol documentation citing GeneXpert Omni specifications",
    },
    149: {  # FilmArray Multiplex PCR Panels (BioFire)
        "Hands-on time": "About 2 minutes per test",
        "Total run time": "45 minutes to about 1 hour (assay-dependent)",
        "Workflow": "Automated sample preparation, nested multiplexed nucleic acid amplification, DNA melting analysis, and results generation in a single closed disposable reagent pouch",
        "Respiratory panel (RP2.1)": "Tests for viral and bacterial respiratory pathogens; ~45 minute run time",
        "Blood Culture ID panel (BCID2)": "Identifies bacteria, fungi, and antimicrobial resistance markers directly from positive blood culture bottles",
        "Gastrointestinal panel": "22 pathogens (viruses, bacteria, parasites) from a single stool specimen; reduces turnaround time to under 2 hours vs. ~53 hours for routine PCR in published comparisons",
        "System options": "BioFire FilmArray 2.0, FilmArray Torch (higher-throughput multi-module), and CLIA-waived FilmArray 2.0 EZ Configuration",
        "Source": "bioMerieux/BioFire official panels page (biofiredx.com/products/the-filmarray-panels/); FIND landscape report on molecular platforms for near-patient testing",
    },
    164: {  # LIAISON XL (DiaSorin)
        "Throughput": "Up to 180 tests/hour",
        "Assay menu": "60+ assays available (infectious disease, metabolic bone disease/vitamin D, autoimmunity, and more)",
        "Detection technology": "Chemiluminescence immunoassay (CLIA) using magnetic microparticles",
        "Loading": "Continuous loading, walk-away operation",
        "Sample types": "Serum, plasma; assay-dependent",
        "Source": "DiaSorin official product page (int.diasorin.com/en/immunodiagnostics/tools/liaison-xl); refurbisher technical listing (diamonddiagnostics.com) confirming throughput/menu size",
    },
    106: {  # DxH 900 / DxH 690T (Beckman Coulter)
        "Throughput": "Up to 100 tests/hour (closed-tube whole blood)",
        "First-pass yield": "93% (reduces slide reviews and manual intervention)",
        "Detection technology": "VCS technology (Volume, Conductivity, light Scatter) + DataFusion, near native-state cellular characterization",
        "Unique biomarker": "Monocyte Distribution Width (MDW) -- aids early identification of infection severity/sepsis risk in adult ED patients, part of routine CBC-Diff",
        "Workflow automation": "Up to 1,800 samples between reagent changes without interruption (DxH 900-3S configuration)",
        "Slide-making (with SMS II)": "Up to 4 slides per 90 uL sample aspiration, up to 140 slides/hour",
        "Connectivity": "Compatible with DxA 5000 / DxA Fit 5000 lab automation and REMISOL Advance middleware; up to 3 analyzers connected per workcell",
        "Source": "Beckman Coulter official product pages (beckmancoulter.com/products/hematology/dxh-900; m.beckmancoulter.com/dxh-900-series-high-volume-hematology-solutions.html)",
    },
    38: {  # Erytra (Grifols)
        "Throughput (Type & Screen)": "Up to 48 assays/hour",
        "Throughput (complete ABO/Rh)": "Up to 60 tests/hour",
        "Walkaway autonomy": "Up to 4 hours nonstop",
        "STAT handling": "Dedicated STAT access button for immediate loading and prioritization",
        "Design": "Upright, compact footprint with self-organizing sample/card/reagent workflow",
        "Capacity": "Handles workloads from 1 to 96 samples with consistent turnaround management",
        "Source": "Grifols official product page (diagnostic.grifols.com/en/blood-typing/automated-and-manual-testing/fully-automated-systems-erytra)",
    },
    68: {  # Biossays 240 Plus / C8 / C10 (Snibe)
        "Throughput": "Constant 240 tests/hour (240 Plus); ISE option adds 200 tests/hour",
        "Test menu": "Up to 236 parameters (routine biochemistry, liver/kidney function, lipids, cardiac markers, electrolytes)",
        "Sample/reagent positions": "Up to 90 continuous-loading sample positions, up to 90 reagent positions",
        "Reaction cuvettes": "80 reusable reaction cuvettes",
        "Sample volume": "2.0-35.0 uL (biochemistry); 90.0 uL (ISE)",
        "Sample types": "Serum, plasma, urine, CSF",
        "Storage": "24-hour independent refrigeration for samples and reagents",
        "STAT handling": "Unlimited STAT priority, random access, continuous loading",
        "Source": "Snibe official product page (snibe.com/en/product/biochemistry_analyzer/433.html)",
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
