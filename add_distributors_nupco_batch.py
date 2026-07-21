"""
Populates company_distributors with real, government-tender-verified
relationships extracted from two official NUPCO Final Awardation
documents (uploaded by the user):
  - NPT0003/23 "Supplementary LAB (A)", dated 18-Sep-2023
  - NPT0012/23 "LAB supplies BATCH (B)", dated 21-Nov-2023

This resolves 8 manufacturers that were previously flagged as
status_tag='unclear' after web research came up empty or ambiguous
(DiaSorin, Sansure Biotech, SD Biosensor, Nihon Kohden, EKF Diagnostics,
QuidelOrtho, Immucor) with a government-sourced, itemized award record
naming the exact vendor for each line item -- the strongest possible
source tier for this table.

Run once: python3 add_distributors_nupco_batch.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

# manufacturer_id (existing) -> list of (vendor_name, country, tender_source)
LINKS = {
    50: [  # DiaSorin
        ("AL KAMAL IMPORT OFFICE CO.,LTD.", "Saudi Arabia", "NUPCO Tender NPT0003/23 (Supplementary LAB A, 18-Sep-2023) -- awarded as DiaSorin distributor for BEP III immunology analyzer consumables"),
        ("Abdulla Fouad for medical supplies", "Saudi Arabia", "NUPCO Tender NPT0012/23 (LAB supplies Batch B, 21-Nov-2023) -- awarded as DiaSorin distributor"),
    ],
    57: [  # Sansure Biotech
        ("Al Osool Medical Trading Co", "Saudi Arabia", "NUPCO Tender NPT0003/23 (Supplementary LAB A, 18-Sep-2023) -- awarded as Sansure Biotech distributor for RT-PCR adenovirus detection kit"),
    ],
    59: [  # SD Biosensor
        ("RUSTOM MEDICAL Co.", "Saudi Arabia", "NUPCO Tender NPT0012/23 (LAB supplies Batch B, 21-Nov-2023) -- awarded as SD Biosensor distributor"),
    ],
    91: [  # Nihon Kohden Corporation
        ("Abdulla Fouad for medical supplies", "Saudi Arabia", "NUPCO Tender NPT0012/23 (LAB supplies Batch B, 21-Nov-2023) -- awarded as Nihon Kohden distributor"),
    ],
    89: [  # EKF Diagnostics
        ("GENERAL ANALYSIS FOR MEDICAL SERVICES CO", "Saudi Arabia", "NUPCO Tender NPT0012/23 (LAB supplies Batch B, 21-Nov-2023) -- awarded as EKF Diagnostics distributor"),
    ],
    54: [  # QuidelOrtho
        ("Abdulla Fouad for medical supplies", "Saudi Arabia", "NUPCO Tender NPT0012/23 (LAB supplies Batch B, 21-Nov-2023) -- awarded as QuidelOrtho (Quidel-branded line) distributor"),
    ],
    3: [  # Immucor (already noted as acquired by Werfen, 2023 -- recording the tender-level assignment as-is)
        ("Medical Supplies & Services Co. Ltd", "Saudi Arabia", "NUPCO Tenders NPT0003/23 and NPT0012/23 -- awarded as Immucor distributor at time of tender (note: Immucor was acquired by Werfen in 2023; this reflects the NUPCO award record, which may not yet reflect the post-acquisition corporate structure)"),
    ],
}

def get_or_create_distributor(conn, name, country, source):
    row = conn.execute("SELECT id, source FROM distributors WHERE name = ?", (name,)).fetchone()
    if row:
        return row[0]
    cur = conn.execute(
        "INSERT INTO distributors (name, country, represents, source, market_strength_tier, market_strength_basis) VALUES (?,?,?,?,?,?)",
        (name, country, "", source, "Tender-verified (partial)",
         "Confirmed via NUPCO tender award record; not independently confirmed for overall company size or revenue.")
    )
    return cur.lastrowid

def main():
    conn = sqlite3.connect(DB_PATH)
    linked, skipped = 0, 0
    for mfr_id, vendor_entries in LINKS.items():
        mfr = conn.execute("SELECT id, name, status_tag FROM manufacturers WHERE id = ?", (mfr_id,)).fetchone()
        if not mfr:
            print(f"SKIP (manufacturer not found): id={mfr_id}")
            continue
        for vendor_name, country, source in vendor_entries:
            dist_id = get_or_create_distributor(conn, vendor_name, country, source)
            existing_link = conn.execute(
                "SELECT id FROM company_distributors WHERE manufacturer_id = ? AND distributor_id = ?",
                (mfr_id, dist_id)
            ).fetchone()
            if existing_link:
                print(f"SKIP (link exists): {mfr[1]} <-> {vendor_name}")
                skipped += 1
                continue
            conn.execute(
                "INSERT INTO company_distributors (manufacturer_id, distributor_id) VALUES (?, ?)",
                (mfr_id, dist_id)
            )
            # append manufacturer name to distributor's "represents" field
            represents = conn.execute("SELECT represents FROM distributors WHERE id = ?", (dist_id,)).fetchone()[0] or ""
            if mfr[1] not in represents:
                new_represents = (represents + ", " if represents else "") + mfr[1]
                conn.execute("UPDATE distributors SET represents = ? WHERE id = ?", (new_represents, dist_id))
            print(f"LINKED: {mfr[1]} <-> {vendor_name}")
            linked += 1
        # Update manufacturer status_tag from 'unclear' to 'covered' now that we have a confirmed distributor
        if mfr[2] == "unclear":
            conn.execute("UPDATE manufacturers SET status_tag = 'covered' WHERE id = ?", (mfr_id,))
            print(f"  -> status_tag updated to 'covered' for {mfr[1]}")

    conn.commit()
    conn.close()
    print(f"\nDone. Linked: {linked}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
