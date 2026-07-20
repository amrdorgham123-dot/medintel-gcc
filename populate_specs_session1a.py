"""
Continuation batch (Session 1, part A) toward filling specs_json for all
244 products. Covers verified refrigeration/freezer units and lab
equipment: Biobase freezer, Haier Biomedical freezer, Zhongke Meiling
pharmacy refrigerator and ULT freezer, Esco biosafety cabinets, and
Mettler Toledo XPR analytical balance.

Run once: python3 populate_specs_session1a.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    221: {  # Biobase BDF-25V100
        "Temperature range": "-25°C (vertical freezer)",
        "Capacity": "100 L",
        "External dimensions (W x D x H)": "540 x 540 x 880 mm",
        "Internal dimensions (W x D x H)": "410 x 410 x 670 mm",
        "Configuration": "Vertical, laboratory/blood plasma freezer",
        "Source": "MedicalExpo/manufacturer listing for Biobase BDF-25V100 (medicalexpo.com/prod/biobase/product-84845-651802.html)",
    },
    215: {  # Haier Biomedical DW-30L818BP
        "Temperature range": "-10°C to -30°C",
        "Capacity": "818 L (28.8 cu ft)",
        "Interior dimensions (W x D x H)": "29.5\" x 29.7\" x 57.5\" (approx. 750 x 755 x 1460 mm)",
        "Exterior dimensions (W x D x H)": "38.9\" x 37.4\" x 77.9\" (approx. 988 x 950 x 1979 mm)",
        "Cooling technology": "Evaporator-shelf design with variable-speed inverter compressor; temperature uniformity ±3°C at set point",
        "Refrigerant": "Environmentally-friendly hydrocarbon (HC) refrigerant, RoHS-compliant",
        "Shelves": "6 adjustable shelves",
        "Source": "Haier Biomedical official listing via Geneva Scientific (geneva-scientific.com/products/cold-storage/freezers/30-large-capacity-biomedical-freezer-model-dw-30l818bp/)",
    },
    243: {  # Zhongke Meiling YC-130L
        "Temperature range": "2°C to 8°C",
        "Capacity": "130 L",
        "External dimensions (W x D x H)": "650 x 625 x 810 mm",
        "Internal dimensions (W x D x H)": "554 x 510 x 588 mm",
        "Net weight": "51 kg",
        "Shelves": "2+1",
        "Noise level": "41.8 dB(A)",
        "Features": "True air cooling technology, UL/CE certified, built-in USB datalogger, 2-year temperature data recording, automatic door heating",
        "Source": "Meling Biomedical official product catalog (manuals.plus/m/90e10fb4b74dfe53a794b6b5432890c9d13b870e5fc5a36b326b47394e6db057)",
    },
    244: {  # Zhongke Meiling DW-FL90
        "Temperature range": "-20°C to -40°C",
        "Configuration": "Undercounter ultra-low temperature freezer, small footprint",
        "Application": "Storage of plasma, vaccines, biological products, and special materials",
        "Refrigeration system": "High-efficiency, environmentally-friendly (Freon-free) enclosed compressor for energy savings and low noise",
        "Source": "Zhongke Meiling Cryogenics official product listing (medicalexpo.com/prod/zhongke-meiling-cryogenics-co-ltd/product-127493-1023471.html)",
    },
    206: {  # Esco Labculture G4 Class II Type A2 BSC
        "Class": "Class II, Type A2 biosafety cabinet",
        "Certification": "NSF-certified",
        "Sash opening options": "8\", 10\", or 12\" openings, with standby-height mode",
        "Controller": "Centurion touchscreen controller",
        "Filtration": "ULPA/HEPA-filtered downflow (ISO Class 3 work zone) and exhaust",
        "Lighting": "Dimmable LED work-zone lighting",
        "Ergonomics": "Raised stainless-steel armrest, large recessed spill-containing work tray, Isocide antimicrobial powder coat",
        "Connectivity": "USB port for relaying operational parameters to a Building Management System (BMS)",
        "Source": "Esco Lifesciences official product page (escolifesciences.com/products/class-ii-biological-safety-cabinet/labculture-g4-class-ii-type-a2-biological-safety-cabinet)",
    },
    207: {  # Esco Streamline Class II BSC
        "Class": "Class II biosafety cabinet (S-series)",
        "Certification": "EN 12469-certified",
        "Controller": "Centurion touchscreen controller",
        "Design": "Compact size, advanced features aimed at space-constrained laboratories",
        "Lighting": "Dimmable LED work-zone lighting",
        "Ergonomics": "Raised stainless-steel armrest",
        "Source": "Esco Lifesciences official product page (escolifesciences.com/products/class-ii-biological-safety-cabinet/streamline-s-series-g4-class-ii-biological-safety-cabinet)",
    },
    208: {  # Esco CO2 Incubators
        "Product line": "CelCulture CO2 Incubator series",
        "Capacity options": "50 L and 170 L chamber sizes (CCL-050B-9, CCL-170B-9, and other capacities in the line)",
        "CO2 control": "Infrared (IR) CO2 sensor for accurate, drift-resistant control",
        "Decontamination": "90°C moist heat decontamination cycle",
        "Filtration": "ULPA-filtered air circulation to minimize contamination risk",
        "Source": "Esco Lifesciences CelCulture CO2 incubator listings (glesales.com/collections/esco)",
    },
    203: {  # Mettler Toledo XPR Analytical Balance (Excellence Level)
        "Product line": "XPR Analytical Balances (Excellence level)",
        "Readability": "Down to 2-5 µg depending on model/capacity (e.g., XPR206DR: 0.005/0.01 mg readability)",
        "Capacity range": "Varies by model, e.g., 81 g/220 g dual-range on XPR206DR",
        "Draft protection": "Motorized side and top doors with touchless SmartSens optical sensors",
        "Quality assurance": "StaticDetect for electrostatic charge detection, integrated methods, results notepad for automatic result/parameter logging",
        "Connectivity": "Optional Bluetooth USB adapter for wireless connection",
        "Source": "Mettler Toledo official product pages (mt.com/us/en/home/products/Laboratory_Weighing_Solutions/analytical-balances/xpr-essential-analytical-balances.html; mt.com XPR206DR/XPR56DR product pages)",
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
