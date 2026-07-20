"""
Session 4 batch continuing specs_json population. Covers Chrono-log Model
700 Whole Blood/Optical Lumi-Aggregometer (platelet function testing) and
Copan's eSwab collection/transport system and WASPLab microbiology
automation platform.

Run once: python3 populate_specs_session4.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SPECS = {
    50: {  # Chrono-log Model 700 (Analyzer record)
        "Configuration": "2-channel or 4-channel Whole Blood/Optical Lumi-Aggregometer",
        "Detection methods": "Electrical impedance (whole blood) or optical density (plasma), with simultaneous ATP-release luminescence measurement",
        "Test menu": "Platelet aggregation with agonists (collagen, ADP, arachidonic acid, epinephrine, ristocetin, thrombin); Ristocetin Cofactor Assay for von Willebrand disease workup",
        "Sample requirement": "Less than 5 mL of blood per protocol; results in approximately 30 minutes",
        "Software": "AGGRO/LINK 8 software for real-time color display of up to 4 channels of aggregation and ATP release (8 traces total); vW Cofactor software for the ristocetin cofactor assay",
        "Output options": "Strip chart recorder or computer interface",
        "Source": "Chrono-log Corporation official product page (chronolog.com/Model700.html); FDA 510(k) summary K050265",
    },
    93: {  # duplicate Model 700 entry (Platelet aggregometer type)
        "Configuration": "2-channel or 4-channel Whole Blood/Optical Lumi-Aggregometer",
        "Detection methods": "Electrical impedance (whole blood) or optical density (plasma), with simultaneous ATP-release luminescence measurement",
        "Test menu": "Platelet aggregation with agonists (collagen, ADP, arachidonic acid, epinephrine, ristocetin, thrombin); Ristocetin Cofactor Assay for von Willebrand disease workup; Sticky Platelet Syndrome testing via turbidometric feature",
        "Clinical applications": "Monitoring aspirin therapy (collagen-induced aggregation), clopidogrel/Plavix therapy (ADP-induced aggregation), and DDAVP administration (ristocetin-induced aggregation) in whole blood",
        "Electrodes": "Supports both disposable and reusable electrodes for impedance aggregation",
        "Source": "Chrono-log Corporation official product pages (chronolog.com/Model700.html; avant-medical.com/en/products/chrono-log-model-700/); Labmedics distributor technical page",
    },
    145: {  # Copan eSwab / FLOQSwabs
        "System": "Liquid-based specimen collection and transport combining a flocked FLOQSwab with 1 mL of Liquid Amies medium in a screw-cap tube",
        "Organism viability": "Up to 48 hours at room or refrigerated temperature for aerobic, anaerobic, and fastidious bacteria (Neisseria gonorrhoeae viability 24 hours per CLSI standard)",
        "Elution efficiency": "Elutes over 90% of the collected patient specimen into the liquid medium",
        "Regulatory/validation status": "FDA-cleared; validated per CLSI M40-A2 (Quality Control of Microbiological Transport Systems)",
        "Automation compatibility": "Compatible with automated specimen processors and pipettors; validated for molecular and rapid antigen testing on multiple manufacturer platforms",
        "Multi-test capability": "A single ESwab sample can support multiple downstream investigations (culture, molecular, antigen testing)",
        "Source": "Copan (COPAN USA) official eSwab product page (copanusa.com/products/sample-collection-transport-kits/eswab-liquid-based-collection-and-transport/)",
    },
    146: {  # Copan WASP / WASPLab
        "Platform": "WASPLab -- central hub of Copan's Full Laboratory Automation for clinical microbiology (works with front-end WASP specimen processor)",
        "Throughput": "Up to 180 plates loaded/unloaded per hour per incubator",
        "Incubation capacity": "Single or double incubator configurations holding up to 1,590 plates, with O2 or CO2 atmosphere control and a dual-robot loading system",
        "Imaging": "48 MP RGB telecentric trilinear camera, 1,600 pixel/mm resolution, 24-bit color depth, over 1,000 lighting combinations for image optimization across media types",
        "AI integration": "Optional PhenoMATRIX artificial intelligence software to assist culture plate analysis and result sorting (final interpretation performed by qualified laboratory personnel)",
        "Modularity": "Modular, scalable, and customizable configuration; can integrate with Radian (automated AST plate set-up/reading) and Colibri (automated colony picking)",
        "Source": "Copan (COPAN USA) official WASPLab FAQ and brochure pages (copanusa.com/faqs/wasplab-faq/; copanusa.com/laboratory-automation/microbiology-laboratory-automation-ai/wasplab/wasplab-brochure-page/)",
    },
}

def main():
    conn = sqlite3.connect(DB_PATH)
    updated, skipped = 0, 0
    for pid, specs in SPECS.items():
        row = conn.execute("SELECT id, product_name, specs_json FROM products WHERE id = ?", (pid,)).fetchone()
        if not row:
            print(f"SKIP (not found): id={pid}")
            skipped += 1
            continue
        existing_specs = row[2]
        if existing_specs and existing_specs not in ("", "{}", "[]"):
            print(f"SKIP (already has specs_json): id={pid} ({row[1]})")
            skipped += 1
            continue
        conn.execute("UPDATE products SET specs_json = ? WHERE id = ?", (json.dumps(specs), pid))
        print(f"UPDATED: id={pid} ({row[1]})")
        updated += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Updated: {updated}, Skipped: {skipped}")

if __name__ == "__main__":
    main()
