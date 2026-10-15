"""
Evaluation and benchmark script for NS Live Pulse sentiment models.
Evaluates 52 real transit posts manually labeled (Ground Truth) against:
1. Primary Model: DTAI-KULeuven/robbert-v2-dutch-sentiment
2. Secondary Model: cardiffnlp/twitter-roberta-base-sentiment-latest
3. Baseline: Rule-based Dutch transit keyword lexicon
Computes accuracy, confusion matrix, and exports test_results.csv and test_results.md.
"""

import csv
import json
from src.models import analyze_sentiment, run_lexicon_baseline

TEST_DATA = [
  {"id": "masto_d84be4e26ecb", "text": "STORING: overwegstoring 's-Hertogenbosch - Oss #storing #ns", "ground_truth": "negative"},
  {"id": "masto_83728f4a0532", "text": "Storing voorbij: defecte trein Utrecht - Amersfoort #ns", "ground_truth": "neutral"},
  {"id": "masto_d411eb6322ea", "text": "STORING: defecte trein Utrecht - Amersfoort #storing #ns", "ground_truth": "negative"},
  {"id": "masto_0373bbf644c8", "text": "STORING: overwegstoring Zwolle - Leeuwarden #storing #ns", "ground_truth": "negative"},
  {"id": "masto_ccaca7e1e745", "text": "Storing voorbij: defecte trein Utrecht - Rhenen #ns", "ground_truth": "neutral"},
  {"id": "masto_b0a599235ae7", "text": "Storing voorbij: defecte trein Arnhem - Nijmegen #ns", "ground_truth": "neutral"},
  {"id": "masto_dc73ee5abbc0", "text": "Storing voorbij: defecte trein Nijmegen - 's-Hertogenbosch #ns", "ground_truth": "neutral"},
  {"id": "masto_254c6b2e776e", "text": "STORING: defecte trein Utrecht - Rhenen #storing #ns", "ground_truth": "negative"},
  {"id": "masto_2103f16e0c21", "text": "STORING: defecte trein Arnhem - Nijmegen #storing #ns", "ground_truth": "negative"},
  {"id": "masto_7beeeb7c90ee", "text": "STORING: defecte trein Nijmegen - 's-Hertogenbosch #storing #ns", "ground_truth": "negative"},
  {"id": "masto_94007a0cff7e", "text": "Storing voorbij: defecte trein Arnhem - Nijmegen #ns", "ground_truth": "neutral"},
  {"id": "masto_2fd3d567bf4e", "text": "Storing voorbij: persoon op het spoor Utrecht - Hilversum #ns", "ground_truth": "neutral"},
  {"id": "masto_03b11e985c31", "text": "STORING: defecte trein Nijmegen - 's-Hertogenbosch #storing #ns", "ground_truth": "negative"},
  {"id": "masto_2f3a82500637", "text": "STORING: persoon op het spoor Utrecht - Hilversum #storing #ns", "ground_truth": "negative"},
  {"id": "masto_51df11994b7a", "text": "Storing voorbij: defecte trein Deventer - Enschede; Zwolle - Enschede #ns #nsinternational", "ground_truth": "neutral"},
  {"id": "masto_ab8192bd3602", "text": "klant bij NS, heb je een probleem met je chipkaart bij een servicepunt en dan chat je met de servicedesk, dan vragen ze je tot 4 keer toe wat er mis is. Shit, en dan morgen weer opnieuw proberen.", "ground_truth": "negative"},
  {"id": "masto_4fb5a47fff13", "text": "Storing voorbij: gestrande trein Dordrecht - Roosendaal #ns", "ground_truth": "neutral"},
  {"id": "masto_8dd2fd204103", "text": "STORING: gestrande trein Dordrecht - Roosendaal #storing #ns", "ground_truth": "negative"},
  {"id": "masto_94e99574d077", "text": "STORING: defecte trein Almelo - Hengelo; Zutphen - Hengelo #storing #ns", "ground_truth": "negative"},
  {"id": "masto_518dab44e3cd", "text": "Vertraging - #duitsland, #groningen, #trein, #vertraging", "ground_truth": "negative"},
  {"id": "masto_5e3b44fe2cc7", "text": "Een week geen treinen tussen Rotterdam en Utrecht, lelijk station ook aangepakt", "ground_truth": "negative"},
  {"id": "masto_d72a642c5837", "text": "Storing voorbij: defecte trein Utrecht - Tiel #ns", "ground_truth": "neutral"},
  {"id": "masto_9474d04c204b", "text": "Storing voorbij: defecte trein Utrecht - Gouda; Utrecht - Leiden #ns", "ground_truth": "neutral"},
  {"id": "masto_2af4c2a70d13", "text": "Storing voorbij: defecte trein Haarlem - Alkmaar #ns", "ground_truth": "neutral"},
  {"id": "masto_6046fcc3f496", "text": "STORING: defecte trein Utrecht - Tiel #storing #ns", "ground_truth": "negative"},
  {"id": "masto_742d205521d7", "text": "STORING: defecte trein Utrecht - Gouda; Utrecht - Leiden #storing #ns", "ground_truth": "negative"},
  {"id": "masto_55236f6cdb74", "text": "STORING: defecte trein Haarlem - Alkmaar #storing #ns", "ground_truth": "negative"},
  {"id": "masto_46fb18286290", "text": "Storing voorbij: persoon op het spoor Den Haag - Rotterdam; Leiden - Rotterdam #ns", "ground_truth": "neutral"},
  {"id": "masto_84b010f007a6", "text": "STORING: persoon op het spoor Den Haag - Rotterdam #storing #ns", "ground_truth": "negative"},
  {"id": "masto_fa0a8827f19c", "text": "Goedendag, u heeft contact met de virtuele AI assistent van de meldkamer NS. De melding komt nu pas bij mij binnen.", "ground_truth": "negative"},
  {"id": "masto_2c3ea2a4ac8a", "text": "#treinleven #ns Volle trein, maar mevrouw neemt op deze manier 2 plaatsen. Doet alsof ze niets door heeft, krant lezend.", "ground_truth": "negative"},
  {"id": "masto_6301e018506b", "text": "STORING: defecte trein Eindhoven - Venlo #storing #ns", "ground_truth": "negative"},
  {"id": "masto_1522dbb0d151", "text": "STORING: defecte bovenleiding Rotterdam Centraal #storing #ns", "ground_truth": "negative"},
  {"id": "masto_93be78125146", "text": "Kimberly van 11 is hulp-conducteur in historische trein, wat een prachtig initiatief!", "ground_truth": "positive"},
  {"id": "masto_73e7ab2ee759", "text": "Wat is dat toch voor achterlijke woordkeuze van NS communicatie?!", "ground_truth": "negative"},
  {"id": "masto_c36ba5e513cf", "text": "‘Onbestaanbaar’ en weinig begrip voor mogelijk schrappen van aanpak spoorproblemen", "ground_truth": "negative"},
  {"id": "masto_eed34de70b15", "text": "Reis je dit weekend naar Amsterdam? 🚆 Let dan op: op zaterdag 3 oktober werkzaamheden", "ground_truth": "neutral"},
  {"id": "masto_43a222651ac3", "text": "Geen chauffeurs, te weinig treinen en bussen: provincie trekt lijn in", "ground_truth": "negative"},
  {"id": "masto_477e19791154", "text": "morgen de hele dag geen openbaar vervoer 😟 Ze gaan staken, ik snap de woede maar reizigers zijn de dupe", "ground_truth": "negative"},
  {"id": "masto_463b6da81e5d", "text": "Morgen staken de NS-medewerkers weer. Werk dus een dagje thuis of geniet van de rust", "ground_truth": "neutral"},
  {"id": "masto_97242d2b7189", "text": "NS en Rode Kruis verlengen fijne samenwerking bij grote treinverstoringen voor gestrande reizigers", "ground_truth": "positive"},
  {"id": "masto_4b3a6e552c7b", "text": "Fietsersbond op de bres voor fietsers in de trein: meer fietsparkeerplekken nodig", "ground_truth": "neutral"},
  {"id": "masto_1770640ce84a", "text": "Weinig camerabeelden van sabotageacties op spoor: hier ging het gisteren al mis", "ground_truth": "negative"},
  {"id": "masto_dfa49d79a567", "text": "Premier over storingen op spoor: Ontwrichtende sabotage, volstrekt onacceptabel", "ground_truth": "negative"},
  {"id": "masto_96c238842eae", "text": "Prorail: sabotage op meerdere plekken op het spoor, geen gewonden", "ground_truth": "negative"},
  {"id": "masto_ff8c0fd5fc46", "text": "Grote drukte en chaos op station Meppel door aanhoudende treinstoring en vertraging", "ground_truth": "negative"},
  {"id": "masto_4ceb0e5c7cd9", "text": "Hoe ziek kan iemand zijn: Op meerdere plekken op het spoor zijn materialen gedumpt", "ground_truth": "negative"},
  {"id": "masto_23e86c436759", "text": "ProRail overschrijdt limiet grote spoorstoringen opnieuw, reizigersvereniging eist maatregelen", "ground_truth": "negative"},
  {"id": "masto_8736d96f4d76", "text": "Vakbond luidt opnieuw de noodklok: De maat is vol door toenemend geweld tegen conducteurs", "ground_truth": "negative"},
  {"id": "masto_1a65960bf8a0", "text": "Extra miljarden voor infrastructuur en onderhoud spoornetwerk aangekondigd door minister, goed nieuws!", "ground_truth": "positive"},
  {"id": "reddit_0a79cd06ca1e", "text": "Woensdagse zeurdraad: NS treinen rijden weer eens niet door defecte wissel, sta al 40 min in de kou te wachten", "ground_truth": "negative"},
  {"id": "reddit_734077c6e510", "text": "NS Conducteur hielp oudere dame met zware koffers de trein in bij Utrecht Centraal, top actie en heel vriendelijk!", "ground_truth": "positive"}
]

