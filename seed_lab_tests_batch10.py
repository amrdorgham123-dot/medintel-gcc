"""
Seed script (batch 10) for MedForsa GCC's Lab Info reference library.
Adds reproductive hormones and additional infectious disease screening tests.
English-only content per platform policy.

Run once: python3 seed_lab_tests_batch10.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "lh", "name_en": "Luteinizing Hormone (LH), Serum",
        "aliases": "LH, Lutropin",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Evaluates ovarian/testicular function, menstrual cycle status, ovulation timing, and pituitary-gonadal axis disorders; used in fertility workups, precocious/delayed puberty evaluation, and menopause assessment.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "In women, timing relative to the menstrual cycle is critical for interpretation -- results are meaningless without knowing the cycle day (or menopausal status); a series of daily measurements is sometimes used to detect the ovulatory LH surge.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "LH", "population": "Adult female, follicular phase", "range": "~2-13 mIU/mL", "notes": "Varies by assay and reference population"},
            {"parameter": "LH", "population": "Adult female, ovulatory peak", "range": "~8-73 mIU/mL", "notes": "Wide range reflects the sharp mid-cycle surge; timing of the draw relative to the surge greatly affects the result"},
            {"parameter": "LH", "population": "Adult female, luteal phase", "range": "~1-13 mIU/mL"},
            {"parameter": "LH", "population": "Postmenopausal", "range": "~11-59 mIU/mL", "notes": "Elevated due to loss of negative feedback from declining estrogen"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "High LH with low estradiol/testosterone suggests primary gonadal failure (ovarian or testicular); low or inappropriately normal LH with low sex hormones suggests a hypothalamic/pituitary (secondary) cause. In women, persistently elevated LH relative to FSH (high LH:FSH ratio) is a classic, though not universal, finding in polycystic ovary syndrome. LH is interpreted alongside FSH, estradiol/testosterone, and clinical context (cycle day, menopausal status) rather than in isolation.",
        "associated_conditions": [
            {"condition": "Primary ovarian insufficiency / menopause", "direction": "high"},
            {"condition": "Male primary hypogonadism (testicular failure)", "direction": "high"},
            {"condition": "Hypothalamic/pituitary (secondary) hypogonadism", "direction": "low or inappropriately normal"},
            {"condition": "Polycystic ovary syndrome (PCOS)", "direction": "high LH:FSH ratio, a supportive but not required finding"}
        ],
        "sources": [
            {"name": "Mayo Clinic Laboratories - Luteinizing Hormone (LH), Serum (test catalog)", "url": "https://endocrinology.testcatalog.org/show/LH", "accessed": "2026-07-14"},
            {"name": "ScienceDirect Topics - Follitropin Blood Level, citing commercial immunoassay LH/FSH reference ranges", "url": "https://www.sciencedirect.com/topics/biochemistry-genetics-and-molecular-biology/follitropin-blood-level", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "fsh", "name_en": "Follicle-Stimulating Hormone (FSH), Serum",
        "aliases": "FSH, Follitropin",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Evaluates ovarian reserve, menstrual cycle status, and pituitary-gonadal axis disorders; a key component of fertility workups (day-3 FSH), precocious/delayed puberty evaluation, and menopause assessment.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "In women being evaluated for fertility, FSH is conventionally drawn on cycle day 2-4 (early follicular phase) for the most standardized, interpretable result.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "FSH", "population": "Adult female, reproductive years (cycle-dependent)", "range": "~4.7-21.5 mIU/mL", "notes": "Varies by cycle phase and assay"},
            {"parameter": "FSH", "population": "Postmenopausal", "range": "~25.8-134.8 mIU/mL", "notes": "Elevated due to loss of negative feedback from declining estrogen"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "An elevated day-3 FSH (commonly cited threshold above ~10-12 mIU/mL, though lab-specific) suggests diminished ovarian reserve and is associated with a lower chance of success with fertility treatment including IVF. High FSH with low estradiol confirms primary ovarian insufficiency or menopause. Low or inappropriately normal FSH with low estradiol/testosterone suggests a hypothalamic/pituitary cause. In men, elevated FSH suggests impaired spermatogenesis (primary testicular failure).",
        "associated_conditions": [
            {"condition": "Diminished ovarian reserve", "direction": "high, day-3 FSH"},
            {"condition": "Primary ovarian insufficiency / menopause", "direction": "high"},
            {"condition": "Male primary testicular failure / impaired spermatogenesis", "direction": "high"},
            {"condition": "Hypothalamic/pituitary (secondary) hypogonadism", "direction": "low or inappropriately normal"}
        ],
        "sources": [
            {"name": "Cleveland Clinic - Follicle-Stimulating Hormone (FSH): What It Is & Function", "url": "https://my.clevelandclinic.org/health/articles/24638-follicle-stimulating-hormone-fsh", "accessed": "2026-07-14"},
            {"name": "Mayo Clinic Laboratories - Follicle-Stimulating Hormone (FSH), Serum (test catalog)", "url": "https://endocrinology.testcatalog.org/show/FSH", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "estradiol", "name_en": "Estradiol (E2), Serum",
        "aliases": "E2, Estradiol",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Assesses ovarian function and estrogen status; used in fertility monitoring, menstrual cycle evaluation, precocious puberty workup, and monitoring of assisted reproduction (ovarian stimulation).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "In women, timing relative to the menstrual cycle is essential for interpretation; results are only meaningful when the cycle day (or menopausal/pregnancy status) is known.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA); mass spectrometry (LC-MS/MS) is preferred for low concentrations (children, postmenopausal women, men) where immunoassay specificity is limited.",
        "reference_ranges": [
            {"parameter": "Estradiol", "population": "Adult female, follicular phase (5th-95th percentile)", "range": "~31-90 pg/mL"},
            {"parameter": "Estradiol", "population": "Adult female, ovulatory peak (5th-95th percentile)", "range": "~60-534 pg/mL", "notes": "Wide range reflects the sharp periovulatory rise"},
            {"parameter": "Estradiol", "population": "Adult female, luteal phase (5th-95th percentile)", "range": "~60-233 pg/mL"},
            {"parameter": "Estradiol", "population": "Postmenopausal", "range": "Typically <20 pg/mL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low estradiol with high LH/FSH indicates primary ovarian insufficiency or menopause. Low estradiol with low/inappropriately normal LH/FSH suggests a hypothalamic/pituitary cause (e.g., functional hypothalamic amenorrhea, pituitary disease). Elevated estradiol outside the expected cyclical pattern can suggest an estrogen-producing ovarian or adrenal tumor, or reflect exogenous estrogen exposure. In assisted reproduction, serial estradiol measurements are used to monitor follicular development and response to ovarian stimulation.",
        "associated_conditions": [
            {"condition": "Primary ovarian insufficiency / menopause", "direction": "low, with high LH/FSH"},
            {"condition": "Hypothalamic amenorrhea / pituitary dysfunction", "direction": "low, with low/normal LH/FSH"},
            {"condition": "Estrogen-secreting ovarian or adrenal tumor", "direction": "high, outside expected cyclical pattern"}
        ],
        "sources": [{"name": "PMC - Extensive monitoring of the natural menstrual cycle using serum biomarkers estradiol, LH and progesterone (peer-reviewed multicenter reference study)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8042396/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "progesterone", "name_en": "Progesterone, Serum",
        "aliases": "P4, Progesterone",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Confirms ovulation (mid-luteal progesterone) and evaluates luteal phase function; also used to monitor early pregnancy viability and assess corpus luteum function.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "For confirming ovulation, the sample should be drawn approximately 7 days after the presumed ovulation (mid-luteal phase, e.g., cycle day 21 in a standard 28-day cycle) -- timing relative to ovulation is essential for correct interpretation.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "Progesterone", "population": "Adult female, follicular phase (5th-95th percentile)", "range": "~0.05-0.19 ng/mL"},
            {"parameter": "Progesterone", "population": "Adult female, ovulation (5th-95th percentile)", "range": "~0.06-4.15 ng/mL"},
            {"parameter": "Progesterone", "population": "Adult female, mid-luteal phase (5th-95th percentile)", "range": "~4.1-14.6 ng/mL", "notes": "A mid-luteal level >3 ng/mL is commonly used as presumptive evidence of ovulation, though the exact cutoff varies by lab/reference"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A mid-luteal progesterone consistent with the luteal-phase range supports that ovulation occurred; a low result at the expected mid-luteal timing suggests anovulation or luteal phase defect. In early pregnancy, a low progesterone can be associated with (though does not definitively diagnose) an abnormal or non-viable pregnancy, and is sometimes used alongside serial beta-hCG and ultrasound in the evaluation of suspected miscarriage or ectopic pregnancy, though its diagnostic role here is debated and varies by clinical protocol.",
        "associated_conditions": [
            {"condition": "Anovulation / luteal phase defect", "direction": "low at expected mid-luteal timing"},
            {"condition": "Confirmed ovulation", "direction": "appropriately elevated mid-luteal level"},
            {"condition": "Possible non-viable early pregnancy (adjunct marker)", "direction": "low, interpreted alongside beta-hCG and ultrasound"}
        ],
        "sources": [{"name": "PMC - Extensive monitoring of the natural menstrual cycle using serum biomarkers estradiol, LH and progesterone (peer-reviewed multicenter reference study)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8042396/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "anti-hcv", "name_en": "Hepatitis C Virus Antibody (Anti-HCV)",
        "aliases": "Anti-HCV, HCV Antibody, Hepatitis C Screen",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Screening test for current or past hepatitis C virus (HCV) infection; used for routine adult screening (per current CDC one-time screening recommendations), blood donor screening, and evaluation of unexplained liver enzyme elevation.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. A reactive result requires reflex/confirmatory HCV RNA testing to distinguish current (active) infection from a resolved past infection, since antibodies persist for life even after the virus has cleared (spontaneously or with treatment).",
        "methodology_en": "Chemiluminescent immunoassay (CIA) or enzyme immunoassay (EIA); reactive screening results are typically reflexed to HCV RNA (viral load) testing by the laboratory.",
        "reference_ranges": [{"parameter": "Anti-HCV", "population": "Result categories", "range": "Non-reactive (negative) or Reactive (positive) -- reported by signal-to-cutoff ratio, not a numeric concentration"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A reactive anti-HCV antibody result indicates exposure to HCV at some point but does not confirm current infection -- a positive antibody with a negative/undetectable HCV RNA indicates a resolved past infection (either spontaneous clearance or successful prior treatment), while a positive antibody with detectable HCV RNA confirms current active infection requiring evaluation for antiviral treatment. In immunocompromised patients or those tested very early after exposure (acute infection), antibody testing can be falsely negative, and direct HCV RNA testing may be needed if suspicion is high.",
        "associated_conditions": [
            {"condition": "Current (active) hepatitis C infection", "direction": "reactive antibody + detectable HCV RNA"},
            {"condition": "Resolved past hepatitis C infection", "direction": "reactive antibody + undetectable HCV RNA"},
            {"condition": "Chronic hepatitis C (cirrhosis/hepatocellular carcinoma risk if untreated)", "direction": "reactive antibody + persistently detectable HCV RNA"}
        ],
        "sources": [{"name": "Mayo Clinic Laboratories - Hepatitis C Virus Antibody Confirmation, Serum (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/overview/63063", "accessed": "2026-07-14"}]
    },
    {
        "slug": "syphilis-screening", "name_en": "Syphilis Screening (RPR/VDRL with Treponemal Confirmation)",
        "aliases": "RPR, VDRL, TPHA, TPPA, FTA-ABS, Syphilis Serology",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Screens for syphilis infection; used in routine prenatal screening, STI evaluation, and blood donor screening. Two complementary test types are used together: non-treponemal tests (RPR/VDRL) for screening and activity/treatment monitoring, and treponemal tests (TPHA/TPPA/FTA-ABS or treponemal EIA/CIA) for confirmation.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Testing algorithms vary by laboratory: the 'traditional' algorithm screens with a non-treponemal test (RPR/VDRL) and confirms reactive results with a treponemal test, while the 'reverse' algorithm (increasingly common) screens with a treponemal EIA/CIA first and confirms with RPR/VDRL, which changes how discordant results are interpreted.",
        "methodology_en": "Non-treponemal tests (RPR, VDRL) detect antibodies to cardiolipin-lecithin-cholesterol antigen released from damaged host cells and are reported as reactive/non-reactive with a titer; treponemal tests (TPHA, TPPA, FTA-ABS, or automated treponemal EIA/CIA) detect antibodies specific to Treponema pallidum antigens.",
        "reference_ranges": [{"parameter": "RPR/VDRL and treponemal test", "population": "Result categories", "range": "Non-reactive or Reactive (with titer for RPR/VDRL) -- interpretation depends on the pattern of both test types together, not either alone"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A reactive non-treponemal test (RPR/VDRL) confirmed by a reactive treponemal test supports active or previously treated syphilis (the treponemal test typically remains reactive for life even after successful treatment, so it cannot distinguish current from past treated infection on its own). A reactive RPR/VDRL with a non-reactive treponemal test suggests a biologic false-positive, which can occur with other conditions including pregnancy, autoimmune disease, and other infections such as chronic hepatitis C. Declining RPR/VDRL titers after treatment indicate treatment response; a sustained fourfold titer rise suggests reinfection or treatment failure.",
        "associated_conditions": [
            {"condition": "Active or previously treated syphilis", "direction": "reactive non-treponemal + reactive treponemal test"},
            {"condition": "Biologic false-positive (pregnancy, autoimmune disease, other infections)", "direction": "reactive non-treponemal + non-reactive treponemal test"},
            {"condition": "Treatment response monitoring", "direction": "declining RPR/VDRL titer over time"}
        ],
        "sources": [
            {"name": "CDC NHANES Laboratory Procedure Manual - Syphilis (RPR methodology)", "url": "https://wwwn.cdc.gov/nchs/data/nhanes/public/2003/labmethods/l36_c_met_rpr.pdf", "accessed": "2026-07-14"},
            {"name": "ScienceDirect - Hepatitis C virus infection and biological false-positive syphilis test (RPR/TPHA discordance context)", "url": "https://www.sciencedirect.com/science/article/abs/pii/S1499387211600672", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "rubella-igg", "name_en": "Rubella IgG (Immunity Status)",
        "aliases": "Rubella Antibody, German Measles Immunity",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Determines immune status to rubella (German measles), most commonly as part of prenatal/preconception screening, since maternal rubella infection in early pregnancy can cause congenital rubella syndrome with serious fetal malformations.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Part of standard prenatal panels; a non-immune result in a pregnant woman prompts postpartum vaccination (rubella vaccine is a live vaccine and cannot be given during pregnancy).",
        "methodology_en": "Chemiluminescent or enzyme immunoassay, calibrated against the WHO International Standard (RUBI-1-94) and reported in IU/mL.",
        "reference_ranges": [{"parameter": "Rubella IgG", "population": "Seropositive (immune)", "range": "\u226510 IU/mL (conventional WHO-standardized cutoff)", "notes": "Assay calibration and cutoffs vary between manufacturers; results near the cutoff (equivocal) may need confirmatory testing, particularly in vaccinated (versus naturally infected) individuals"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive (seropositive) result indicates immunity, either from prior vaccination or past natural infection, and no specific action is needed. A negative (non-immune) result in a woman of reproductive age, especially when planning pregnancy, prompts vaccination before conception or postpartum (since the vaccine cannot be given during pregnancy). If a pregnant woman has a suspected rubella exposure or rash illness, IgG and IgM testing together (with attention to timing and possible paired acute/convalescent samples) helps determine whether an acute infection is occurring.",
        "associated_conditions": [
            {"condition": "Rubella immunity (from vaccination or past infection)", "direction": "positive/seropositive"},
            {"condition": "Susceptibility to rubella infection", "direction": "negative -- prompts vaccination when not pregnant"},
            {"condition": "Congenital rubella syndrome risk (if maternal infection occurs in pregnancy)", "direction": "relevant when a pregnant patient is non-immune and exposed"}
        ],
        "sources": [{"name": "PMC - Evaluation of Commercial Immunoassays for Rubella Virus IgG Detection (WHO standard cutoff)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12844522/", "accessed": "2026-07-14"}]
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
