# Model Evaluation & Benchmark Report

Test set: **52 items** from our own stream, labelled by hand (negative / neutral / positive). Models: RobBERT (`DTAI-KULeuven/robbert-v2-dutch-sentiment`), Cardiff RoBERTa (`cardiffnlp/twitter-roberta-base-sentiment-latest`) and a rule-based Dutch rail word list.

## Accuracy, overall and by subset

| Subset | Items | RobBERT | Cardiff RoBERTa | Word list |
|:---|:---:|:---:|:---:|:---:|
| All items | 52 | 31/52 (59.6%) | 18/52 (34.6%) | 25/52 (48.1%) |
| Only items RobBERT *can* get right (label is not neutral) | 37 | 31/37 (83.8%) | 3/37 (8.1%) | 22/37 (59.5%) |
| Human-written posts (not machine alerts) | 24 | 19/24 (79.2%) | 6/24 (25.0%) | 9/24 (37.5%) |
| Machine-generated alerts (`STORING:` / `Storing voorbij:`) | 28 | 12/28 (42.9%) | 12/28 (42.9%) | 16/28 (57.1%) |

### How to read these numbers

- **RobBERT has only two labels (positive / negative) and can never answer neutral.** 15 of our 52 labels are neutral, so those 15 items are guaranteed misses. The headline accuracy therefore partly measures our label scheme, not the model. On the 37 items where a correct answer was possible, RobBERT scores 31/37 (83.8%).
- **28 of 52 items are near-identical machine alerts** from one kind of source, so the set is not very varied. The human-written posts are the more interesting test: RobBERT 19/24 (79.2%), word list 9/24 (37.5%), Cardiff 6/24 (25.0%).
- **Cardiff RoBERTa answers neutral for 49 of 52 items.** It scores on the neutral labels and almost nowhere else (3/37 (8.1%) on non-neutral items). It is an English model used on Dutch text.
- **The word list looks strong on the alerts** because words like *storing* and *defect* are in the list, so it is tuned to exactly this kind of text. It is much weaker on human-written posts, and it only knows words we wrote down.
- Only 4 items are labelled positive, so a difference of one or two items is not meaningful.

## Failure analysis

Why-explanations below are our best reading of the model's behaviour, not something we proved.

### 1. No neutral class: resolved incidents (systematic)
- **Post**: `Storing voorbij: defecte trein Utrecht - Amersfoort #ns`
- **Human label**: `neutral` (the disruption is over) | **RobBERT**: `negative` (0.994)
- **Why**: RobBERT cannot say neutral, and the words *defecte trein* carry negative meaning. The resolution marker *voorbij* (over) does not flip it. Every `Storing voorbij` item in the test set is wrong (0/12 (0.0%) correct).

### 2. Factual alerts with no emotional words (systematic, and the dangerous direction)
- **Post**: `STORING: overwegstoring 's-Hertogenbosch - Oss #storing #ns`
- **Human label**: `negative` | **RobBERT**: `positive` (0.992)
- **Why**: the model was fine-tuned on book reviews, where sentiment is carried by adjectives. A bare alert has none, and compounds such as *overwegstoring* are probably rare in its training text. 4 of 16 `STORING` alerts were read as **positive**. For an early-warning tool, false calm is worse than a false alarm.

### 3. Mixed message: polite surface, implicit complaint
- **Post**: `Goedendag, u heeft contact met de virtuele AI assistent van de meldkamer NS. De melding komt nu pas bij mij binnen.`
- **Human label**: `negative` | **RobBERT**: `positive` (0.785)
- **Why**: the post opens with a friendly greeting (*Goedendag*) and contains no complaint word. The negative part (*pas nu*, only now) is implicit and needs context.

### 4. Irony / silver-lining phrasing
- **Post**: `Morgen staken de NS-medewerkers weer. Werk dus een dagje thuis of geniet van de rust`
- **Human label**: `neutral` | **RobBERT**: `positive` (0.995)
- **Why**: *geniet van de rust* (enjoy the quiet) reads as clearly positive on its own, but here it is a light-hearted comment on a strike announcement. The model reads the words, not the situation. (Our label is also debatable: some readers would call this post negative.)

### 5. Jargon and hashtag-only text
- **Post**: `Vertraging - #duitsland, #groningen, #trein, #vertraging`
- **Human label**: `negative` | **RobBERT**: `positive` (0.889)
- **Why**: there is no sentence, only a list of hashtags around the word *Vertraging* (delay). There is almost no context for a model trained on full book reviews.

## Which model would we hand to the user?

See section 7 of the README for the recommendation and its caveats.
