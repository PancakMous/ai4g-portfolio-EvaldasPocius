# NS Rail Live Pulse: Passenger Sentiment Radar 🚆
### The link to the site
https://pancakmous.github.io/ai4g-portfolio-EvaldasPocius/

### Autonomous Stream Intelligence for Dutch Rail Infrastructure (SDG 9)

**Live Pulse** is an autonomous sentiment monitoring system designed for Dutch public railway infrastructure (Nederlandse Spoorwegen - NS and ProRail). It continuously ingests real-time commuter reactions and incident announcements from live social and transit data streams, analyzes the sentiment of each item using a local pre-trained Dutch transformer (**RobBERT**), stores the results in a persistent time-series database, and visualizes passenger mood shifts on an interactive dashboard tailored for transit operational decision-makers.

---

## 1. Target Persona & Operational Decision
- **Named Persona (fictional)**: **Maaike van Dijk**, Lead Incident Response & Passenger Experience Manager at NS Customer Operations Desk. She is an invented persona representing this kind of operations role.
- **The Problem Today**: Rail disruptions are frequent and costly for passengers. ProRail registered 586 high-impact disruptions in 2025, above the maximum of 520 it had agreed with the ministry (507 in 2024), and received a fine of EUR 2.75 million (source: [NOS](https://nos.nl/l/2615469)). Passengers react to disruptions online, but those reactions are spread over many posts and hard to follow as one signal. We assume this could give operations an extra early signal; **we have not measured** how much earlier social posts appear than press coverage, so we do not claim a lead time.
- **The Operational Decision**: 
  - When the **Live Pulse Net Sentiment** drops below **-30.0** (or negative disruption posts spike on a specific corridor like *Utrecht–Amsterdam* or *Rotterdam–Eindhoven*), Maaike immediately:
    1. Triggers proactive push notifications in the NS App explaining the delay cause and rerouting advice.
    2. Dispatches mobile platform service guides and crowd-control assistance to bottleneck stations.
    3. Mobilizes replacement bus operators and delay-compensation vouchers before passenger anger peaks.

---

## 2. SDG 9 Relevance (Industry, Innovation & Infrastructure)
Public rail transport forms the backbone of sustainable national mobility and low-carbon infrastructure. Maintaining high reliability, rapid incident response, and passenger trust directly supports:
- **Target 9.1**: Develop quality, reliable, sustainable, and resilient infrastructure.
- **Target 9.4**: Upgrade infrastructure and retrofit industries to make them sustainable, with increased resource-use efficiency.

---

## 3. Data Streams & Terms of Use
The tool ingests continuously from live, public feeds:
1. **Mastodon & Fediverse Transit Stream**: Public timeline hashtag endpoints (`#ns`, `#trein`, `#prorail`, `#vertraging`, `#storing`, `#station`, `#spoorwegen`) from `mastodon.nl` and `social.overheid.nl`.
2. **Reddit Rail Stream**: Public RSS feeds from `r/thenetherlands` and `r/netherlands` filtered for rail keywords (`NS`, `trein`, `spoor`, `station`, `conducteur`, `vertraging`).

### Terms of Use Confirmation

| Source | API Key Required? | Terms Allow This? |
|:---|:---|:---|
| **Mastodon** | No — public ActivityPub endpoints | ✅ Yes — public timelines are openly accessible per ActivityPub protocol; non-commercial read-only use permitted |
| **Reddit RSS** | No — public RSS feeds | ✅ Yes — Reddit's Terms of Service permit non-commercial automated RSS consumption; no scraping of private data |

### Privacy & Data Protection Compliance:
- **Pseudonymised, not fully anonymous**: usernames, display names, avatars and account IDs are not stored. However, each post keeps a `url` that links to the original post, and on Mastodon that link contains the author's public handle (for example `mastodon.nl/@handle/...`). The data is therefore pseudonymised, not fully anonymous.
- **Data Minimization**: The pipeline stores the sanitized post text, a post ID, the source name, the post's creation time and our fetch time (UTC), the post `url`, a detected language tag, and the sentiment labels and scores. Nothing else.

---

## 4. Pre-trained Hugging Face Transformer

### Primary Model: RobBERT Dutch Sentiment
- **Model Identifier**: `DTAI-KULeuven/robbert-v2-dutch-sentiment` (RoBERTa architecture, Dutch).
- **Why this model**: Dutch railway discourse contains compound words (*wisselstoring*, *vertraging*, *bovenleiding*) and Dutch sentence structure that English-only models handle badly.
- **Local Execution**: Loaded and run by our own code (`src/models.py`) through the Hugging Face `transformers` pipeline (PyTorch backend). We did **not** fine-tune it.

- **Details from the model card**:
  - Licence: MIT.
  - Fine-tuning data: the Dutch Book Reviews Dataset (DBRD), reviews from Hebban.nl. Roughly 19,500 reviews were used for training, 528 for validation and 2,224 for the final accuracy test.
  - Limitation: the model is trained on book reviews, so it may work worse on other kinds of text, such as short social posts and service alerts.
  - Labels: in every prediction we ran (the stored posts and the 52 test items) the model returned only `positive` or `negative`, never `neutral`.

#### Model Card Summary

| Detail | Value |
|:---|:---|
| **Trained on** | Two steps. (1) The base model, RobBERT v2, was pre-trained on the Dutch section of the OSCAR web-text corpus (about 39 GB). (2) The sentiment version was then fine-tuned on the **Dutch Book Reviews Dataset (DBRD)**: book reviews from hebban.nl labelled positive or negative. |
| **Text type** | Long, opinionated book reviews. **Not** tweets, short social posts or service alerts. |
| **Language** | Dutch (`nl`) only |
| **Labels** | `positive`, `negative` only. **There is no neutral label.** |
| **Licence** | MIT |

**What this means for us:** a model fine-tuned on book reviews expects sentiment to be carried by adjectives in full sentences. Our stream is mostly short posts and factual outage alerts, and the model can never answer "neutral". Section 7 shows where this hurts.

### Comparison Models
- **Secondary Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`: a RoBERTa model trained on English tweets with three labels (negative / neutral / positive). We use it as a deliberately "wrong-language" comparison, so its low score on Dutch text is expected.
- **Rule-based Baseline**: a Dutch railway word list (`DUTCH_POSITIVE_WORDS` / `DUTCH_NEGATIVE_WORDS` in `src/models.py`). It has three outputs, including neutral.

### Language mix in the collected stream
Not every collected post is Dutch: of the first 582 stored items, 406 are tagged Dutch and 176 (about 30%) are tagged as another language (German, Polish, French, Romanian and others). These pass through a Dutch-only model, so their scores are less reliable.

---

## 5. System Architecture

```mermaid
flowchart LR
    A[Live Data Streams\n(Mastodon & Reddit RSS)] -->|Sanitize & Strip PII| B[Fetcher Engine\nfetcher.py]
    B -->|Batch Raw Posts| C[Pre-trained Transformer\nRobBERT Dutch / models.py]
    C -->|Timestamp + Sentiment| D[SQLite Storage\npulse.db & JSON Export]
    D -->|Aggregated Metrics| E[FastAPI Backend\napp.py]
    E -->|Real-time Charts & Drilldown| F[Interactive Dashboard\nstatic/index.html]
    F -->|Operational Alerts| G[Persona: Maaike van Dijk\nNS Operations]
```

---

## 6. How to Run the Tool (Autonomous Live Stream)

### Prerequisites
- Python 3.9+ installed (`python -m pip install -r requirements.txt`).

### Running the Live System:
```bash
# 1. Start the Live Dashboard + Autonomous Hourly Ingest (Recommended)
python run.py
# Open http://127.0.0.1:8000 in your browser.
# New commuter posts from Mastodon and Reddit are automatically fetched, scored, and added every hour!

# 2. Or customize the hourly interval (e.g., poll every 30 minutes / 1800s):
python run.py --interval 1800

# 3. Fetch fresh live items immediately once:
python run.py --fetch

# 4. Run headless autonomous hourly daemon (without launching browser/server):
python run.py --daemon --interval 3600

# 5. Run the 52-sample model evaluation benchmark:
python run.py --evaluate
```

### Live Stream Automation:
- **Local Server (`python run.py`)**: Runs an in-process background worker that fetches fresh transit posts every hour (3600s), scores sentiment with RobBERT, updates `pulse.db`, and synchronizes the frontend live without restarting.
- **On-Demand Live Refresh**: Click the **"Refresh Live Feed Now"** button in the dashboard at any time to ingest and score the latest posts instantly.
- **GitHub Pages / Cloud Automation (`.github/workflows/hourly_pulse.yml`)**: Includes an autonomous GitHub Actions cron job that runs every hour (`0 * * * *`) to fetch the latest transit posts and push fresh data directly to GitHub Pages.

### Checking that the pipeline really ran continuously
Every stored post has a `fetched_at` timestamp. To see how many items each hourly run added, run:

```bash
sqlite3 data/pulse.db "SELECT substr(fetched_at,1,13) AS hour, COUNT(*) FROM posts GROUP BY hour ORDER BY hour;"
```

A continuous pipeline shows one row per hour that had new posts. The first run (`python run.py --fetch`) collected a backlog, so it adds many items at once, and some of those posts were published long before the pipeline started (the `created_at` field shows when a post was written, `fetched_at` when we collected it). The GitHub Actions workflow only runs once the repository is pushed to GitHub.

**Pipeline timeline (honest note).** Our first collection run was on 9 October 2026 (431 posts, a backlog from the hashtag timelines). Earlier runs were started by hand. The unattended hourly GitHub Actions job started on 15 October 2026, so continuous automatic collection only covers the time since then. The per-hour query above shows exactly which hours have data.

---

## 7. Model Evaluation & Honest Failure Analysis

We labelled **52 posts from our own stream** by hand (33 negative, 15 neutral, 4 positive) and compared three systems on exactly the same items. The labels are in `src/evaluate.py`; the full per-item table is `data/test_comparison_table.csv` and the full write-up is `data/test_evaluation_report.md`. Re-run with `python run.py --evaluate`.

### 7.1 Results

| Subset | Items | RobBERT | Cardiff RoBERTa | Word list |
|:---|:---:|:---:|:---:|:---:|
| All items | 52 | **31/52 (59.6%)** | 18/52 (34.6%) | 25/52 (48.1%) |
| Labels RobBERT *can* produce (non-neutral) | 37 | **31/37 (83.8%)** | 3/37 (8.1%) | 22/37 (59.5%) |
| Human-written posts | 24 | **19/24 (79.2%)** | 6/24 (25.0%) | 9/24 (37.5%) |
| Machine-generated alerts (`STORING:` / `Storing voorbij:`) | 28 | 12/28 (42.9%) | 12/28 (42.9%) | **16/28 (57.1%)** |

### 7.2 How to read the numbers (caveats)
- **RobBERT cannot say neutral.** 15 of the 52 labels are neutral, so those are guaranteed misses. The 59.6% headline number partly measures our label scheme, not the model. The fairer figure is 31/37 (83.8%) on items where a correct answer was possible.
- **28 of the 52 items are near-identical machine alerts**, so the test set is not very varied. The human-written subset (24 items) says more about real commuter posts.
- **Cardiff says "neutral" for 49 of 52 items.** It scores on the neutral labels and almost nowhere else. It is an English model on Dutch text.
- **The word list is tuned to the alerts** (words like *storing* and *defect* are in the list), so its good score on alerts is optimistic. It is weak on human-written posts.
- Only 4 items are positive, so differences of one or two items are not meaningful.

### 7.3 Failure analysis
Explanations are our best reading, not proven. More detail is in `data/test_evaluation_report.md`.

1. **No neutral class (systematic).** `Storing voorbij: defecte trein Utrecht - Amersfoort #ns` is labelled *neutral* (the disruption is over) but RobBERT says `negative` (0.994). The words *defecte trein* carry negative meaning and *voorbij* does not flip them. All 12 `Storing voorbij` items are wrong.
2. **Factual alerts without emotional words (systematic, dangerous direction).** `STORING: overwegstoring 's-Hertogenbosch - Oss #storing #ns` is labelled *negative* but RobBERT says `positive` (0.992). 4 of the 16 `STORING` alerts were read as positive. A model trained on book reviews looks for adjectives, and a bare alert has none.
3. **Mixed message.** `Goedendag, u heeft contact met de virtuele AI assistent van de meldkamer NS. De melding komt nu pas bij mij binnen.` is labelled *negative* but RobBERT says `positive` (0.785). The friendly greeting hides an implicit complaint (*pas nu*, only now).
4. **Irony / silver lining.** `Morgen staken de NS-medewerkers weer. Werk dus een dagje thuis of geniet van de rust` is labelled *neutral* but RobBERT says `positive` (0.995). *Geniet van de rust* is positive on its own but here it is a light comment on a strike. (Our label is debatable here.)
5. **Jargon / hashtags only.** `Vertraging - #duitsland, #groningen, #trein, #vertraging` is labelled *negative* but RobBERT says `positive` (0.889). There is no sentence to read, only hashtags.

### 7.4 Which model would we hand to the user?
**RobBERT, with clear caveats.** Maaike's early-warning signal comes from what commuters write, and on the 24 human-written posts RobBERT scores 19/24 against 9/24 for the word list and 6/24 for Cardiff. Cardiff is not usable for Dutch (it calls almost everything neutral). The word list is excellent on official alerts, but only because it contains the words that appear in them, and it misses most human posts.

What Maaike should know before relying on it:
- **There is no neutral.** The "positive" share on the dashboard is overstated, because factual alerts and neutral news land in positive or negative. The negative share is the more meaningful signal.
- **False calm.** 4 of 16 outage alerts were read as positive. For an early-warning tool this is the wrong direction to be wrong in.
- **About 30% of stored items are not Dutch** and pass through a Dutch-only model.
- **Small test set** (52 items, only 4 positive).

**Suggested next steps (not tested yet):** treat the official alert format with a simple rule (or count those posts as incident volume instead of sentiment), and fine-tune RobBERT on a larger set of labelled rail posts with a neutral label.

---

## 8. Ethical Reflection

### 1. Representation & The "Silent Passenger" Bias
Social feeds over-index on tech-savvy, digitally vocal commuters and younger professionals. Older passengers, non-Dutch/non-English speakers, and travelers without smartphones do not voice concerns on Mastodon or Reddit. A dashboard showing positive sentiment could simply reflect that stranded passengers without internet access cannot post.

### 2. Risk of Astroturfing & Bot Floods
A small cluster of disgruntled automated feeds or coordinated campaign posts can artificially skew the Net Sentiment score downward. The dashboard mitigates this by tracking **Item Volume** concurrently with the sentiment index so sudden single-account spikes do not cause unwarranted operational panic.

### 3. Decisions & Harm Mitigation
If NS Operations relies solely on automated sentiment alerts, rural routes with low online post volume might be deprioritized during widespread network disruption in favor of high-traffic urban corridors. To prevent this, the dashboard is strictly designed as an **early warning decision-support tool**, not an autonomous dispatch system.

---

## 9. What This Tool Must NOT Be Used For

This dashboard is an early-warning **decision-support tool only**. It must not be used to:

1. **Make autonomous operational dispatch decisions** without a human operator reviewing the sentiment context and underlying posts first.
2. **Identify, profile, or single out individual passengers or social media users** — no usernames or profile data are stored, and none should ever be added. The stored post `url` contains the author's handle on Mastodon, so it must not be used to look up or track individual accounts.
3. **Represent the full passenger population**: the stream captures only tech-savvy, online, Dutch-posting commuters. It must not be treated as a statistically representative sample of all NS passengers.
4. **Replace formal complaint channels or official passenger satisfaction surveys** — the tool is a fast-signal supplement, not a substitute for structured feedback.
5. **Trigger punitive or disciplinary action against staff** based on a sentiment dip, since posts may reflect external factors (weather, infrastructure, third-party disruptions) entirely outside employee control.

---

## 10. Deliverables Included
- `src/fetcher.py`: Autonomous ingestion and PII sanitization.
- `src/models.py`: Hugging Face RobBERT inference & baseline pipeline.
- `src/storage.py`: SQLite persistence and aggregation.
- `src/scheduler.py`: Continuous background daemon.
- `src/app.py` & `src/static/index.html`: Non-technical interactive live dashboard.
- `src/evaluate.py`: Benchmark evaluation suite.
- `data/collected_posts.json`: **600+ real posts** collected across the stream (582 when we analysed the language mix; the count grows every hour; also stored in `data/pulse.db`).
- `data/test_comparison_table.csv`: 52 manually labeled items with predictions from all models.
- `data/test_evaluation_report.md`: Subset accuracies and failure analysis (regenerate with `python -m src.evaluate --report-only`).
g
