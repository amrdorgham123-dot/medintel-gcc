"""
Specs batch continuing product specs_json population. Covers BD
SurePath Liquid-Based Pap Test and BD FocalPoint (GS Imaging System)
Slide Profiler.

Run once: python3 populate_specs_batch_2025j.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    194: {  # BD SurePath Liquid-Based Pap Test
        "Collection method": "Two-in-one brush with a detachable head deposited directly into the ethanol-based SurePath collection vial -- sends 100% of the collected cells to the lab, unlike the rinse-and-swirl technique (which can discard an average of 37% of cells)",
        "Sample processing": "Proprietary cell enrichment process separates and removes blood, mucus, and interfering debris so only the most diagnostically relevant material reaches the slide",
        "Slide characteristics": "13 mm deposition area with uniform, thin-layer cell distribution",
        "Automation compatibility": "Scalable from manual processing up to full automation: BD PrepMate or BD Totalys MultiProcessor (sample prep/cell enrichment, up to 12 samples per cycle in under 5 minutes), BD Totalys SlidePrep (slide prep/staining), and BD FocalPoint GS Imaging System (slide analysis)",
        "Clinical performance (vs. conventional cytology)": "Independent studies cite -58% unsatisfactory reports, -29% ASC-US/LSIL ratio, +64% HSIL+ detection, and +107% LSIL+ detection",
        "Ancillary testing": "Supports optional customizable aliquots for ancillary molecular testing, including the BD Onclarity HPV Assay, from the same collection vial",
        "Source": "BD official BD SurePath product pages (bd.com/en-us/products-and-solutions/products/product-families/bd-surepath-liquid-based-pap-test; eu.bd.com/cervical-screening-solutions cervical cytology automation and clinical performance pages)",
    },
    195: {  # BD FocalPoint Slide Profiler / GS Imaging System
        "Function": "Automated imaging system that ranks and prioritizes cervical cytology slides for screener review, on both BD SurePath Liquid-Based Pap Test and conventional Pap preparations",
        "Throughput": "Continuous throughput with a maximum onboard capacity of 288 slides at any one time",
        "Review guidance": "Directs the screener to specific fields of interest most likely to contain abnormal cells -- up to 10 fields for SurePath slides and up to 15 fields for conventional Pap slides -- focusing reviewer attention rather than requiring full manual slide review",
        "Stain compatibility": "Accepts a wide variety of laboratory-preferred stains, with no requirement to purchase or train on imager-specific proprietary stains",
        "Clinical value": "Reported to improve cervical cancer detection and screening efficiency versus manual screening alone",
        "Source": "BD official cytology testing instruments page (emea.bd.com/advancing-diagnostics/products/cervical-cancer/bd-cervical/) and BD FocalPoint Slide Profiler Product Insert (7790419402)",
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
