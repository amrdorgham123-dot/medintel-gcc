"""
Seed script (batch 25) for MedForsa GCC's Lab Info reference library.
Adds Extended Rh Phenotype (C/c/E/e) and Weak D Testing -- both Blood Bank /
Immunohematology, directly relevant to Amr's transfusion medicine focus.

Run once: python3 seed_lab_tests_batch25.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "rh-phenotype-extended", "name_en": "Extended Rh Phenotype (C/c/E/e Antigen Typing)",
        "aliases": "Rh Phenotype, Rh Antigen Typing, CcEe Typing",
        "category": "Blood Bank / Immunohematology",
        "purpose_en": "Determines the full Rh antigen profile (C, c, E, e, in addition to D) of a patient's or donor's red cells; used for antigen-matched transfusion in chronically transfused patients (e.g., sickle cell disease, thalassemia) to reduce alloimmunization risk, and to help resolve or predict specific Rh antibody identifications.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "Recent transfusion introduces donor red cells that can cause a mixed-field or inaccurate phenotype result -- testing is ideally done on a pre-transfusion sample, or DNA-based genotyping is used instead when a recent transfusion makes serologic phenotyping unreliable.",
        "methodology_en": "Hemagglutination technique using monoclonal antisera specific to each antigen (anti-C, anti-c, anti-E, anti-e), performed by tube, gel-card, or automated solid-phase methods; molecular (RHCE genotyping) methods are used when serologic results are ambiguous or the patient has been recently transfused.",
        "reference_ranges": [{"parameter": "Rh phenotype (C/c/E/e)", "population": "Result categories", "range": "Each antigen reported as present or absent, combined into a phenotype designation (e.g., DCCee, DCcee, DccEe)", "notes": "Population frequencies vary by ethnicity -- e.g., one hospital donor study found DCCee (~46%) and DCcee (~30%) as the most common phenotypes, with e (~97%) and D (~99%) the most prevalent individual antigens and E (~21%) the least"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "After D, the C/c/E/e antigens are among the most clinically significant in transfusion medicine because of their immunogenicity and the clinical severity of antibodies formed against them (e.g., anti-c and anti-E can cause both hemolytic transfusion reactions and hemolytic disease of the fetus/newborn). Extended phenotype matching (beyond ABO/D alone) is standard of care for patients requiring chronic transfusion support, most notably sickle cell disease and thalassemia patients, since it substantially reduces the rate of alloimmunization compared to D-only matching. Certain antigen combinations are also population-dependent -- for example, the C-c+E-e+ phenotype is typically associated with Rh-positive haplotypes in patients of African ancestry but Rh-negative haplotypes in Caucasian patients, which is relevant when predicting likely genotype from phenotype.",
        "associated_conditions": [
            {"condition": "Sickle cell disease / thalassemia requiring chronic transfusion", "direction": "guides extended antigen-matched unit selection"},
            {"condition": "Alloimmunization to non-D Rh antigens (anti-C, anti-c, anti-E, anti-e)", "direction": "phenotype used to select antigen-negative units"},
            {"condition": "Hemolytic disease of the fetus/newborn risk (non-D Rh antibodies)", "direction": "maternal phenotype/antibody correlation in prenatal care"}
        ],
        "sources": [
            {"name": "PMC - Distribution and frequency of principal Rh blood group antigens (D, C, c, E, and e) in blood donors", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9855209/", "accessed": "2026-07-15"},
            {"name": "ScienceDirect Topics - Rh Blood Group System", "url": "https://www.sciencedirect.com/topics/immunology-and-microbiology/rh-blood-group-system", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "weak-d-testing", "name_en": "Weak D Testing",
        "aliases": "Weak D, Du Testing, Partial D Testing",
        "category": "Blood Bank / Immunohematology",
        "purpose_en": "Resolves an ambiguous or discrepant RhD typing result by detecting weak expression of the D antigen using an indirect antiglobulin (AHG) enhancement step; historically also used more broadly, though current practice reserves it for specific discrepancy/ambiguity scenarios rather than routine typing.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "Performed as a reflex test when initial RhD typing is negative or gives a weak/ambiguous reaction (commonly \u22642+ agglutination), or when there is a discrepancy with a patient's historical Rh type on record.",
        "methodology_en": "An indirect antiglobulin test (IAT): red cells are incubated with anti-D reagent, then antihuman globulin (AHG) is added to enhance and detect otherwise weak or undetectable agglutination; a positive result after AHG addition indicates weak or partial D antigen expression. When serology remains ambiguous, RHD molecular genotyping is used to definitively classify the specific weak D type.",
        "reference_ranges": [{"parameter": "Weak D test", "population": "Result categories", "range": "Negative (true RhD-negative) or Positive (weak/partial D detected) -- approximately 0.2-1.0% of routine RhD typings in Caucasian populations result in a serologic weak D phenotype"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "How a weak D result is managed differs sharply depending on the clinical role of the person tested. Blood donors with a serologic weak D phenotype are conventionally managed as RhD-positive for donation purposes. Transfusion recipients and pregnant women, by contrast, have traditionally been managed as RhD-negative out of caution, since some weak D variants (though not the common weak D types 1, 2, and 3) carry a real risk of forming anti-D antibodies if given RhD-positive blood or exposed to RhD-positive fetal cells. Molecular RHD genotyping can now distinguish weak D types 1, 2, and 3 (which can safely be managed as RhD-positive, avoiding unnecessary Rh immune globulin and preserving the RhD-negative blood supply) from other weak D types and partial D variants that still carry alloimmunization risk and should continue to be managed as RhD-negative.",
        "associated_conditions": [
            {"condition": "Weak D phenotype (blood donor)", "direction": "positive -- generally managed as RhD-positive for donation"},
            {"condition": "Weak D phenotype (transfusion recipient or pregnant patient)", "direction": "positive -- traditionally managed as RhD-negative unless RHD genotyping confirms a low-risk weak D type"},
            {"condition": "Partial D phenotype (alloimmunization risk if given RhD-positive blood)", "direction": "positive on weak D screen, requires genotyping to distinguish from benign weak D types"}
        ],
        "sources": [
            {"name": "StatPearls / NCBI Bookshelf - Rh Blood Group System", "url": "https://www.ncbi.nlm.nih.gov/books/NBK594252/", "accessed": "2026-07-15"},
            {"name": "PMC - Serological weak D phenotypes: A review and guidance for interpreting the RhD blood type using the RHD genotype", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5612847/", "accessed": "2026-07-15"},
            {"name": "Medscape/eMedicine - Rh Typing: Overview, Clinical Indications/Applications, Test Performance and Limitations", "url": "https://emedicine.medscape.com/article/1731214-overview", "accessed": "2026-07-15"}
        ]
    }
]

def main():
    conn = sqlite3.connect(DB_PATH)
    inserted, skipped = 0, 0
    for t in TESTS:
        existing = conn.execute("SELECT id FROM lab_tests WHERE slug = ?", (t["slug"],)).fetchone()
        if existing:
            print(f"SKIP (already exists): {t['slug']}")
            skipped += 1
            continue
        conn.execute(
            """INSERT INTO lab_tests
            (slug, name_en, name_ar, aliases, category, purpose_en, purpose_ar, specimen_type,
             collection_notes_en, collection_notes_ar, methodology_en, methodology_ar,
             reference_ranges_json, reference_ranges_verified, clinical_significance_en, clinical_significance_ar,
             associated_conditions_json, related_tests_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             json.dumps(t.get("associated_conditions", [])),
             json.dumps(["abo-rh-typing", "antibody-screen", "antibody-identification", "kleihauer-betke"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
