"""
Seed script (batch 3) for MedForsa GCC's Lab Info reference library.
Adds core Blood Bank / Transfusion Medicine (Immunohematology) tests.
English-only content per platform policy.
Sources: StatPearls/NCBI Bookshelf, AABB-referenced clinical literature (PMC/PubMed),
Labcorp/Testing.com consumer test descriptions cross-checked against StatPearls.

Run once: python3 seed_lab_tests_batch3.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

STATPEARLS_PRETRANSFUSION = {"name": "StatPearls / NCBI Bookshelf - Pretransfusion Testing", "url": "https://www.ncbi.nlm.nih.gov/books/NBK585033/", "accessed": "2026-07-14"}
STATPEARLS_COOMBS = {"name": "StatPearls / NCBI Bookshelf - Coombs Test", "url": "https://www.ncbi.nlm.nih.gov/books/NBK547707/", "accessed": "2026-07-14"}
PMC_GROUPING_XM = {"name": "PMC - Practical Solutions for Problems in Blood Grouping and Crossmatching", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8886265/", "accessed": "2026-07-14"}

TESTS = [
    {
        "slug": "abo-rh-typing", "name_en": "ABO Grouping & Rh(D) Typing",
        "aliases": "Blood Typing, ABO/Rh, Blood Group and Type",
        "category": "Blood Bank / Immunohematology",
        "purpose_en": "Determines a person's ABO blood group (A, B, AB, or O) and RhD status (positive/negative). Foundational test for transfusion candidates, prenatal/newborn care (risk of ABO or Rh hemolytic disease of the newborn), and organ/tissue/bone marrow transplant workup.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "Positive patient identification at the time of collection is critical -- mislabeled samples are a leading cause of ABO-incompatible transfusion errors. A second confirmatory sample is often required for first-time patients per institutional policy.",
        "methodology_en": "Hemagglutination technique: forward typing (patient RBCs mixed with known anti-A and anti-B reagent antisera) and reverse typing (patient serum/plasma mixed with known A and B reagent red cells) to cross-check results; Rh(D) typing uses anti-D reagent antiserum. Performed by tube, gel-card (column agglutination), or automated solid-phase methods.",
        "reference_ranges": [
            {"parameter": "ABO group", "population": "Result categories", "range": "A, B, AB, or O"},
            {"parameter": "Rh(D) type", "population": "Result categories", "range": "Positive or Negative"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "ABO and RhD are the most immunogenic red cell antigens; mismatched transfusion can cause acute hemolytic transfusion reactions, which can be fatal. RhD-negative individuals (especially pregnant women) who are exposed to RhD-positive blood (transfusion, delivery, sensitizing events in pregnancy) are at risk of forming anti-D antibodies, which can cause hemolytic disease of the fetus/newborn in future RhD-positive pregnancies -- this risk is mitigated by giving Rh immune globulin at appropriate times. Discrepancies between forward and reverse typing require investigation before a result is finalized (e.g., weak/partial D variants, cold autoagglutinins, recent transfusion, or abnormal plasma proteins).",
        "associated_conditions": [
            {"condition": "ABO-incompatible transfusion risk", "direction": "mismatch between donor/recipient ABO group"},
            {"condition": "Rh alloimmunization / hemolytic disease of the fetus and newborn (HDFN)", "direction": "RhD-negative patient exposed to RhD-positive cells"}
        ],
        "sources": [PMC_GROUPING_XM, {"name": "Labcorp - ABO Grouping and Rho(D) Typing test description", "url": "https://www.labcorp.com/tests/006049/abo-grouping-and-rho-d-typing", "accessed": "2026-07-14"}]
    },
    {
        "slug": "antibody-screen", "name_en": "Antibody Screen (Indirect Antiglobulin Test / IAT)",
        "aliases": "Antibody Screen, IAT, Indirect Coombs Test, Type and Screen",
        "category": "Blood Bank / Immunohematology",
        "purpose_en": "Detects clinically significant unexpected (non-ABO) antibodies in a patient's plasma/serum against red cell antigens, prior to transfusion or during pregnancy workup. Forms the 'screen' half of routine pretransfusion 'type and screen' testing.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top) or clot tube",
        "collection_notes_en": "Sample validity period for pretransfusion testing is typically limited (commonly 72 hours) if the patient has been pregnant or transfused within the prior 3 months, per institutional/AABB-aligned policy, due to the risk of new antibody formation.",
        "methodology_en": "Patient plasma/serum is incubated with 2-3 reagent group O red cells of known antigen profile (selected to detect clinically significant antibodies), then tested through saline, 37\u00b0C, and antihuman globulin (AHG) phases; agglutination at the AHG phase indicates a positive screen. Performed by tube, gel-card, or solid-phase methods.",
        "reference_ranges": [{"parameter": "Antibody screen", "population": "Result categories", "range": "Negative (no clinically significant antibody detected) or Positive (requires antibody identification panel)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A negative screen with no history of clinically significant antibodies generally allows an immediate-spin or electronic crossmatch, speeding blood availability. A positive screen requires antibody identification to determine specificity and clinical significance before selecting compatible donor units -- this can delay transfusion, so early testing is important in patients likely to need blood (e.g., before scheduled surgery). In pregnancy, a positive screen with a clinically significant antibody (e.g., anti-D, anti-Kell) prompts titer monitoring for risk of hemolytic disease of the fetus/newborn.",
        "associated_conditions": [
            {"condition": "Alloimmunization from prior transfusion or pregnancy", "direction": "positive"},
            {"condition": "Delayed hemolytic transfusion reaction risk", "direction": "positive, with history of undetected antibody"},
            {"condition": "Hemolytic disease of the fetus/newborn risk (pregnancy)", "direction": "positive, with clinically significant antibody"}
        ],
        "sources": [STATPEARLS_PRETRANSFUSION, PMC_GROUPING_XM]
    },
    {
        "slug": "dat-coombs", "name_en": "Direct Antiglobulin Test (DAT / Direct Coombs Test)",
        "aliases": "DAT, Direct Coombs, Direct Antiglobulin",
        "category": "Blood Bank / Immunohematology",
        "purpose_en": "Detects antibodies and/or complement already bound to a patient's own red blood cells in vivo. Used to investigate suspected autoimmune hemolytic anemia, hemolytic disease of the newborn, and suspected transfusion or drug-induced hemolysis.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "Not used for routine pretransfusion compatibility testing on its own (it does not assess the patient's plasma antibodies) -- it evaluates the patient's own red cells.",
        "methodology_en": "Patient red cells are washed with saline to remove unbound antibody, then antihuman globulin (AHG) reagent (polyspecific, or monospecific anti-IgG / anti-complement) is added; agglutination indicates antibody and/or complement is bound to the cells.",
        "reference_ranges": [{"parameter": "DAT", "population": "Result categories", "range": "Negative (no bound antibody/complement detected) or Positive"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive DAT supports a diagnosis of autoimmune hemolytic anemia (AIHA), hemolytic disease of the fetus/newborn, hemolytic transfusion reaction, or drug-induced immune hemolysis, but must be interpreted alongside clinical and other laboratory findings (e.g., LDH, haptoglobin, bilirubin, reticulocyte count) since 2-4% of patients with clinical AIHA can have a negative DAT, and some healthy individuals have a weakly positive DAT with no hemolysis.",
        "associated_conditions": [
            {"condition": "Autoimmune hemolytic anemia (AIHA)", "direction": "positive"},
            {"condition": "Hemolytic disease of the fetus/newborn (HDFN)", "direction": "positive, on newborn's cells"},
            {"condition": "Hemolytic transfusion reaction", "direction": "positive, post-transfusion"},
            {"condition": "Drug-induced immune hemolysis", "direction": "positive"}
        ],
        "sources": [STATPEARLS_COOMBS]
    },
    {
        "slug": "crossmatch", "name_en": "Crossmatch (Compatibility Testing)",
        "aliases": "Crossmatch, XM, Type and Crossmatch, Compatibility Test",
        "category": "Blood Bank / Immunohematology",
        "purpose_en": "Final pretransfusion step confirming serologic compatibility between a specific donor red cell unit and the intended recipient, before the unit is released for transfusion.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top) or clot tube",
        "collection_notes_en": "Requires a valid ABO/Rh type and antibody screen on file; sample validity period rules (commonly 72 hours if recently pregnant/transfused) apply as with the antibody screen.",
        "methodology_en": "Three main methods depending on antibody screen results and local policy: (1) Immediate-spin crossmatch -- rapid room-temperature check for ABO incompatibility only, used when the antibody screen is negative and no clinically significant antibody history exists; (2) Antiglobulin (AHG/IAT) crossmatch -- donor cells incubated with recipient plasma through saline, 37\u00b0C, and AHG phases, required if a clinically significant antibody is present or suspected; (3) Electronic (computer) crossmatch -- a validated computer system verifies ABO compatibility against donor unit records without physical serologic testing, used only when the antibody screen is negative and the system meets validation requirements.",
        "reference_ranges": [{"parameter": "Crossmatch", "population": "Result categories", "range": "Compatible (no agglutination/hemolysis -- unit may be released) or Incompatible (unit must not be released for that patient)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "An incompatible crossmatch means the selected donor unit is not safe for that patient and another unit must be selected/tested; it may indicate a clinically significant antibody was missed on screening, a technical/clerical error, or a rare antigen incompatibility. In urgent situations, uncrossmatched group O (RhD-negative for females of childbearing potential) red cells may be issued per institutional emergency-release protocols while full compatibility testing is completed.",
        "associated_conditions": [
            {"condition": "Undetected or newly-identified alloantibody", "direction": "incompatible result"},
            {"condition": "Clerical/technical error in sample or unit identification", "direction": "incompatible result"}
        ],
        "sources": [STATPEARLS_PRETRANSFUSION]
    },
    {
        "slug": "antibody-identification", "name_en": "Antibody Identification Panel",
        "aliases": "Antibody ID Panel, Panel Reactive Antibody Identification",
        "category": "Blood Bank / Immunohematology",
        "purpose_en": "Determines the specific identity (e.g., anti-D, anti-K, anti-Fya) of an unexpected red cell antibody detected on a positive antibody screen, so that antigen-negative, compatible donor units can be selected.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top) or clot tube",
        "collection_notes_en": "Requires a positive antibody screen result to trigger; testing follows the same sample validity rules as the antibody screen.",
        "methodology_en": "Patient plasma is tested against a panel of typically 10-16 reagent red cells of known, differing antigen profiles (antigram) through saline, 37\u00b0C, and antihuman globulin phases; the reaction pattern across the panel cells is matched against their known antigen profiles to identify the antibody specificity (or specificities, if more than one is present).",
        "reference_ranges": [{"parameter": "Antibody identification", "population": "Result categories", "range": "Specific antibody identified (e.g., anti-D, anti-K, anti-E) or unresolved/multiple antibodies requiring further workup"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Identifying the antibody specificity determines which donor units must be selected (antigen-negative for that specificity) to avoid a hemolytic transfusion reaction, and whether the antibody is clinically significant (capable of causing in-vivo hemolysis) versus clinically insignificant (e.g., some cold-reactive antibodies). In pregnancy, identifying antibodies known to cause hemolytic disease of the fetus/newborn (notably anti-D, anti-c, anti-K) guides titer monitoring and fetal surveillance.",
        "associated_conditions": [
            {"condition": "Alloimmunization requiring antigen-matched blood for future transfusions", "direction": "clinically significant antibody identified"},
            {"condition": "Hemolytic disease of the fetus/newborn risk (pregnancy)", "direction": "anti-D, anti-c, or anti-K identified"}
        ],
        "sources": [PMC_GROUPING_XM]
    },
    {
        "slug": "kleihauer-betke", "name_en": "Kleihauer-Betke Test (Fetomaternal Hemorrhage Quantification)",
        "aliases": "KB Test, KB Stain, Fetomaternal Hemorrhage Test, Acid Elution Test",
        "category": "Blood Bank / Immunohematology",
        "purpose_en": "Quantifies the volume of fetal blood that has entered the maternal circulation (fetomaternal hemorrhage), most often after trauma, delivery, or other sensitizing events in RhD-negative mothers, to calculate the correct dose of Rh immune globulin needed to prevent maternal RhD alloimmunization.",
        "specimen_type": "Maternal venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "Typically performed only after a qualitative screening test (e.g., rosette test) is positive, since the rosette test is more sensitive for excluding clinically significant hemorrhage and the Kleihauer-Betke test is used to precisely quantify it.",
        "methodology_en": "A maternal blood smear is exposed to an acid buffer (citric acid-phosphate), which elutes adult hemoglobin (HbA) from maternal red cells but not fetal hemoglobin (HbF), which is acid-resistant; after staining, fetal cells appear dark/rose-pink while maternal 'ghost' cells appear pale, and the percentage of fetal cells is counted microscopically (flow cytometry is an alternative, more precise method in some centers).",
        "reference_ranges": [{"parameter": "Fetal cells on smear", "population": "Interpretation", "range": "Percentage observed is used directly in the RhIG dosing calculation (see clinical significance) -- there is no single 'normal' cutoff value"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "The standard 300 mcg dose of Rh immune globulin covers a fetomaternal hemorrhage of up to 30 mL of whole fetal blood (15 mL of fetal red cells). When the Kleihauer-Betke result indicates a larger hemorrhage, additional vials are calculated as: volume of fetal blood (mL) = % fetal cells x 50; number of additional 300 mcg vials = that volume / 30 (rounding per institutional protocol). As little as 0.01-0.03 mL of fetal blood can be enough to cause maternal Rh sensitization, which is why RhIG is given even when the screening test is negative for detectable hemorrhage.",
        "associated_conditions": [
            {"condition": "Large fetomaternal hemorrhage after trauma, abruption, or invasive obstetric procedures", "direction": "high percentage of fetal cells -- requires additional RhIG dosing"},
            {"condition": "Rh alloimmunization prevention in RhD-negative mothers", "direction": "guides correct RhIG dose"}
        ],
        "sources": [
            {"name": "StatPearls / NCBI Bookshelf - Kleihauer-Betke Test", "url": "https://www.ncbi.nlm.nih.gov/books/NBK430876/", "accessed": "2026-07-14"},
            {"name": "WikEM - Kleihauer-Betke test (mechanism and clinical summary)", "url": "https://www.wikem.org/wiki/Kleihauer-Betke_test", "accessed": "2026-07-14"}
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
             associated_conditions_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             json.dumps(t.get("associated_conditions", [])), json.dumps(t["sources"]),
             1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
