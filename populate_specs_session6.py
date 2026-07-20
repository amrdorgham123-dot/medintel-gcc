"""
Session 6 batch continuing specs_json population. Covers Carl Zeiss
Primovert/Axiovert microscopes and Alcor Scientific iSED-family automated
ESR analyzers (iSED/iSED PRO/iSED Elite and miniiSED).

Run once: python3 populate_specs_session6.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    209: {  # Axiovert 5 / Primovert
        "Product line": "ZEISS Axiovert 5 (digital, AI-enabled) and Primovert -- compact inverted microscopes for cell culture observation",
        "Contrast methods": "Brightfield, phase contrast, and optional fluorescence (GFP-labeled cells)",
        "Illumination": "LED illumination -- long lifespan, low power consumption, low heat generation",
        "Objectives (Primovert)": "Plan-Achromat / LD Plan-Achromat objectives, typically 4x-40x magnification",
        "Automation (Axiovert 5 digital)": "AI-based cell analysis via ZEISS Labscope for one-click cell counting and confluency measurement",
        "Form factor": "Compact design, compatible with placement inside a laminar flow cabinet for sterile-environment work",
        "Source": "ZEISS official product pages (zeiss.com/microscopy/us/products/light-microscopes/widefield-microscopes/primovert.html; zeiss.com/microscopy/us/products/light-microscopes/widefield-microscopes/axiovert-5-digital.html)",
    },
    210: {  # Axio Imager
        "Product line": "ZEISS Axio Imager -- upright research microscope platform (materials and life science configurations)",
        "Application": "High-resolution imaging for research and quality/materials analysis, with automated deformation-axis detection and inclusion analysis in materials configurations",
        "Software": "ZEN core software suite for imaging, analysis, and (in regulated-industry configurations) GxP-compliant traceability and data integrity",
        "Connectivity": "Integrates with other ZEISS imaging solutions via ZEN core for combined workflows across instruments",
        "Source": "ZEISS official product page (zeiss.com/microscopy/en/products/light-microscopes/widefield-microscopes/axiovert-for-materials.html)",
    },
    49: {  # miniiSED i-SED (Analyzer record)
        "Technology": "Photometric rheology / capillary photometry (syllectometry) -- directly measures red cell aggregation (rouleaux formation) rather than the traditional Westergren settling method",
        "Result time": "15-20 seconds per ESR result",
        "Sample requirement": "100 uL, drawn directly from a primary EDTA tube (no disposables or manual sample prep required)",
        "Correlation to reference method": "Highly correlated with the Westergren method; a published verification study found iSED bias of 0.0 (95% CI -1.4 to 1.5) mm/hr vs. Westergren across low/medium/high ESR ranges",
        "Efficiency": ">96% less hands-on time and up to 94% shorter turnaround time compared with the Westergren method",
        "Sample stability": "Up to 28 hours at room temperature (versus the short stability window of Westergren-based testing)",
        "Source": "ALCOR Scientific official iSED product page (alcorscientific.com/clinical-lab/ised/); PMC verification study (ncbi.nlm.nih.gov/pmc/articles/PMC8833250/)",
    },
    113: {  # iSED / iSED PRO / iSED Elite
        "Technology": "Photometric rheology / capillary photometry directly measuring RBC aggregation (rouleaux formation)",
        "Workflow (iSED PRO/Elite)": "Rack-based, fully automated -- capped primary EDTA tubes loaded via racks, with automated determination of which samples need testing, mixing, aspiration, and reading",
        "Result time": "Results in seconds (approximately 15-20 seconds per sample)",
        "Additional features (PRO)": "Automated QC scheduling, onboard consumables storage, automatic self-cleaning, no per-test disposables required, STAT-testing capable",
        "Sample stability": "Up to 28 hours at room temperature",
        "Quality assurance": "SEDiTROL bi-level, human-based whole blood controls (60-day open-vial stability) with free access to ALCOR's iQAP peer-to-peer online QA program",
        "Source": "ALCOR Scientific official iSED PRO / iSED Elite product pages (alcorscientific.com/clinical-lab/ised-pro-esr-analyzer/; alcorscientific.com/clinical-lab/ised-elite-us-esr-analyzer/)",
    },
    114: {  # miniiSED
        "Technology": "Same photometric rheology / capillary photometry principle as the full iSED platform, in a compact instrument footprint",
        "Result time": "Approximately 15-20 seconds per ESR result",
        "Sample requirement": "100 uL, drawn directly from a primary EDTA tube",
        "Target setting": "Smaller-volume or space-constrained laboratories needing walk-away ESR automation without the full iSED PRO/Elite rack-based throughput",
        "Source": "ALCOR Scientific official product listings and Labmedica MEDICA 2023 coverage (labmedica.com/medica-2023/articles/294799302/alcor-scientific-demonstrates-fully-automated-esr-analyzers.html)",
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
