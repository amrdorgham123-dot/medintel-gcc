"""
Specs batch continuing product specs_json population. Covers Alphavita
MDF-U781VHE ultra-low temperature freezer.

Run once: python3 populate_specs_batch_2025f.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    219: {  # Alphavita MDF-U781VHE
        "Temperature range": "-50C to -86C (base MDF-U781 series; VHE variant adds VIP insulation + HC refrigerant + inverter compressor + intelligent touchscreen control)",
        "Capacity": "736 L (base MDF-U781 series)",
        "External dimensions (W x D x H)": "1030 x 875 x 1990 mm",
        "Internal dimensions (W x D x H)": "890 x 600 x 1380 mm",
        "Net weight": "329 kg",
        "Rated input power": "900 W",
        "Insulation": "Vacuum insulation panel (VIP) technology -- thermal conductivity <0.0018 W/m*K, cited as ~13x better insulating performance than traditional PU foam",
        "Refrigerant": "Hydrocarbon (HC) refrigerant with cascade cooling system, reported to improve pull-down time by ~20% over standard designs",
        "Construction": "Electrogalvanized steel exterior with powder coating; standard expansion tank for pressure regulation to maintain compressor performance at elevated ambient temperatures",
        "Source": "Alphavita Bio-Scientific official specifications page (alphavitabiosci.com/ultra-low-freezer/) and MedicalExpo manufacturer listing (medicalexpo.com/prod/alphavita/product-299686-1141153.html)",
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
