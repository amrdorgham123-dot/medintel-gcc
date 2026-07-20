"""
Adds a verified opportunity entry for Diatron (STRATEC Group) -- their own
official 2025 distributor-recruitment country list explicitly names
"KSA (Hematology only)" as an open market, meaning Diatron itself confirms
it currently has no Saudi hematology distributor. This is a directly
manufacturer-sourced finding, not an inference.

Source checked and rejected for comparison: QuidelOrtho was also
researched (a "Product Specialist CL - Saudi Arabia" job posting explicitly
describes monitoring "QuidelOrtho Distributors in the country"), which
indicates QuidelOrtho already has KSA distributor coverage -- so no
opportunity entry was created for QuidelOrtho, to avoid a false positive.

Run once: python3 add_opportunity_diatron.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    mfr = conn.execute("SELECT id FROM manufacturers WHERE name = 'Diatron'").fetchone()
    if not mfr:
        print("Diatron manufacturer not found -- skipping.")
        return
    existing = conn.execute("SELECT id FROM opportunities WHERE manufacturer_id = ?", (mfr[0],)).fetchone()
    if existing:
        print("Opportunity for Diatron already exists -- skipping.")
        return
    conn.execute(
        """INSERT INTO opportunities
        (manufacturer_id, reason, action, score_no_distributor, score_confidence, score_brand)
        VALUES (?,?,?,?,?,?)""",
        (
            mfr[0],
            "Diatron (STRATEC Group) officially lists Saudi Arabia as an open market on their own 2025 "
            "distributor recruitment country list, specifically for the hematology portfolio "
            "(\"KSA (Hematology only)\") -- confirming no current KSA hematology distributor from the "
            "manufacturer itself, not inferred.",
            "Contact Diatron directly via their distributor application form "
            "(surveymonkey.com/s/Distributor_Form) or their Our Distributors page, referencing the "
            "hematology-specific KSA gap on their own published country list. Their hematology line "
            "(Abacus 5/380/Junior 30, Aquila, Aquarius 3) is a natural complement to Attieh Medico's "
            "existing Snibe/Sysmex/Mindray hematology expertise for entry-level and mid-tier segments.",
            3, 3, 2,
        ),
    )
    conn.commit()
    print("Inserted Diatron opportunity. Total opportunities:",
          conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0])
    conn.close()

if __name__ == "__main__":
    main()