def run_evaluation():
    print(f"Evaluating {len(TEST_DATA)} manually labeled items against models...")
    
    results = []
    robbert_correct = 0
    roberta_correct = 0
    baseline_correct = 0

    for item in TEST_DATA:
        text = item["text"]
        gt = item["ground_truth"]
        
        # Run inference
        analysis = analyze_sentiment(text, run_secondary=True)
        pred_robbert = analysis["primary_sentiment"]
        pred_roberta = analysis["secondary_sentiment"]
        
        lex_pred, _ = run_lexicon_baseline(text)

        if pred_robbert == gt:
            robbert_correct += 1
        if pred_roberta == gt:
            roberta_correct += 1
        if lex_pred == gt:
            baseline_correct += 1
            
        results.append({
            "id": item["id"],
            "text": text,
            "ground_truth": gt,
            "pred_robbert": pred_robbert,
            "score_robbert": analysis["primary_score"],
            "pred_roberta": pred_roberta,
            "score_roberta": analysis["secondary_score"],
            "pred_lexicon": lex_pred,
            "robbert_match": pred_robbert == gt,
            "roberta_match": pred_roberta == gt
        })

    n = len(TEST_DATA)
    acc_robbert = round((robbert_correct / n) * 100, 1)
    acc_roberta = round((roberta_correct / n) * 100, 1)
    acc_baseline = round((baseline_correct / n) * 100, 1)

    print("\n================ EVALUATION SUMMARY ================")
    print(f"Total Test Items: {n}")
    print(f"Model 1 (RobBERT Dutch Transformer): {robbert_correct}/{n} ({acc_robbert}%)")
    print(f"Model 2 (Cardiff Twitter RoBERTa):   {roberta_correct}/{n} ({acc_roberta}%)")
    print(f"Baseline (Domain Lexicon):           {baseline_correct}/{n} ({acc_baseline}%)")

    # Export to CSV
    csv_file = "data/test_comparison_table.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "text", "ground_truth", "pred_robbert", "score_robbert",
            "pred_roberta", "score_roberta", "pred_lexicon", "robbert_match"
        ])
        writer.writeheader()
        for r in results:
            writer.writerow({
                "id": r["id"],
                "text": r["text"],
                "ground_truth": r["ground_truth"],
                "pred_robbert": r["pred_robbert"],
                "score_robbert": r["score_robbert"],
                "pred_roberta": r["pred_roberta"],
                "score_roberta": r["score_roberta"],
                "pred_lexicon": r["pred_lexicon"],
                "robbert_match": "YES" if r["robbert_match"] else "NO"
            })
    print(f"Exported evaluation table to {csv_file}")

    write_report(results)
    return results


