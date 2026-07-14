"""
Seed script (batch 5) for MedForsa GCC's Lab Info reference library.
Adds reproductive hormones, semen analysis (WHO 2021), and infectious disease
screening serology. English-only content per platform policy.

Run once: python3 seed_lab_tests_batch5.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "total-testosterone", "name_en": "Testosterone, Total, Serum",
        "aliases": "Total Testosterone, T",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Evaluates androgen status; used to investigate hypogonadism, erectile dysfunction, and low libido in men, and hirsutism/virilization or suspected androgen-secreting tumors in women.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Morning sample (before 10 AM) strongly preferred in men, as testosterone follows a diurnal pattern and peaks in the early morning.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) for routine screening; LC-MS/MS is the preferred, more specific method at low concentrations (e.g., in women, children, and hypogonadal men) per current endocrine guidelines.",
        "reference_ranges": [
            {"parameter": "Total testosterone", "population": "Adult male (\u226519 years)", "range": "240-950 ng/dL"},
            {"parameter": "Total testosterone", "population": "Adult female (\u226519 years)", "range": "8-60 ng/dL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low testosterone in men (with compatible symptoms, confirmed on a repeat morning sample) supports a diagnosis of hypogonadism; LH/FSH levels help distinguish primary (testicular) from secondary (pituitary/hypothalamic) causes. Elevated testosterone in women can suggest PCOS (usually mild elevation) or, when total testosterone exceeds roughly 150-200 ng/dL, raises concern for an androgen-secreting ovarian or adrenal tumor requiring further workup.",
        "associated_conditions": [
            {"condition": "Male hypogonadism (primary or secondary)", "direction": "low, in men"},
            {"condition": "Polycystic ovary syndrome (PCOS)", "direction": "mildly high, in women"},
            {"condition": "Androgen-secreting ovarian/adrenal tumor", "direction": "markedly high, in women"}
        ],
        "sources": [{"name": "Mayo Clinic Laboratories - Testosterone, Total and Bioavailable, Serum (test catalog)", "url": "https://endocrinology.testcatalog.org/show/TTBS", "accessed": "2026-07-14"}]
    },
    {
        "slug": "free-testosterone", "name_en": "Testosterone, Free, Serum",
        "aliases": "Free Testosterone",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Measures the biologically active, unbound fraction of testosterone; useful when total testosterone is borderline or when sex hormone-binding globulin (SHBG) is abnormal (e.g., obesity, thyroid disease, aging), which can distort the total testosterone result.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Morning sample preferred, same rationale as total testosterone.",
        "methodology_en": "Equilibrium dialysis (reference method) or calculated from total testosterone, SHBG, and albumin; direct immunoassay methods for free testosterone are less reliable and generally discouraged by endocrine societies.",
        "reference_ranges": [
            {"parameter": "Free testosterone", "population": "Adult male", "range": "9-30 ng/dL"},
            {"parameter": "Free testosterone", "population": "Adult female", "range": "0.3-1.9 ng/dL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Free testosterone is most useful when total testosterone is equivocal but SHBG is abnormal -- for example, a normal total testosterone with low free testosterone can occur when SHBG is elevated, masking true androgen deficiency. Interpretation should follow the same clinical framework as total testosterone (hypogonadism workup in men, hyperandrogenism workup in women).",
        "associated_conditions": [
            {"condition": "Male hypogonadism masked by abnormal SHBG on total testosterone alone", "direction": "low"},
            {"condition": "Hyperandrogenism (PCOS and related conditions)", "direction": "high, in women"}
        ],
        "sources": [{"name": "USPTO patent literature citing Mayo Clinic 2013 reference ranges for testosterone (free and total)", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9482678", "accessed": "2026-07-14"}]
    },
    {
        "slug": "prolactin", "name_en": "Prolactin, Serum",
        "aliases": "PRL",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Evaluates suspected hyperprolactinemia (galactorrhea, menstrual irregularity, infertility, erectile dysfunction/low libido) and helps investigate suspected pituitary adenoma (prolactinoma).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Draw when the patient is relaxed and fasting is not required; avoid recent breast exam, sexual activity, or significant stress/exercise before the draw, as these can transiently raise prolactin. Consider repeating an elevated result before extensive workup, as prolactin secretion is pulsatile and stress-sensitive.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "Prolactin", "population": "Adult male", "range": "<20 ng/mL", "notes": "Upper limit varies by lab/assay, commonly cited as 15-25 ng/mL"},
            {"parameter": "Prolactin", "population": "Adult female, non-pregnant", "range": "<25 ng/mL", "notes": "Upper limit varies by lab/assay"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Mild-to-moderate elevation is commonly caused by medications (antipsychotics, some antiemetics/antidepressants), hypothyroidism, renal failure, or physiologic causes (pregnancy, stress, nipple stimulation). Marked elevation (often >200 ng/mL) is more specific for a prolactin-secreting pituitary adenoma (prolactinoma) and warrants pituitary imaging. High prolactin suppresses GnRH, causing low LH/FSH and secondary hypogonadism -- explaining menstrual irregularity in women and low testosterone/libido in men. Low prolactin is less commonly clinically significant.",
        "associated_conditions": [
            {"condition": "Medication-induced hyperprolactinemia (antipsychotics, etc.)", "direction": "mild-moderate high"},
            {"condition": "Prolactinoma (pituitary adenoma)", "direction": "markedly high, often >200 ng/mL"},
            {"condition": "Primary hypothyroidism", "direction": "mild high (via elevated TRH)"},
            {"condition": "Secondary hypogonadism from prolactin excess", "direction": "high prolactin with low LH/FSH/testosterone or estradiol"}
        ],
        "sources": [{"name": "Jinfiniti Precision Medicine - Prolactin Blood Test Levels, citing Canadian Medical Association primary care guidance", "url": "https://www.jinfiniti.com/prolactin-blood-test-levels/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "semen-analysis", "name_en": "Semen Analysis (WHO 2021)",
        "aliases": "Sperm Analysis, Spermiogram, Sperm Count",
        "category": "Andrology",
        "purpose_en": "Evaluates male fertility potential by assessing semen volume, sperm concentration, motility, and morphology; a core component of the infertility workup for couples, and used to confirm sterility after vasectomy.",
        "specimen_type": "Semen sample, collected by masturbation into a sterile container after 2-7 days of sexual abstinence (per WHO recommendation)",
        "collection_notes_en": "Sample should reach the laboratory and be analyzed within 1 hour of collection, kept close to body temperature during transport. Because sperm parameters vary significantly between ejaculates and spermatogenesis takes about 72 days, a single abnormal result should be confirmed with a repeat analysis 4-8 weeks later before drawing conclusions.",
        "methodology_en": "Manual microscopic assessment (hemocytometer counting chamber for concentration, motility and morphology graded per WHO criteria) or computer-assisted sperm analysis (CASA) systems.",
        "reference_ranges": [
            {"parameter": "Semen volume", "population": "WHO 2021 lower reference limit (5th centile)", "range": "\u22651.4 mL"},
            {"parameter": "Sperm concentration", "population": "WHO 2021 lower reference limit", "range": "\u226516 million/mL"},
            {"parameter": "Total motility", "population": "WHO 2021 lower reference limit", "range": "\u226542%"},
            {"parameter": "Progressive motility", "population": "WHO 2021 lower reference limit", "range": "\u226530%"},
            {"parameter": "Normal morphology (strict criteria)", "population": "WHO 2021 lower reference limit", "range": "\u22654%"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "WHO 2021 lower reference limits represent the 5th percentile of semen parameters from a large cohort of fertile men whose partners conceived naturally within 12 months -- they are a statistical benchmark, not a strict pass/fail cutoff, and a single below-threshold result does not by itself diagnose infertility. Common patterns include oligozoospermia (low concentration), asthenozoospermia (reduced motility), teratozoospermia (abnormal morphology), or azoospermia (no sperm seen), which require correlation with hormonal workup (FSH, LH, testosterone) and clinical evaluation. Results are compared against the specific WHO edition used by the reporting laboratory, since thresholds have changed across the 1999, 2010, and 2021 editions.",
        "associated_conditions": [
            {"condition": "Male factor infertility (oligo-/astheno-/teratozoospermia)", "direction": "below WHO lower reference limit(s)"},
            {"condition": "Obstructive or non-obstructive azoospermia", "direction": "no sperm observed"},
            {"condition": "Post-vasectomy sterility confirmation", "direction": "azoospermia expected post-procedure"}
        ],
        "sources": [
            {"name": "Boeri et al., Andrology (Wiley) - The impact of different WHO reference criteria for semen analysis in clinical practice (WHO 1999/2010/2021 comparison table)", "url": "https://onlinelibrary.wiley.com/doi/10.1111/andr.13213", "accessed": "2026-07-14"},
            {"name": "PMC - Trends in sperm quality by computer-assisted sperm analysis (WHO 5th edition/2021 reference values)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10390301/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "hbsag", "name_en": "Hepatitis B Surface Antigen (HBsAg)",
        "aliases": "HBsAg, Hepatitis B Surface Antigen",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Primary screening test for current hepatitis B virus (HBV) infection (acute or chronic); required for blood/organ donor screening, prenatal screening, and routine adult HBV screening per CDC recommendations.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Chemiluminescent microparticle immunoassay (CMIA) or similar automated immunoassay; reactive (positive) results are typically confirmed by a neutralization assay before being reported as confirmed-positive, and may reflex to quantitative HBV DNA PCR.",
        "reference_ranges": [{"parameter": "HBsAg", "population": "Result categories", "range": "Non-reactive (negative) or Reactive (positive) -- reported by signal-to-cutoff ratio, not a numeric concentration"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A reactive HBsAg indicates the person is currently infected with hepatitis B (acute or chronic) and is potentially infectious. Persistence of HBsAg beyond 6 months defines chronic HBV infection, which requires further evaluation (HBeAg, HBV DNA viral load, liver function) and specialist referral for possible antiviral therapy. HBsAg is one of three tests (with anti-HBc and anti-HBs) used together to fully characterize a person's HBV status (never infected, actively infected, resolved infection/immune, or vaccinated/immune).",
        "associated_conditions": [
            {"condition": "Acute hepatitis B infection", "direction": "reactive, with symptoms/elevated ALT"},
            {"condition": "Chronic hepatitis B infection", "direction": "reactive, persisting beyond 6 months"}
        ],
        "sources": [{"name": "UW Medicine - Hepatitis B Surface Antigen (HBsAg) with reflex to PCR, Laboratory Test Guide", "url": "https://dlmp.uw.edu/test-guide/view/HBSAG", "accessed": "2026-07-14"}]
    },
    {
        "slug": "hbsab", "name_en": "Hepatitis B Surface Antibody (Anti-HBs)",
        "aliases": "HBsAb, Anti-HBs, Hepatitis B Surface Antibody",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Determines immunity to hepatitis B, either from prior vaccination or from resolved past infection; used to confirm post-vaccination immune response, especially in healthcare workers.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. If checking post-vaccination response, timing is typically 1-2 months after completing the vaccine series.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA); available as qualitative (reactive/non-reactive) or quantitative (mIU/mL) testing.",
        "reference_ranges": [
            {"parameter": "Anti-HBs (qualitative)", "population": "Result categories", "range": "Reactive (immune) or Non-reactive (not immune)"},
            {"parameter": "Anti-HBs (quantitative)", "population": "Protective threshold", "range": "\u226510 mIU/mL considered protective"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A reactive anti-HBs with a non-reactive HBsAg and non-reactive anti-HBc indicates vaccine-induced immunity. A reactive anti-HBs together with reactive anti-HBc indicates immunity from a past, resolved natural infection. A quantitative titer below 10 mIU/mL after vaccination suggests an inadequate response, and revaccination may be recommended, particularly in healthcare workers or immunocompromised patients.",
        "associated_conditions": [
            {"condition": "Vaccine-induced immunity", "direction": "reactive anti-HBs, non-reactive anti-HBc"},
            {"condition": "Immunity from resolved past infection", "direction": "reactive anti-HBs, reactive anti-HBc"},
            {"condition": "Inadequate vaccine response", "direction": "quantitative titer <10 mIU/mL post-vaccination"}
        ],
        "sources": [{"name": "HealthMatters.io - Hepatitis B Surface Antibody (Qual): Reactive and Non-Reactive Results", "url": "https://healthmatters.io/understand-blood-test-results/hep-b-surface-ab-qual", "accessed": "2026-07-14"}]
    },
    {
        "slug": "hiv-ag-ab-combo", "name_en": "HIV Antigen/Antibody Combination Screen",
        "aliases": "HIV Combo, HIV Ag/Ab, 4th Generation HIV Test, HIV p24/Antibody Screen",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Fourth-generation screening test for HIV-1 and HIV-2 infection, detecting both the HIV-1 p24 antigen (present early in acute infection, before antibodies develop) and antibodies to HIV-1/HIV-2; recommended as the standard initial screening assay by current testing algorithms.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Antibodies are not reliably detectable until roughly 3 weeks after exposure, so a very recent (acute) exposure may still test negative even with the more sensitive combo assay.",
        "methodology_en": "Chemiluminescent immunoassay (CMIA) detecting both p24 antigen and HIV-1/2 antibodies simultaneously; reactive (positive) results are confirmed with an HIV-1/HIV-2 antibody-differentiating immunoassay, with reflex to HIV-1 RNA nucleic acid testing (NAT) when the differentiating assay is negative or indeterminate.",
        "reference_ranges": [{"parameter": "HIV Ag/Ab Combo", "population": "Result categories", "range": "Non-reactive (negative) or Reactive (positive, requires confirmatory testing) -- reported by signal-to-cutoff ratio"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A non-reactive result on the initial screen generally means no HIV infection, without need for further confirmatory antibody-differentiating testing, when outside the window period. A reactive screening result with a non-reactive or indeterminate differentiating assay may indicate very recent (acute) HIV infection and requires HIV-1 RNA testing to clarify. A reactive screen confirmed by a reactive differentiating assay establishes the diagnosis and identifies HIV-1 versus HIV-2.",
        "associated_conditions": [
            {"condition": "Acute HIV infection (early window period)", "direction": "reactive combo screen, non-reactive/indeterminate differentiating assay -- needs RNA testing"},
            {"condition": "Established HIV-1 or HIV-2 infection", "direction": "reactive screen confirmed by reactive differentiating assay"}
        ],
        "sources": [
            {"name": "UW Medicine - HIV Antigen and Antibody Screen, Laboratory Test Guide", "url": "https://dlmp.uw.edu/test-guide/view/HVAGAB", "accessed": "2026-07-14"},
            {"name": "Virginia Dept. of Health - Current HIV Testing Guidelines and Additional Considerations", "url": "https://www.vdh.virginia.gov/content/uploads/sites/10/2021/02/Provider_Messaging_2019_Final.pdf", "accessed": "2026-07-14"}
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
