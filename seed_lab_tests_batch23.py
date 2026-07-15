"""
Seed script (batch 23) for MedForsa GCC's Lab Info reference library.
Adds Semen Fructose, Antisperm Antibodies (andrology), and IGF-1.

Run once: python3 seed_lab_tests_batch23.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "semen-fructose", "name_en": "Semen Fructose (Qualitative/Quantitative)",
        "aliases": "Seminal Fructose, Fructose Test (Semen)",
        "category": "Andrology",
        "purpose_en": "Assesses seminal vesicle function and helps establish the cause of azoospermia or very low-volume ejaculate -- fructose is produced by the seminal vesicles, so its presence or absence helps localize an obstruction or developmental absence within the male reproductive tract.",
        "specimen_type": "Semen sample (same collection as a standard semen analysis)",
        "collection_notes_en": "Collected as part of, or as a reflex test from, a semen analysis, particularly when the initial analysis shows azoospermia or low ejaculate volume with low/absent pH.",
        "methodology_en": "Qualitative colorimetric test (resorcinol-based color reaction) for a positive/negative result, or quantitative spectrophotometric measurement when a precise concentration is needed.",
        "reference_ranges": [{"parameter": "Semen fructose", "population": "Normal", "range": "Positive (present); quantitatively often cited as >13 mmol/L in seminal plasma", "notes": "Qualitative testing (positive/negative) is most commonly used clinically; quantitative cutoffs vary by method/lab"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Absent fructose in an azoospermic, low-volume, acidic (low pH) semen sample strongly suggests bilateral congenital absence of the vas deferens (CBAVD), ejaculatory duct obstruction, or seminal vesicle agenesis/hypoplasia -- since the seminal vesicles are the source of seminal fructose, and their secretions are absent when they are missing, obstructed, or not connected to the ejaculate. Normal (present) fructose with azoospermia and normal semen volume/pH instead points toward an obstruction distal to the seminal vesicles or a testicular/spermatogenesis problem (non-obstructive azoospermia) rather than an ejaculatory duct or seminal vesicle problem, helping direct further workup (e.g., transrectal ultrasound, testicular biopsy, or genetic testing for CFTR mutations in suspected CBAVD).",
        "associated_conditions": [
            {"condition": "Congenital bilateral absence of the vas deferens (CBAVD)", "direction": "absent, with azoospermia, low volume, low pH"},
            {"condition": "Ejaculatory duct obstruction / seminal vesicle agenesis", "direction": "absent"},
            {"condition": "Non-obstructive azoospermia (testicular cause)", "direction": "present, with normal volume/pH despite azoospermia"}
        ],
        "questions_to_ask_en": "Given the absence of fructose, does this point to an obstruction or a developmental absence of the seminal vesicles/vas deferens? Do I need genetic testing (e.g., for CFTR mutations) as part of this workup? What imaging or further tests are needed to pinpoint the exact location of the problem? Does this change my options for fertility treatment (e.g., surgical sperm retrieval)?",
        "next_steps": "Absent fructose with azoospermia typically prompts further evaluation with transrectal ultrasound (to assess the seminal vesicles and ejaculatory ducts), CFTR genetic testing if CBAVD is suspected (since it's strongly associated with cystic fibrosis gene mutations), and consultation with a reproductive urologist to discuss surgical sperm retrieval options for fertility treatment, since sperm production in the testes may still be normal even when transport is obstructed.",
        "sources": [
            {"name": "Mayo Clinic Laboratories - Fructose, Qualitative, Semen (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/overview/92187", "accessed": "2026-07-15"},
            {"name": "Male Infertility Guide - Azoospermia and Male Infertility (clinical reference)", "url": "https://www.maleinfertilityguide.com/azoospermia", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "antisperm-antibodies", "name_en": "Antisperm Antibodies (ASA)",
        "aliases": "ASA, Anti-Sperm Antibodies, MAR Test, Immunobead Test",
        "category": "Andrology",
        "purpose_en": "Investigates suspected immunologic male infertility, particularly when semen analysis shows sperm agglutination (clumping) or unexplained reduced motility, and in men with a history of testicular trauma, infection, surgery (including vasectomy reversal), or obstructive azoospermia where the blood-testis barrier may have been breached.",
        "specimen_type": "Semen sample (direct testing, most clinically relevant) or venous serum (indirect testing, for circulating antibodies)",
        "collection_notes_en": "Direct testing on semen (mixed agglutination reaction/MAR test or immunobead test) evaluates antibodies actually bound to the sperm surface and is more clinically informative than indirect serum testing, which only detects circulating antibodies that may not reflect what's happening at the sperm surface.",
        "methodology_en": "Mixed agglutination reaction (MAR) test or direct immunobead binding test, both of which detect IgG or IgA antibodies bound directly to motile sperm.",
        "reference_ranges": [{"parameter": "Antisperm antibodies (direct, % sperm bound)", "population": "Normal", "range": "Generally <10% of motile sperm with bound antibody considered a negative/non-significant result", "notes": "Cutoffs for clinical significance vary by lab and test method; some use a >50% threshold as clearly significant"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A significant percentage of antibody-bound sperm can impair fertility by interfering with sperm motility, cervical mucus penetration, and sperm-egg binding/fusion, contributing to unexplained infertility even when standard semen parameters appear otherwise normal. Roughly 70% of men whose azoospermia is due to a physical obstruction test positive for antisperm antibodies on indirect (blood) testing (since obstruction allows sperm antigens to leak and trigger an immune response), whereas men with non-obstructive azoospermia (a primary production problem) are not expected to have these antibodies -- making indirect ASA testing occasionally useful to help distinguish obstructive from non-obstructive causes of azoospermia in specific clinical scenarios (normal FSH, normal testicular size, no clear cause for obstruction).",
        "associated_conditions": [
            {"condition": "Immunologic male infertility", "direction": "high % antibody-bound sperm, with agglutination on semen analysis"},
            {"condition": "Obstructive azoospermia (supportive indirect finding)", "direction": "positive indirect (serum) ASA in ~70% of cases"},
            {"condition": "Post-vasectomy or vasectomy reversal infertility", "direction": "positive, from breach of the blood-testis barrier"}
        ],
        "questions_to_ask_en": "Given a positive result, how significant is the antibody level for my fertility, and does it explain my infertility findings? What treatment options are available (e.g., sperm washing with IUI, corticosteroids, IVF/ICSI) and which is recommended for my situation? If this followed a vasectomy reversal, does it affect the likelihood of natural conception versus needing assisted reproduction?",
        "next_steps": "A clinically significant result often leads to a discussion of assisted reproductive techniques that can bypass the antibody effect, most reliably intracytoplasmic sperm injection (ICSI) as part of IVF, since it circumvents the natural barriers antibodies interfere with; sperm washing combined with intrauterine insemination (IUI) is sometimes tried first in less severe cases, and corticosteroid therapy is occasionally used though with variable evidence and known side effects.",
        "sources": [
            {"name": "Male Infertility Guide - Antisperm Antibodies (clinical reference)", "url": "https://www.maleinfertilityguide.com/antisperm-antibodies", "accessed": "2026-07-15"},
            {"name": "PMC - Prevalence and impact of antisperm antibodies on semen quality and male reproductive health aspects: A 10-years retrospective study", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3003948/", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "igf-1", "name_en": "Insulin-Like Growth Factor 1 (IGF-1), Serum",
        "aliases": "IGF-1, Somatomedin C",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Primary screening and monitoring test for growth hormone (GH) status -- used to evaluate suspected adult or pediatric GH deficiency, support diagnosis of acromegaly/gigantism (GH excess), and monitor GH replacement therapy or treatment response in acromegaly.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Recent resistance exercise or a high-protein meal can transiently raise levels; acute illness, stress, or prolonged fasting (>24 hours) can transiently lower levels -- ideally tested in a stable, non-acute state.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) on automated immunoassay analyzers, standardized against international reference preparations; results are typically reported alongside an age- and sex-adjusted Z-score, since IGF-1 varies substantially across the lifespan (rising through childhood/puberty, peaking in young adulthood, then steadily declining with age).",
        "reference_ranges": [{"parameter": "IGF-1", "population": "Adult", "range": "Age- and sex-specific reference ranges apply; a Z-score of -2.0 to +2.0 is generally considered normal", "notes": "IGF-1 declines steadily with age -- there is no single adult-wide numeric range; the reporting lab's age/sex-matched reference interval and Z-score should be used"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "IGF-1 reflects average growth hormone secretion over time (unlike GH itself, which is secreted in pulses and is hard to interpret from a single random sample) and is considered the primary screening test for GH axis disorders. A level below the 2.5th percentile (Z-score below -2) for age is consistent with GH deficiency or severe GH resistance, though dynamic GH stimulation testing is often needed for definitive diagnosis, especially when IGF-1 is borderline. Elevated IGF-1 supports a diagnosis of acromegaly (in adults) or gigantism (in children with open growth plates) when combined with compatible clinical findings, and is also used to monitor treatment response in confirmed acromegaly, with a goal of normalizing IGF-1 into the age-adjusted reference range.",
        "associated_conditions": [
            {"condition": "Adult or pediatric growth hormone deficiency", "direction": "low, Z-score below -2"},
            {"condition": "Acromegaly / gigantism (GH excess)", "direction": "high, with compatible clinical findings"},
            {"condition": "Chronic illness, malnutrition, or liver disease (non-GH-axis cause of low IGF-1)", "direction": "low, independent of true GH status"}
        ],
        "questions_to_ask_en": "Given my age and sex, is my result truly abnormal, or within the expected range for someone my age? Do I need dynamic GH stimulation testing to confirm a diagnosis before starting treatment? If I'm on GH replacement therapy, is my current dose achieving the target IGF-1 range? Could a non-hormonal cause (illness, nutrition, liver function) be affecting this result?",
        "next_steps": "A low result consistent with possible GH deficiency typically leads to a GH stimulation test (such as insulin tolerance testing or GHRH-arginine testing) performed under endocrinology supervision to confirm the diagnosis before starting GH replacement therapy. An elevated result suggestive of acromegaly leads to pituitary imaging (MRI) and, often, an oral glucose tolerance test with GH suppression testing to confirm the diagnosis.",
        "sources": [
            {"name": "Mayo Clinic Laboratories - Insulin-Like Growth Factor 1, Serum (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/Overview/623571", "accessed": "2026-07-15"},
            {"name": "PMC - Reference ranges for serum insulin-like growth factor I (IGF-I) in healthy Chinese adults (peer-reviewed age-dependence study)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5627923/", "accessed": "2026-07-15"}
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
        related = ["semen-analysis", "total-testosterone"] if t["slug"] != "igf-1" else ["total-testosterone", "prolactin", "acth"]
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
