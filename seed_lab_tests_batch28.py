"""
Seed script (batch 28) for MedForsa GCC's Lab Info reference library.
Adds JAK2 V617F Mutation, BCR-ABL1 Quantitative PCR, Aldolase, and MTHFR
Mutation Testing.

Run once: python3 seed_lab_tests_batch28.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "jak2-v617f", "name_en": "JAK2 V617F Mutation Analysis",
        "aliases": "JAK2 Mutation, JAK2 V617F",
        "category": "Hematology / Molecular",
        "purpose_en": "Key diagnostic test for BCR-ABL1-negative myeloproliferative neoplasms (polycythemia vera, essential thrombocythemia, primary myelofibrosis), used to evaluate unexplained sustained elevation of red cell or platelet counts, splenomegaly, or bone marrow fibrosis of undetermined cause.",
        "specimen_type": "Venous whole blood or bone marrow, EDTA tube",
        "collection_notes_en": "No special preparation required. Can be performed on peripheral blood in most cases, avoiding the need for a bone marrow sample specifically for this test.",
        "methodology_en": "Allele-specific PCR (ARMS-PCR) or quantitative real-time PCR (qPCR) detecting the specific c.1849G>T (p.Val617Phe) point mutation in the JAK2 gene; quantitative methods also report the mutant allele burden as a percentage.",
        "reference_ranges": [{"parameter": "JAK2 V617F", "population": "Result categories", "range": "Not detected (negative) or Detected/Positive (with mutant allele burden % if quantitative testing is used)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "The JAK2 V617F mutation is detected in approximately 95-98% of polycythemia vera cases, and 50-60% of essential thrombocythemia and primary myelofibrosis cases, making it a highly useful diagnostic marker when positive. A negative result does not rule out any of these myeloproliferative neoplasms, since a meaningful proportion of ET and PMF cases are JAK2-negative but may carry a CALR or MPL mutation instead (these three mutations are essentially mutually exclusive). The mutation is not seen in reactive causes of elevated blood counts or in BCR-ABL1-positive chronic myeloid leukemia, helping distinguish true myeloproliferative neoplasms from secondary/reactive processes. Rising allele burden over time, or transition from heterozygous to homozygous status, has been associated with disease progression in some studies.",
        "associated_conditions": [
            {"condition": "Polycythemia vera", "direction": "positive in ~95-98% of cases"},
            {"condition": "Essential thrombocythemia", "direction": "positive in ~50-60% of cases"},
            {"condition": "Primary myelofibrosis", "direction": "positive in ~50-65% of cases"}
        ],
        "questions_to_ask_en": "Does a positive result confirm my diagnosis, or do I need bone marrow examination too? What does my specific allele burden mean for my prognosis? If negative, do I need testing for CALR or MPL mutations instead?",
        "next_steps": "A positive result, combined with your blood counts and bone marrow findings, generally confirms the diagnosis of a JAK2-mutated myeloproliferative neoplasm and guides risk stratification and treatment planning with hematology. A negative result in someone still suspected of having an MPN typically leads to CALR and MPL mutation testing before the diagnosis is reconsidered.",
        "sources": [
            {"name": "Mayo Clinic Laboratories - JAK2 V617F Mutation Detection, Blood (test catalog)", "url": "https://hematology.testcatalog.org/show/JAK2B", "accessed": "2026-07-19"},
            {"name": "MLabs (University of Michigan) - JAK2 V617F Mutation (test catalog)", "url": "https://mlabs.umich.edu/tests/jak2-v617f-mutation", "accessed": "2026-07-19"}
        ]
    },
    {
        "slug": "bcr-abl1-quantitative", "name_en": "BCR-ABL1 Quantitative PCR (International Scale)",
        "aliases": "BCR-ABL1, Philadelphia Chromosome PCR, CML Molecular Monitoring",
        "category": "Hematology / Molecular",
        "purpose_en": "Diagnoses and monitors chronic myeloid leukemia (CML) and Philadelphia chromosome-positive acute lymphoblastic leukemia by detecting and quantifying the BCR-ABL1 fusion transcript, and is the standard test for monitoring molecular response to tyrosine kinase inhibitor (TKI) therapy.",
        "specimen_type": "Venous whole blood or bone marrow (peripheral blood is standard for routine monitoring)",
        "collection_notes_en": "Typically collected in an RNA-stabilizing tube per the testing laboratory's requirements, since RNA is less stable than DNA and results depend on adequate transcript preservation during transport.",
        "methodology_en": "Real-time quantitative reverse-transcriptase PCR (RT-qPCR) detecting the BCR-ABL1 fusion transcript (most commonly e13a2/e14a2, 'major' breakpoint) relative to a control gene (ABL1), with results standardized to the International Scale (IS) to allow comparison across laboratories.",
        "reference_ranges": [
            {"parameter": "BCR-ABL1 (International Scale)", "population": "Major molecular response (MMR)", "range": "\u22640.1% IS (a 3-log reduction from a standardized baseline)"},
            {"parameter": "BCR-ABL1 (International Scale)", "population": "Deep molecular response (MR4)", "range": "\u22640.01% IS"},
            {"parameter": "BCR-ABL1 (International Scale)", "population": "Deep molecular response (MR4.5)", "range": "\u22640.0032% IS"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "In newly diagnosed CML, the baseline BCR-ABL1 level (before treatment) is used as the reference point for tracking log-reduction in response to TKI therapy (imatinib, nilotinib, dasatinib, and others). Achieving a major molecular response (BCR-ABL1 \u22640.1% IS) by 12 months of treatment is a key treatment milestone associated with excellent long-term outcomes, while failure to reach expected milestones prompts consideration of treatment adherence issues, resistance mutations, or a change in therapy. Deeper molecular responses (MR4, MR4.5) are increasingly used to identify patients who may be candidates for treatment-free remission (stopping TKI therapy under close monitoring) in appropriate clinical trials or protocols.",
        "associated_conditions": [
            {"condition": "Chronic myeloid leukemia (diagnosis and monitoring)", "direction": "detectable at diagnosis, tracked serially during treatment"},
            {"condition": "Philadelphia chromosome-positive acute lymphoblastic leukemia", "direction": "detectable, monitored similarly"},
            {"condition": "Treatment failure / TKI resistance", "direction": "failure to achieve expected log-reduction milestones, or rising level after a response"}
        ],
        "questions_to_ask_en": "Am I on track to meet my expected molecular response milestones for this stage of treatment? Does this result mean my current TKI is working, or should we consider a change? Could this level make me eligible for treatment-free remission in the future?",
        "next_steps": "Results are tracked serially against established treatment milestones (typically at 3, 6, and 12 months after starting therapy); failure to meet expected milestones prompts assessment of medication adherence, mutation testing for TKI resistance, and consideration of switching to a different tyrosine kinase inhibitor.",
        "sources": [
            {"name": "ScienceDirect - BCR-ABL1 RT-qPCR for Monitoring the Molecular Response to Tyrosine Kinase Inhibitors in Chronic Myeloid Leukemia", "url": "https://www.sciencedirect.com/science/article/pii/S1525157813001001", "accessed": "2026-07-19"},
            {"name": "PMC - A new highly sensitive real-time quantitative-PCR method for detection of BCR-ABL1 to monitor minimal residual disease in chronic myeloid leukemia (International Scale / MMR definitions)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6400442/", "accessed": "2026-07-19"},
            {"name": "Labcorp - BCR-ABL1 Transcript Detection for CML and ALL, Quantitative (test description)", "url": "https://www.labcorp.com/tests/480481/bcr-abl1-transcript-detection-for-chronic-myelogenous-leukemia-cml-and-acute-lymphocytic-leukemia-all-quantitative", "accessed": "2026-07-19"}
        ]
    },
    {
        "slug": "aldolase", "name_en": "Aldolase, Serum",
        "aliases": "Aldolase",
        "category": "Clinical Chemistry",
        "purpose_en": "Marker of muscle and liver cell damage, used to investigate suspected inflammatory myopathy (polymyositis, dermatomyositis) particularly when creatine kinase (CK) is normal, and to help distinguish muscular from neurological causes of weakness.",
        "specimen_type": "Venous serum, collected in a red-top (no additive) tube",
        "collection_notes_en": "No fasting required. Recent strenuous exercise or intramuscular injections can transiently raise levels, similar to CK.",
        "methodology_en": "Enzymatic (ultraviolet or coupled enzymatic) assay on automated chemistry analyzers; not offered as a routine test by all laboratories.",
        "reference_ranges": [{"parameter": "Aldolase", "population": "Adult", "range": "Approximately 1.0-7.5 U/L (some sources cite up to 8.2 U/L)", "notes": "Newborns and children have higher reference ranges (up to ~4x and ~2x the adult value respectively); reference range varies by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated aldolase supports muscle damage or an inflammatory myopathy (polymyositis, dermatomyositis, inclusion body myositis), and is particularly useful when CK is normal despite clinical suspicion of myopathy -- a pattern (isolated aldolase elevation with normal CK) seen in a meaningful subset of dermatomyositis patients, who in one Mayo Clinic cohort had less cutaneous involvement but more perifascicular mitochondrial pathology than those with elevated CK. Aldolase does not rise in weakness caused by neurological (rather than muscular) disease, making it useful for that distinction. It is nonspecific, however, and also elevated in liver disease, myocardial infarction, and some hemolytic anemias, so results are interpreted alongside CK, clinical exam, and other muscle/liver markers.",
        "associated_conditions": [
            {"condition": "Polymyositis / dermatomyositis (especially with normal CK)", "direction": "high"},
            {"condition": "Muscular dystrophy / other myopathies", "direction": "high"},
            {"condition": "Liver disease (nonspecific elevation)", "direction": "high"}
        ],
        "questions_to_ask_en": "Given my CK is normal, does this elevated aldolase still support a muscle disease diagnosis? Do I need a muscle biopsy to confirm? Could this be related to my liver instead of my muscles?",
        "next_steps": "An elevated aldolase with clinical weakness, especially when CK is normal, typically prompts further myositis workup (autoantibody panel, EMG, muscle biopsy) with rheumatology or neurology, since this pattern can represent a distinct and treatable subset of inflammatory myopathy.",
        "sources": [
            {"name": "Medscape/eMedicine - Aldolase: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2087158-overview", "accessed": "2026-07-19"},
            {"name": "PMC - Disease spectrum of myopathies with elevated aldolase and normal creatine kinase (Mayo Clinic cohort study)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11235866/", "accessed": "2026-07-19"}
        ]
    },
    {
        "slug": "mthfr-mutation", "name_en": "MTHFR Mutation Testing (C677T / A1298C)",
        "aliases": "MTHFR, MTHFR Gene Mutation",
        "category": "Hematology / Molecular",
        "purpose_en": "Detects the two most common variants (C677T and A1298C) in the MTHFR gene, which affect folate metabolism and homocysteine processing; historically ordered as part of thrombophilia panels, though current major medical society guidance does not recommend routine testing for this purpose.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "No fasting or special preparation required; this is a DNA-based test unaffected by current physiological state.",
        "methodology_en": "PCR-based genotyping detecting the specific C677T (rs1801133) and A1298C (rs1801131) single nucleotide variants.",
        "reference_ranges": [{"parameter": "MTHFR C677T and A1298C", "population": "Result categories", "range": "Homozygous wild-type, heterozygous, or homozygous variant for each of the two positions -- a genetic result, not a numeric value; C677T heterozygosity occurs in ~30-40% and homozygosity in ~10-15% of White European/Hispanic populations, with substantial variation by ethnicity"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "The C677T variant reduces MTHFR enzyme activity and, particularly in the homozygous (TT) state combined with low folate status, can raise homocysteine levels. However, major medical organizations including the American College of Medical Genetics and the American Heart Association do not recommend routine MTHFR genotyping for the general population, including for most thrombophilia workups, since homocysteine level itself (rather than the genotype) is the more clinically actionable measurement -- many people with an MTHFR variant never develop elevated homocysteine, and the CDC states that finding an MTHFR mutation generally 'has no clinical implications for the patient.' The A1298C variant alone is generally considered to have minimal clinical significance. When relevant, an elevated homocysteine (rather than the MTHFR genotype itself) is what typically prompts folate/B12/B6 supplementation.",
        "associated_conditions": [
            {"condition": "Mildly elevated homocysteine (in homozygous C677T with low folate status)", "direction": "positive genotype, only relevant if homocysteine is also elevated"},
            {"condition": "Generally minimal independent clinical significance", "direction": "positive genotype without elevated homocysteine"}
        ],
        "questions_to_ask_en": "Given current guidelines don't recommend routine MTHFR testing, why was this ordered, and does the result actually change my management? Should my homocysteine level be checked directly instead of relying on this genotype result? Does this affect anything about a current or future pregnancy?",
        "next_steps": "In most cases, an MTHFR result by itself does not lead to specific treatment -- your clinician will likely check (or already have checked) a homocysteine level, since that is the measurement that actually guides whether folate/B-vitamin supplementation or further workup is warranted, rather than the genotype alone.",
        "sources": [
            {"name": "World Thrombosis Day - Thrombophilia Testing and MTHFR", "url": "https://www.worldthrombosisday.org/thrombophilia-testing-and-mthfr/", "accessed": "2026-07-19"},
            {"name": "AskMyDNA - MTHFR Gene Mutation Complete Guide (citing CDC and ACMG/AHA guidance)", "url": "https://www.askmydna.com/en/blog/mthfr-gene-mutation-complete-guide", "accessed": "2026-07-19"}
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
        related = ["cbc"] if t["slug"] in ("jak2-v617f", "bcr-abl1-quantitative") else (
            ["creatine-kinase-total", "myoglobin"] if t["slug"] == "aldolase" else
            ["homocysteine", "folate", "vitamin-b12"]
        )
        conn.execute(
            """INSERT INTO lab_tests
            (slug, name_en, name_ar, aliases, category, purpose_en, purpose_ar, specimen_type,
             collection_notes_en, collection_notes_ar, methodology_en, methodology_ar,
             reference_ranges_json, reference_ranges_verified, clinical_significance_en, clinical_significance_ar,
             questions_to_ask_en, next_steps_en,
             associated_conditions_json, related_tests_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             t.get("questions_to_ask_en"), t.get("next_steps"),
             json.dumps(t.get("associated_conditions", [])),
             json.dumps(related),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
