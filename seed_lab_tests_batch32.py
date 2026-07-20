"""
Seed script (batch 32) for MedForsa GCC's Lab Info reference library.
Adds Calcitonin, Anti-Mitochondrial Antibody (AMA), Anti-Smooth Muscle
Antibody (ASMA), Vitamin B6 (Pyridoxal 5'-Phosphate), and Vitamin A (Retinol).

Run once: python3 seed_lab_tests_batch32.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "calcitonin", "name_en": "Calcitonin, Serum",
        "aliases": "Calcitonin, CT",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Primary tumor marker for medullary thyroid carcinoma (MTC), used to help evaluate a thyroid nodule when MTC is suspected, and to monitor for residual or recurrent disease after thyroidectomy.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required for most assays. Levels are affected by sex (higher in men) and can be falsely low in early childhood; some centers use a pentagastrin or calcium stimulation test to increase sensitivity in equivocal cases, though pentagastrin is not available in all countries.",
        "methodology_en": "Chemiluminescent or immunoradiometric assay (IRMA) on automated immunoassay analyzers; assays are not fully standardized between manufacturers, so results and cutoffs can vary meaningfully by platform.",
        "reference_ranges": [
            {"parameter": "Calcitonin", "population": "Normal", "range": "<10 pg/mL (assay-dependent; some report separate male/female cutoffs)"},
            {"parameter": "Calcitonin", "population": "Suspicious for MTC (per American Thyroid Association)", "range": ">100 pg/mL"},
            {"parameter": "Calcitonin", "population": "Suggests nodal metastases", "range": "~10-40 pg/mL, with tumor present"},
            {"parameter": "Calcitonin", "population": "Suggests distant metastases", "range": ">150 pg/mL, often >1,000 pg/mL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated calcitonin is produced by the parafollicular (C) cells of the thyroid and is a sensitive and fairly specific marker for medullary thyroid carcinoma, with preoperative levels correlating with tumor size, nodal involvement, and distant metastasis. A cutoff around 10 pg/mL gives high sensitivity (~91-96% in various studies) and specificity (~92-99%) for MTC in patients being evaluated for a thyroid nodule, though benign causes of mild elevation exist (C-cell hyperplasia, renal failure, some neuroendocrine tumors, proton pump inhibitor use, and hypergastrinemia). After thyroidectomy for confirmed MTC, calcitonin is used serially to monitor for residual disease or recurrence -- normalization suggests no residual disease outside the thyroid, while a persistently detectable or rising level after surgery suggests residual or recurrent tumor.",
        "associated_conditions": [
            {"condition": "Medullary thyroid carcinoma (diagnosis, staging, and postoperative monitoring)", "direction": "high, correlates with tumor burden"},
            {"condition": "C-cell hyperplasia / benign causes (renal failure, hypergastrinemia, PPI use)", "direction": "mild elevation, non-malignant cause"}
        ],
        "questions_to_ask_en": "Given this level, how likely is it that I have medullary thyroid cancer, and do I need further testing (like a stimulation test or imaging)? If I've already had surgery for MTC, does this result mean I still have residual disease? Should my family be screened for MEN2, given that MTC can be hereditary?",
        "next_steps": "A markedly elevated result in someone with a thyroid nodule typically leads to fine-needle aspiration biopsy (with calcitonin washout testing if needed) and, if MTC is confirmed, genetic testing for RET proto-oncogene mutations, since about 20% of MTC is hereditary (part of MEN2 syndrome) and family screening may be needed. After surgery, persistently elevated or rising calcitonin prompts further imaging to locate residual or recurrent disease.",
        "sources": [
            {"name": "PMC - Current Understanding and Management of Medullary Thyroid Cancer", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3805151/", "accessed": "2026-07-19"},
            {"name": "American Thyroid Association - Calcitonin for Patients (Vol 12 Issue 8)", "url": "https://www.thyroid.org/patient-thyroid-information/ct-for-patients/august-2019/vol-12-issue-8-p-9-10/", "accessed": "2026-07-19"}
        ]
    },
    {
        "slug": "anti-mitochondrial-antibody", "name_en": "Anti-Mitochondrial Antibody (AMA)",
        "aliases": "AMA, Anti-Mitochondrial Antibody",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Serologic hallmark of primary biliary cholangitis (PBC, formerly primary biliary cirrhosis), used to investigate unexplained cholestatic liver enzyme elevation (particularly a disproportionately high alkaline phosphatase), especially in middle-aged women with fatigue or itching.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Usually ordered alongside a full liver panel and, if AMA is negative but suspicion remains high, PBC-specific antinuclear antibodies (anti-sp100, anti-gp210).",
        "methodology_en": "Indirect immunofluorescence assay (IFA) on rodent tissue sections (the traditional reference method) or solid-phase immunoassays (ELISA) targeting the M2 mitochondrial antigen (AMA-M2), which is the clinically relevant subtype in PBC.",
        "reference_ranges": [{"parameter": "AMA", "population": "Result categories", "range": "Negative or Positive (with titer if using immunofluorescence) -- a qualitative/semi-quantitative result, not a single numeric value"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "AMA is detected in approximately 90-95% of patients with primary biliary cholangitis and is uncommon in other conditions, making it highly useful diagnostically -- per current diagnostic criteria, PBC can be diagnosed with a compatible cholestatic liver enzyme pattern (elevated ALP) plus a positive AMA, without requiring liver biopsy in typical cases. Roughly 5-15% of patients with clinical, biochemical, and histologic features of PBC are AMA-negative; in this group, testing for PBC-specific antinuclear antibodies (anti-sp100, anti-gp210) can help confirm the diagnosis, since these are highly specific (though less sensitive) alternatives. AMA-negative PBC appears clinically similar to AMA-positive disease in most respects, though some studies suggest a potentially more severe course.",
        "associated_conditions": [
            {"condition": "Primary biliary cholangitis", "direction": "positive in ~90-95% of cases"},
            {"condition": "AMA-negative PBC (requires anti-sp100/anti-gp210 or biopsy to confirm)", "direction": "negative despite compatible clinical/biochemical/histologic picture"}
        ],
        "questions_to_ask_en": "Does this confirm a diagnosis of PBC, or do I need a liver biopsy as well? If negative but my liver tests still suggest PBC, do I need the additional antibody tests (anti-sp100, anti-gp210)? What treatment is recommended, and how will my response be monitored?",
        "next_steps": "A positive AMA with a compatible cholestatic liver enzyme pattern generally confirms the diagnosis and leads to starting ursodeoxycholic acid (UDCA), the standard first-line treatment, with periodic monitoring of liver tests to assess response. A negative AMA with strong clinical suspicion leads to further antibody testing or liver biopsy before treatment is started.",
        "sources": [
            {"name": "PMC - Antimitochondrial Antibody-Negative Primary Biliary Cholangitis: A Retrospective Diagnosis", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10106268/", "accessed": "2026-07-19"},
            {"name": "PMC - Anti-mitochondrial autoantibodies-milestone or byway to primary biliary cholangitis?", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5326641/", "accessed": "2026-07-19"}
        ]
    },
    {
        "slug": "anti-smooth-muscle-antibody", "name_en": "Anti-Smooth Muscle Antibody (ASMA)",
        "aliases": "ASMA, SMA, Anti-Smooth Muscle Antibody",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Supports the diagnosis of autoimmune hepatitis (particularly type 1), used to investigate unexplained elevated liver enzymes with a hepatocellular (rather than cholestatic) pattern, especially in young to middle-aged women.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Typically ordered alongside ANA, immunoglobulin levels (especially IgG), and a full liver panel as part of the autoimmune hepatitis diagnostic score.",
        "methodology_en": "Indirect immunofluorescence assay on rodent tissue sections, looking for staining of actin filaments in smooth muscle; anti-actin antibody testing (a more specific ELISA-based test for the F-actin target) is sometimes used as a follow-up or alternative.",
        "reference_ranges": [{"parameter": "ASMA", "population": "Result categories", "range": "Negative or Positive (with titer if using immunofluorescence) -- a qualitative/semi-quantitative result"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive ASMA, together with elevated IgG, a hepatocellular pattern of liver enzyme elevation, and compatible histology, supports a diagnosis of type 1 autoimmune hepatitis (the most common form) -- ASMA is often positive alongside or instead of ANA in this condition, and the two are frequently tested together as part of a validated diagnostic scoring system. ASMA is not specific to autoimmune hepatitis alone and can be seen at low titer in other liver diseases and some infections, so it is interpreted alongside the full clinical, biochemical, and (when needed) histologic picture rather than used as a standalone diagnostic test.",
        "associated_conditions": [
            {"condition": "Type 1 autoimmune hepatitis", "direction": "positive, especially at higher titer with elevated IgG"},
            {"condition": "Other liver diseases / infections (lower-titer, less specific finding)", "direction": "positive, low titer, non-diagnostic alone"}
        ],
        "questions_to_ask_en": "Does this, combined with my liver enzyme pattern and IgG level, support autoimmune hepatitis? Do I need a liver biopsy to confirm before starting treatment? What treatment (and how long) is typically needed for this condition?",
        "next_steps": "A positive result with a compatible clinical and biochemical picture typically leads to liver biopsy to confirm the diagnosis and assess severity before starting immunosuppressive treatment (commonly corticosteroids with or without azathioprine), which is usually needed long-term with periodic monitoring of liver enzymes and immunoglobulin levels.",
        "sources": [
            {"name": "Karger - Distinction between Mitochondrial Antibody-Positive and -Negative Primary Biliary Cholangitis (ASMA testing context)", "url": "https://karger.com/crg/article/17/1/14/832394/Distinction-between-Mitochondrial-Antibody", "accessed": "2026-07-19"},
            {"name": "Rare Disease Advisor - Primary Biliary Cholangitis Types (diagnostic criteria referencing ASMA)", "url": "https://www.rarediseaseadvisor.com/hcp-resource/primary-biliary-cholangitis-types/", "accessed": "2026-07-19"}
        ]
    },
    {
        "slug": "vitamin-b6", "name_en": "Vitamin B6 (Pyridoxal 5'-Phosphate, PLP)",
        "aliases": "Vitamin B6, PLP, Pyridoxine",
        "category": "Clinical Chemistry",
        "purpose_en": "Evaluates suspected vitamin B6 deficiency, evaluated in patients with peripheral neuropathy, certain anemias, or seizures (especially pyridoxine-dependent seizures in infants), and used to guide supplementation dosing.",
        "specimen_type": "Venous plasma (EDTA) or serum",
        "collection_notes_en": "Sample should be protected from light and processed/frozen promptly, since PLP degrades at room temperature and with light exposure; low albumin states can also affect the result since PLP binds tightly to albumin.",
        "methodology_en": "High-performance liquid chromatography (HPLC) with fluorescence detection, or HPLC coupled to tandem mass spectrometry.",
        "reference_ranges": [{"parameter": "Plasma PLP", "population": "Normal", "range": "20-200 nmol/L, with adequate status generally defined as >30 nmol/L"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low PLP indicates vitamin B6 deficiency, which can cause peripheral neuropathy, seizures (notably pyridoxine-dependent epilepsy in infants, a rare but treatable cause of neonatal seizures), sideroblastic anemia, and dermatitis; common causes include poor dietary intake, alcohol use disorder, certain medications (isoniazid, some anticonvulsants, penicillamine), and malabsorption. Results can be confounded by low albumin, elevated alkaline phosphatase, inflammation, and pregnancy, all of which can lower plasma PLP independent of true vitamin B6 status -- red cell PLP or functional enzyme activity assays are sometimes used to clarify borderline results in these situations.",
        "associated_conditions": [
            {"condition": "Vitamin B6 deficiency (dietary, alcohol use, malabsorption, certain medications)", "direction": "low"},
            {"condition": "Pyridoxine-dependent seizures (infants)", "direction": "responds to B6 supplementation; PLP level itself may be normal, since the disorder is in PLP-dependent enzyme function"}
        ],
        "questions_to_ask_en": "Could a medication I'm taking (like isoniazid) be causing this deficiency? Do I need supplementation, and for how long? Could my low albumin or another condition be affecting the accuracy of this result?",
        "next_steps": "Confirmed deficiency is treated with oral pyridoxine supplementation, with attention to the underlying cause (medication review, alcohol use, dietary intake) and, in some cases, a repeat level after a period of supplementation to confirm response.",
        "sources": [
            {"name": "droracle.ai - Which laboratory test best assesses pyridoxine (vitamin B6) status (clinical synthesis)", "url": "https://www.droracle.ai/articles/887154/which-laboratory-test-best-assesses-pyridoxine-vitamin-b6-status", "accessed": "2026-07-19"},
            {"name": "Medscape/eMedicine - Vitamin B6: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2088627-overview", "accessed": "2026-07-19"}
        ]
    },
    {
        "slug": "vitamin-a", "name_en": "Vitamin A (Retinol), Serum",
        "aliases": "Vitamin A, Retinol",
        "category": "Clinical Chemistry",
        "purpose_en": "Evaluates suspected vitamin A deficiency (a leading cause of preventable blindness worldwide) or, less commonly, suspected toxicity from excessive supplementation; relevant in malabsorption syndromes, chronic liver disease, and unexplained night blindness or dry eyes.",
        "specimen_type": "Venous serum or plasma, protected from light",
        "collection_notes_en": "Sample should be protected from light and processed promptly, since retinol degrades on light exposure; fasting is generally preferred.",
        "methodology_en": "High-performance liquid chromatography (HPLC).",
        "reference_ranges": [
            {"parameter": "Serum retinol", "population": "Moderate deficiency", "range": "\u226420 mcg/dL (\u22640.70 \u00b5mol/L)"},
            {"parameter": "Serum retinol", "population": "Severe deficiency", "range": "\u226410 mcg/dL (\u22640.35 \u00b5mol/L)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low serum retinol supports vitamin A deficiency, which classically causes night blindness progressing to xerophthalmia and, if untreated, irreversible blindness, along with impaired immune function; common causes in adults include fat malabsorption (celiac disease, cystic fibrosis, chronic pancreatitis, bariatric surgery), chronic liver disease, and severely restricted diets. Serum retinol is tightly homeostatically regulated by the liver until stores are substantially depleted, so a normal level does not fully exclude early or mild deficiency, and it can also be falsely lowered by acute inflammation (as a negative acute-phase reactant) independent of true vitamin A status. Excess vitamin A (from high-dose supplementation) can cause toxicity (headache, bone pain, liver injury, and birth defects if taken in excess during pregnancy), which is a different clinical concern from deficiency and generally requires assessing supplement/dietary intake rather than serum retinol alone, since retinol doesn't rise proportionally with intake once stores are replete.",
        "associated_conditions": [
            {"condition": "Vitamin A deficiency (dietary, malabsorption, chronic liver disease)", "direction": "low"},
            {"condition": "Night blindness / xerophthalmia", "direction": "low, with compatible symptoms"},
            {"condition": "Vitamin A toxicity (excessive supplementation)", "direction": "assessed via intake history more than serum level alone"}
        ],
        "questions_to_ask_en": "Does this level explain my eye or skin symptoms? Do I need supplementation, and at what dose, given the risk of toxicity with excessive intake? Could inflammation or another condition be affecting this result independent of my true vitamin A status?",
        "next_steps": "Confirmed deficiency is treated with vitamin A supplementation at a dose tailored to severity, with monitoring given the narrow margin between adequate replacement and toxicity, and investigation of the underlying cause (malabsorption, liver disease, dietary intake) addressed where possible.",
        "sources": [
            {"name": "NIH Office of Dietary Supplements - Vitamin A and Carotenoids: Health Professional Fact Sheet", "url": "https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/", "accessed": "2026-07-19"}
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
             json.dumps({
                 "calcitonin": ["tsh", "free-t4", "cea"],
                 "anti-mitochondrial-antibody": ["alkaline-phosphatase", "ggt", "alt-ast", "total-bilirubin"],
                 "anti-smooth-muscle-antibody": ["alt-ast", "ana", "alkaline-phosphatase"],
                 "vitamin-b6": ["vitamin-b12", "folate", "homocysteine"],
                 "vitamin-a": ["vitamin-d", "vitamin-k", "zinc"],
             }.get(t["slug"], [])),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
