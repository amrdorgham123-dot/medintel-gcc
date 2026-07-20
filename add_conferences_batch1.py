"""
Adds real, verified conference entries relevant to Attieh Medico's KSA/GCC
IVD business development -- part of populating the previously near-empty
opportunities/conferences/regulatory_status tables with genuine data
rather than placeholder content.

1. Global Health Exhibition 2026, Riyadh -- the single highest-priority
   entry missing from the table: it's the flagship healthcare/lab
   exhibition held IN Saudi Arabia itself (Riyadh), 26-29 October 2026.
2. World Health Expo Dubai 2027 (formerly Arab Health) -- 25-28 January
   2027, the major GCC-adjacent healthcare exhibition with a strong
   IVD/diagnostics presence, distinct from WHX Labs Dubai (formerly
   MEDLAB Middle East, already in the table for 26-29 Jan 2027).

Run once: python3 add_conferences_batch1.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

CONFERENCES = [
    {
        "name": "Global Health Exhibition 2026",
        "event_date": "2026-10-26",
        "place": "Riyadh Exhibition and Convention Center (Malham), Riyadh, Saudi Arabia",
        "tag": "Healthcare / Lab Equipment / IVD",
        "source": "globalhealthsaudi.com official show information page (26-29 October 2026, confirmed across Kallman Worldwide and ABHI UK Pavilion listings)",
    },
    {
        "name": "World Health Expo Dubai 2027 (formerly Arab Health)",
        "event_date": "2027-01-25",
        "place": "Dubai Exhibition Centre + Dubai World Trade Centre, Dubai, UAE",
        "tag": "Healthcare / IVD / Lab Equipment",
        "source": "worldhealthexpo.com official 'Arab Health is now WHX Dubai' page (25-28 January 2027, confirmed via 10times.com and Informa Markets listing)",
    },
]

def main():
    conn = sqlite3.connect(DB_PATH)
    inserted, skipped = 0, 0
    for c in CONFERENCES:
        existing = conn.execute("SELECT id FROM conferences WHERE name = ?", (c["name"],)).fetchone()
        if existing:
            print(f"SKIP (already exists): {c['name']}")
            skipped += 1
            continue
        conn.execute(
            "INSERT INTO conferences (name, event_date, place, tag, source) VALUES (?,?,?,?,?)",
            (c["name"], c["event_date"], c["place"], c["tag"], c["source"])
        )
        print(f"INSERTED: {c['name']} ({c['event_date']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped: {skipped}")

if __name__ == "__main__":
    main()
