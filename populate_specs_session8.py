"""
Session 8 batch continuing specs_json population. Covers Leica Biosystems
histology and digital pathology instruments: HistoCore PELORIS 3 tissue
processor, HistoCore PEGASUS Plus tissue processor, and Aperio GT 450 /
GT 450 DX digital pathology slide scanner.

Run once: python3 populate_specs_session8.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    160: {  # HistoCore PELORIS 3
        "Design": "Dual-retort ActivFlo technology for rapid, even reagent heating and active reagent movement, improving tissue infiltration uniformity",
        "Capacity": "High-capacity tissue processor designed to deliver consistent results from slide 1 through 1,600",
        "Protocols": "Flexible validated protocols, including a validated 1-hour rapid protocol for urgent biopsies and a 5-hour protocol optimized for fatty tissue",
        "Traceability": "HistoCore I-Scan integrated barcode scanner captures cassette ID, quantity, and color, plus basket ID, user ID, and reagent information for full track-and-trace records",
        "Cassette performance": "Validated ActivFlo cassettes improve drainage efficiency by up to 23% versus standard cassettes",
        "Power/environment": "1,450 W (100-120V) / 2,150 W (220-240V); operating range 5-35°C, 10-80% RH (non-condensing), altitude 0-2,000 m",
        "Source": "Leica Biosystems official product page (leicabiosystems.com/histology-equipment/tissue-processors/histocore-peloris-3/); MedicalExpo technical listing",
    },
    161: {  # HistoCore PEGASUS Plus
        "Function": "Automated tissue processor enabling multiple processing protocols to run in parallel on a single instrument",
        "Value proposition": "Ensures optimal processing conditions for all tissue types without slowing down laboratory throughput, part of Leica Biosystems' end-to-end histology workflow (biopsy to diagnosis)",
        "Source": "Leica Biosystems official innovations/product overview page (leicabiosystems.com/about/Innovations/)",
    },
    162: {  # Aperio GT 450 / GT 180 DX
        "Scan speed": "Approximately 32 seconds per slide at 40x, for an output of 81 slides/hour at 40x (15mm x 15mm scan area)",
        "Capacity": "450-slide capacity via 15 racks (30 slides/rack), continuous rack loading without interrupting active scanning",
        "Resolution": "0.26 um/pixel at 40x magnification, with extra-wide flat-field-corrected objectives (1mm field of view) from Leica Microsystems optics",
        "Image quality features": "Automatic per-slide calibration, automated image quality check during scanning, Extended Focus (multi-layer image combination), Z-Stacking for varied-height sample review",
        "File formats": ".svs and DICOM support for interoperability and streamlined workflow",
        "Regulatory status (DX model)": "FDA 510(k)-cleared and CE-marked under IVDR for in vitro diagnostic use (GT 450 DX); base GT 450 is Research Use Only",
        "Integration": "Compatible with HistoCore SPECTRA Workstation (Stainer and Coverslipper) for direct rack loading into the scanner",
        "Source": "Leica Biosystems official Aperio GT 450 product pages (leicabiosystems.com/us/digital-pathology/scan/aperio-gt-450/; leicabiosystems.com/us/digital-pathology/scan/aperio-gt-450-dx-scanner/); official specifications PDF (leicabiosystems.com/sites/default/files/media_product-download/2025-01/Aperio_GT_450_Specifications_-_English_-_MAN-0393-Rev-L.pdf)",
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