# ---------------------------------------------------------------------------
# Report generation (works on the rows produced above OR on test_comparison_table.csv)
# ---------------------------------------------------------------------------

def _is_alert(text):
    """Machine-generated disruption alerts (e.g. 'STORING: defecte trein ...')."""
    return text.startswith(("STORING", "Storing voorbij"))


def _acc(rows, key):
    hit = sum(1 for r in rows if r[key] == r["ground_truth"])
    return hit, len(rows)


def _fmt(rows, key):
    hit, n = _acc(rows, key)
    return f"{hit}/{n} ({hit / n * 100:.1f}%)" if n else "n/a"


def _example(results, item_id):
    for r in results:
        if r["id"] == item_id:
            return r
    return None


def build_report(results):
    n = len(results)
    non_neutral = [r for r in results if r["ground_truth"] != "neutral"]
    human = [r for r in results if not _is_alert(r["text"])]
    alerts = [r for r in results if _is_alert(r["text"])]
    n_neutral = n - len(non_neutral)
    n_unreachable = sum(1 for r in results if r["ground_truth"] == "neutral")

    lines = []
    w = lines.append
    w("# Model Evaluation & Benchmark Report\n")
    w(f"Test set: **{n} items** from our own stream, labelled by hand (negative / neutral / positive). "
      f"Models: RobBERT (`DTAI-KULeuven/robbert-v2-dutch-sentiment`), Cardiff RoBERTa "
      f"(`cardiffnlp/twitter-roberta-base-sentiment-latest`) and a rule-based Dutch rail word list.\n")

    w("## Accuracy, overall and by subset\n")
    w("| Subset | Items | RobBERT | Cardiff RoBERTa | Word list |")
    w("|:---|:---:|:---:|:---:|:---:|")
    for name, rows in [
        ("All items", results),
        (f"Only items RobBERT *can* get right (label is not neutral)", non_neutral),
        ("Human-written posts (not machine alerts)", human),
        ("Machine-generated alerts (`STORING:` / `Storing voorbij:`)", alerts),
    ]:
        w(f"| {name} | {len(rows)} | {_fmt(rows, 'pred_robbert')} | {_fmt(rows, 'pred_roberta')} | {_fmt(rows, 'pred_lexicon')} |")
    w("")

    w("### How to read these numbers\n")
    w(f"- **RobBERT has only two labels (positive / negative) and can never answer neutral.** "
      f"{n_neutral} of our {n} labels are neutral, so those {n_unreachable} items are guaranteed misses. "
      f"The headline accuracy therefore partly measures our label scheme, not the model. "
      f"On the {len(non_neutral)} items where a correct answer was possible, RobBERT scores {_fmt(non_neutral, 'pred_robbert')}.")
    w(f"- **{len(alerts)} of {n} items are near-identical machine alerts** from one kind of source, so the set is not very varied. "
      f"The human-written posts are the more interesting test: RobBERT {_fmt(human, 'pred_robbert')}, "
      f"word list {_fmt(human, 'pred_lexicon')}, Cardiff {_fmt(human, 'pred_roberta')}.")
    cardiff_neutral = sum(1 for r in results if r["pred_roberta"] == "neutral")
    w(f"- **Cardiff RoBERTa answers neutral for {cardiff_neutral} of {n} items.** It scores on the neutral labels and almost nowhere else "
      f"({_fmt(non_neutral, 'pred_roberta')} on non-neutral items). It is an English model used on Dutch text.")
    w("- **The word list looks strong on the alerts** because words like *storing* and *defect* are in the list, "
      "so it is tuned to exactly this kind of text. It is much weaker on human-written posts, and it only knows words we wrote down.")
    w(f"- Only {sum(1 for r in results if r['ground_truth'] == 'positive')} items are labelled positive, so a difference of one or two items is not meaningful.\n")

    w("## Failure analysis\n")
    w("Why-explanations below are our best reading of the model's behaviour, not something we proved.\n")

    ex = _example(results, "masto_83728f4a0532")
    if ex:
        w("### 1. No neutral class: resolved incidents (systematic)")
        w(f"- **Post**: `{ex['text']}`")
        w(f"- **Human label**: `neutral` (the disruption is over) | **RobBERT**: `{ex['pred_robbert']}` ({ex['score_robbert']})")
        w("- **Why**: RobBERT cannot say neutral, and the words *defecte trein* carry negative meaning. "
          "The resolution marker *voorbij* (over) does not flip it. Every `Storing voorbij` item in the test set is wrong "
          f"({_fmt([r for r in results if r['text'].startswith('Storing voorbij')], 'pred_robbert')} correct).\n")

    ex = _example(results, "masto_d84be4e26ecb")
    if ex:
        alert_neg = [r for r in results if r["text"].startswith("STORING")]
        wrong_pos = [r for r in alert_neg if r["pred_robbert"] == "positive"]
        w("### 2. Factual alerts with no emotional words (systematic, and the dangerous direction)")
        w(f"- **Post**: `{ex['text']}`")
        w(f"- **Human label**: `negative` | **RobBERT**: `{ex['pred_robbert']}` ({ex['score_robbert']})")
        w(f"- **Why**: the model was fine-tuned on book reviews, where sentiment is carried by adjectives. "
          f"A bare alert has none, and compounds such as *overwegstoring* are probably rare in its training text. "
          f"{len(wrong_pos)} of {len(alert_neg)} `STORING` alerts were read as **positive**. "
          "For an early-warning tool, false calm is worse than a false alarm.\n")

    ex = _example(results, "masto_fa0a8827f19c")
    if ex:
        w("### 3. Mixed message: polite surface, implicit complaint")
        w(f"- **Post**: `{ex['text']}`")
        w(f"- **Human label**: `negative` | **RobBERT**: `{ex['pred_robbert']}` ({ex['score_robbert']})")
        w("- **Why**: the post opens with a friendly greeting (*Goedendag*) and contains no complaint word. "
          "The negative part (*pas nu*, only now) is implicit and needs context.\n")

    ex = _example(results, "masto_463b6da81e5d")
    if ex:
        w("### 4. Irony / silver-lining phrasing")
        w(f"- **Post**: `{ex['text']}`")
        w(f"- **Human label**: `neutral` | **RobBERT**: `{ex['pred_robbert']}` ({ex['score_robbert']})")
        w("- **Why**: *geniet van de rust* (enjoy the quiet) reads as clearly positive on its own, "
          "but here it is a light-hearted comment on a strike announcement. The model reads the words, not the situation. "
          "(Our label is also debatable: some readers would call this post negative.)\n")

    ex = _example(results, "masto_518dab44e3cd")
    if ex:
        w("### 5. Jargon and hashtag-only text")
        w(f"- **Post**: `{ex['text']}`")
        w(f"- **Human label**: `negative` | **RobBERT**: `{ex['pred_robbert']}` ({ex['score_robbert']})")
        w("- **Why**: there is no sentence, only a list of hashtags around the word *Vertraging* (delay). "
          "There is almost no context for a model trained on full book reviews.\n")

    w("## Which model would we hand to the user?\n")
    w("See section 7 of the README for the recommendation and its caveats.\n")
    return "\n".join(lines)


def write_report(results, path="data/test_evaluation_report.md"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_report(results))
    print(f"Exported evaluation report to {path}")


def load_results_from_csv(path="data/test_comparison_table.csv"):
    """Rebuild the report from the saved CSV without re-running the models."""
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


if __name__ == "__main__":
    import sys
    if "--report-only" in sys.argv:
        write_report(load_results_from_csv())
    else:
        run_evaluation()
