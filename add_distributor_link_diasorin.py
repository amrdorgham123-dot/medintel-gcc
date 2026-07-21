"""
Confirms and records the DiaSorin -> Abdulla Fouad (Saudi Arabia)
distributor relationship for Immunodiagnostics.

DiaSorin was researched as a candidate for the "opportunities" table
(open KSA market gap), but its own official "Diasorin Worldwide" contacts
page lists a named Saudi Arabia contact under Immunodiagnostics:
Abdulla Fouad for Medical Supplies, P.O. Box 257, Dammam 31411, contact
person Hussein Fares (hussein.fares@abdulla-fouad.com). Abdulla Fouad
already existed in the distributors table (id 11, previously linked to
77Elektronika and QIAGEN via a NUPCO tender record) -- this adds DiaSorin
as a third confirmed principal for that distributor, rather than creating
a false "no distributor" opportunity entry.

Run once: python3 add_distributor_link_diasorin.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    mfr = conn.execute("SELECT id FROM manufacturers WHERE name = 'DiaSorin'").fetchone()
    dist = conn.execute("SELECT id, represents FROM distributors WHERE name = 'Abdulla Fouad for medical supplies'").fetchone()
    if not mfr or not dist:
        print("Manufacturer or distributor not found -- skipping.")
        return
    existing = conn.execute(
        "SELECT id FROM company_distributors WHERE manufacturer_id = ? AND distributor_id = ?",
        (mfr[0], dist[0])
    ).fetchone()
    if existing:
        print("Link already exists -- skipping.")
        return
    conn.execute(
        "INSERT INTO company_distributors (manufacturer_id, distributor_id) VALUES (?, ?)",
        (mfr[0], dist[0])
    )
    if "DiaSorin" not in (dist[1] or ""):
        new_represents = (dist[1] or "") + ", DiaSorin (Immunodiagnostics)"
        conn.execute("UPDATE distributors SET represents = ? WHERE id = ?", (new_represents, dist[0]))
    conn.commit()
    print("Linked DiaSorin -> Abdulla Fouad. company_distributors total:",
          conn.execute("SELECT COUNT(*) FROM company_distributors").fetchone()[0])
    conn.close()

if __name__ == "__main__":
    main()
