"""
Bulk-inserts the remaining NUPCO-tender-verified manufacturer-distributor
relationships (beyond the 8 'unclear'-status manufacturers handled in
add_distributors_nupco_batch.py). Source data: /home/claude/truly_new_links.json,
derived from NUPCO Tenders NPT0003/23 and NPT0012/23 (2023 Final Awardation
records, uploaded by the user).

Run once: python3 add_distributors_nupco_batch2.py
"""
import sqlite3
import json
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")
LINKS_PATH = "/home/claude/truly_new_links.json"

def clean_vendor_name(name):
    return re.sub(r'\s*-Orig-\s*$', '', name).strip()

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def get_or_create_distributor(conn, name, country, source, existing_dist_norm):
    name = clean_vendor_name(name)
    n = norm(name)
    if n in existing_dist_norm:
        return existing_dist_norm[n]
    cur = conn.execute(
        "INSERT INTO distributors (name, country, represents, source, market_strength_tier, market_strength_basis) VALUES (?,?,?,?,?,?)",
        (name, country, "", source, "Tender-verified (partial)",
         "Confirmed via NUPCO tender award record; not independently confirmed for overall company size or revenue.")
    )
    new_id = cur.lastrowid
    existing_dist_norm[n] = new_id
    return new_id

def main():
    conn = sqlite3.connect(DB_PATH)
    links = json.load(open(LINKS_PATH))
    existing_dist_norm = {norm(r[1]): r[0] for r in conn.execute("SELECT id, name FROM distributors").fetchall()}
    existing_links = set(conn.execute("SELECT manufacturer_id, distributor_id FROM company_distributors").fetchall())

    linked, skipped = 0, 0
    for link in links:
        mfr_id = link['mfr_id']
        mfr_name = link['mfr_name']
        vendor_raw = link['vendor']
        country = link['country']
        tenders = ", ".join(link['tenders'])
        source = f"NUPCO Tender(s) {tenders} -- Final Awardation record"

        dist_id = get_or_create_distributor(conn, vendor_raw, country, source, existing_dist_norm)

        if (mfr_id, dist_id) in existing_links:
            skipped += 1
            continue

        conn.execute(
            "INSERT INTO company_distributors (manufacturer_id, distributor_id) VALUES (?, ?)",
            (mfr_id, dist_id)
        )
        existing_links.add((mfr_id, dist_id))

        represents = conn.execute("SELECT represents FROM distributors WHERE id = ?", (dist_id,)).fetchone()[0] or ""
        if mfr_name not in represents:
            new_represents = (represents + ", " if represents else "") + mfr_name
            conn.execute("UPDATE distributors SET represents = ? WHERE id = ?", (new_represents, dist_id))

        print(f"LINKED: {mfr_name} <-> {clean_vendor_name(vendor_raw)}")
        linked += 1

    conn.commit()
    total_distributors = conn.execute("SELECT COUNT(*) FROM distributors").fetchone()[0]
    total_links = conn.execute("SELECT COUNT(*) FROM company_distributors").fetchone()[0]
    conn.close()
    print(f"\nDone. Linked: {linked}, Skipped (dup): {skipped}")
    print(f"distributors table total: {total_distributors}")
    print(f"company_distributors table total: {total_links}")

if __name__ == "__main__":
    main()
