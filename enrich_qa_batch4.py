"""
Enrichment batch 4: adds questions_to_ask_en + next_steps_en to 20 more
existing Lab Info tests (reproductive hormones, hepatitis/HIV screening,
advanced coagulation, hematology).

Run once: python3 enrich_qa_batch4.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ENRICHMENT = {
    "total-testosterone": {
        "questions": "Was this drawn in the morning, since levels vary through the day? Do I need a repeat test to confirm before any treatment decision? Should free testosterone or SHBG be checked too for a fuller picture?",
        "next_steps": "A low result is typically confirmed with a repeat morning sample before diagnosing hypogonadism, and further testing (LH, FSH) helps determine whether the cause is testicular or related to the pituitary/hypothalamus, which guides treatment options."
    },
    "free-testosterone": {
        "questions": "Does this change the interpretation of my total testosterone result? Could an SHBG abnormality (from weight, thyroid, or other factors) be affecting this? What does this mean for my symptoms and treatment options?",
        "next_steps": "This result is used alongside total testosterone and SHBG to get the clearest picture of your androgen status, particularly when the total testosterone alone doesn't fully explain your symptoms."
    },
    "prolactin": {
        "questions": "Could a medication I'm taking be causing this elevation? Do I need pituitary imaging? If markedly elevated, does this need urgent follow-up?",
        "next_steps": "Mild elevation is often rechecked and reviewed against your medication list and recent activity before the day of the draw. Marked elevation typically prompts pituitary MRI to look for a prolactin-secreting tumor, along with thyroid function testing to rule out that as a contributing cause."
    },
    "semen-analysis": {
        "questions": "Given that results can vary between samples, do I need a repeat test to confirm this finding? Does this explain our fertility difficulties, or do we need more testing? What are our options based on this result?",
        "next_steps": "An abnormal result is usually confirmed with a repeat analysis 4-8 weeks later before drawing conclusions, since sperm parameters vary naturally. Persistently abnormal results typically lead to hormonal testing (testosterone, FSH, LH) and a discussion of fertility treatment options with a specialist."
    },
    "hbsag": {
        "questions": "Does this mean I have an active infection, and is it acute or chronic? Do family members or close contacts need to be tested or vaccinated? What follow-up care do I need?",
        "next_steps": "A reactive result leads to further testing (HBeAg, HBV DNA viral load, liver function tests) to characterize the infection and referral to a specialist for ongoing monitoring and consideration of antiviral treatment if chronic infection is confirmed."
    },
    "hbsab": {
        "questions": "Does this confirm I'm protected against hepatitis B? If my level is below the protective threshold, do I need a booster vaccine? Should this be rechecked periodically given my occupation or health status?",
        "next_steps": "A protective level generally means no further action is needed. A level below the protective threshold after vaccination typically leads to a booster dose, particularly important for healthcare workers or others with ongoing exposure risk."
    },
    "hiv-ag-ab-combo": {
        "questions": "If reactive, what confirmatory testing is being done, and how soon will I know the result? Given the timing of my possible exposure, could this be a false negative from testing too early? What support and next steps are available regardless of the result?",
        "next_steps": "A reactive result is followed by a confirmatory differentiating test and, if needed, HIV RNA testing before a diagnosis is finalized -- your care team will guide you through this process with appropriate counseling and support at every step."
    },
    "fibrinogen": {
        "questions": "Does this level explain any bleeding I've experienced? If low, do I need replacement (like cryoprecipitate) before a procedure? Could this be related to my liver function or an ongoing clotting disorder?",
        "next_steps": "A low level, especially with bleeding or before a planned procedure, often prompts fibrinogen replacement and investigation of the underlying cause (liver disease, DIC, or a rare congenital disorder if there's no other explanation)."
    },
    "antithrombin-iii": {
        "questions": "Does this explain my history of blood clots? Do family members need to be tested? How does this affect my anticoagulation treatment, especially around starting or stopping heparin?",
        "next_steps": "A confirmed deficiency typically leads to hematology referral for guidance on long-term anticoagulation strategy and, since it's often hereditary, consideration of family member testing, particularly if there's a personal or family history of blood clots."
    },
    "protein-c": {
        "questions": "Does this explain my clotting history? If I need to start warfarin, does this affect how that's managed to avoid complications? Should other family members be tested?",
        "next_steps": "A confirmed deficiency is factored into your anticoagulation plan (particularly ensuring heparin bridging if warfarin is started, to avoid warfarin-induced skin necrosis) and often prompts a hematology referral and consideration of family testing."
    },
    "protein-s": {
        "questions": "Could pregnancy, hormone therapy, or another medication be lowering this result rather than a true deficiency? Does this explain my clotting history? Do I need this rechecked at a different time?",
        "next_steps": "Given how many things can lower protein S levels, a low result is often rechecked once you're off relevant medications/hormones and not acutely ill or pregnant, before a hereditary deficiency is diagnosed and long-term management planned."
    },
    "reticulocyte-count": {
        "questions": "Does this suggest my bone marrow is responding appropriately to my anemia, or not producing enough new blood cells? Do I need iron, B12, or folate testing based on this result? How does this fit with my other blood counts?",
        "next_steps": "A low or inappropriately normal result in the setting of anemia typically prompts iron studies, B12, and folate testing to look for a nutritional cause, or further workup for bone marrow function if those are normal."
    },
    "g6pd": {
        "questions": "Given this result, are there specific medications or foods I need to avoid? Should my family members be tested, since this can be hereditary? If this was tested during an acute episode, do I need it repeated later to confirm?",
        "next_steps": "A deficient result leads to counseling about medications and foods (like fava beans) to avoid, and family testing may be recommended given the hereditary nature of this condition. If tested during acute hemolysis, a normal result may need to be repeated weeks later to confirm it wasn't falsely normalized by recent cell turnover."
    },
    "homocysteine": {
        "questions": "Could this be related to a B12 or folate deficiency? Does this affect my cardiovascular risk management? Do I need supplementation, and would that meaningfully reduce my risk?",
        "next_steps": "An elevated level often prompts checking B12 and folate status, since deficiency is a common correctable cause; supplementation may be recommended for nutritional reasons, though it's not typically used specifically to reduce cardiovascular risk given mixed trial evidence."
    },
    "lipoprotein-a": {
        "questions": "Given this is largely genetic, does it change my overall cardiovascular risk management? Do family members need to be tested? Since this doesn't need to be rechecked often, when would repeat testing make sense?",
        "next_steps": "An elevated result is used to refine your overall cardiovascular risk assessment and may prompt more aggressive management of other modifiable risk factors (like LDL cholesterol); since levels are genetically determined, this test is generally only needed once in your lifetime."
    },
    "anti-ccp": {
        "questions": "Does this, combined with my symptoms, support a diagnosis of rheumatoid arthritis? Does my titer level (low vs. high positive) affect my prognosis? Do I need a rheumatology referral?",
        "next_steps": "A positive result in someone with joint symptoms typically supports rheumatoid arthritis and prompts rheumatology referral for further evaluation and early treatment, since earlier treatment is linked to better long-term joint outcomes."
    },
    "complement-c3": {
        "questions": "Does this fit with active lupus or another condition I'm being monitored for? Should this be tracked alongside my other antibody tests? Do I need kidney function testing given this result?",
        "next_steps": "In someone with lupus, a low result alongside rising anti-dsDNA often prompts closer monitoring for a flare, including kidney function and urine testing to check for lupus nephritis."
    },
    "complement-c4": {
        "questions": "Does this fit with active lupus, or could this be a hereditary pattern unrelated to disease activity? If I have recurrent swelling episodes, could this point to hereditary angioedema?",
        "next_steps": "In lupus monitoring, a low result alongside other markers may prompt closer disease activity assessment. In someone with recurrent unexplained swelling, a persistently low C4 supports further workup for hereditary angioedema."
    },
    "anti-dsdna": {
        "questions": "Does this confirm a lupus diagnosis, or is more testing needed? Does a rising titer mean my disease is becoming more active? Do I need kidney testing given this result?",
        "next_steps": "A positive result supports a lupus diagnosis when combined with clinical features, and rising titers (especially with falling complement) often prompt closer monitoring for a flare, including kidney function and urine testing."
    },
    "anca": {
        "questions": "Does this pattern (c-ANCA vs. p-ANCA) point to a specific type of vasculitis? Do I need a biopsy to confirm? Given my symptoms (like kidney or lung involvement), how urgent is further workup?",
        "next_steps": "A positive result with compatible symptoms (unexplained kidney disease, lung involvement, sinus disease) typically prompts urgent rheumatology or nephrology referral, since ANCA-associated vasculitis can progress quickly and benefits from early treatment."
    }
}

def main():
    conn = sqlite3.connect(DB_PATH)
    updated, missing = 0, []
    for slug, data in ENRICHMENT.items():
        row = conn.execute("SELECT id FROM lab_tests WHERE slug = ?", (slug,)).fetchone()
        if not row:
            missing.append(slug)
            continue
        conn.execute(
            "UPDATE lab_tests SET questions_to_ask_en = ?, next_steps_en = ? WHERE slug = ?",
            (data["questions"], data["next_steps"], slug)
        )
        updated += 1
    conn.commit()
    conn.close()
    print(f"Updated: {updated}")
    if missing:
        print(f"Not found in DB (skipped): {missing}")

if __name__ == "__main__":
    main()
