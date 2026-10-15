# NS Rail Live Pulse: Passenger Sentiment Radar 🚆
### Autonomous Stream Intelligence for Dutch Rail Infrastructure (SDG 9)

**Live Pulse** is an autonomous sentiment monitoring system designed for Dutch public railway infrastructure (Nederlandse Spoorwegen - NS and ProRail). It continuously ingests real-time commuter reactions and incident announcements from live social and transit data streams, analyzes the sentiment of each item using a local pre-trained Dutch transformer (**RobBERT**), stores the results in a persistent time-series database, and visualizes passenger mood shifts on an interactive dashboard tailored for transit operational decision-makers.

---

## 1. Target Persona & Operational Decision
- **Named Persona**: **Maaike van Dijk**, Lead Incident Response & Passenger Experience Manager at NS Customer Operations Desk.
- **The Problem Today**: Commuter frustration with train delays, platform overcrowding, or rolling stock breakdowns typically bubbles up on social streams 30–60 minutes before escalating into formal press queries or major news headlines. By the time operations reads about it in the media, station halls are already overwhelmed.
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
- **Zero PII Stored**: User handles, screen names, profile URLs, avatars, and IDs are stripped immediately upon fetching.
- **Data Minimization**: The pipeline stores only the sanitized post text, standard UTC timestamp, and sentiment classification.

---

## 4. Pre-trained Hugging Face Transformer

### Primary Model: RobBERT Dutch Sentiment
- **Model Identifier**: `DTAI-KULeuven/robbert-v2-dutch-sentiment` (RoBERTa architecture pre-trained on large-scale Dutch corpora and fine-tuned for sentiment).
- **Why this model**: Dutch railway discourse contains idiomatic phrasing, transit slang, and Dutch syntactic structure (e.g., compound words like *wisselstoring*, *vertraging*, *bovenleiding*) that generic English models fail to parse.
- **Local Execution**: Loaded and run offline via Hugging Face `transformers` pipeline on local hardware (PyTorch backend).

#### Model Card Summary

| Detail | Value |
|:---|:---|
| **Trained on** | Dutch Wikipedia, news articles, books, and CommonCrawl web text (CCNet Dutch) |
| **Language** | Dutch (`nl`) only |
| **Labels** | `positive`, `negative` |
| **Licence** | MIT |

### Benchmark Comparison Models:
- **Secondary Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest` (multilingual RoBERTa).
- **Rule-based Baseline**: Domain-specific Dutch railway lexicon matcher.

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

---

## 7. Model Evaluation & Honest Failure Analysis

A gold-standard test set of **52 real transit posts** was manually annotated and benchmarked against both transformer models and the baseline.

### Quantitative Benchmark:
| Model / Pipeline | Correct / Total | Accuracy | Notes |
| :--- | :---: | :---: | :--- |
| **RobBERT Dutch (Primary)** | **31 / 52** | **59.6%** | High sensitivity to emotional and negative vocabulary. |
| **Rule-based Lexicon Baseline** | 25 / 52 | 48.1% | Fast, but misses subtle context and implicit sentiment. |
| **Cardiff RoBERTa (Secondary)** | 18 / 52 | 34.6% | Defaulted heavily to neutral on non-English text. |

### Failure Analysis (3 Key Failure Archetypes):
1. **Resolution vs. Incident Negation ('Storing voorbij')**:
   - *Post*: *"Storing voorbij: defecte trein Utrecht - Amersfoort"*
   - *Ground Truth*: `neutral` (service restored).
   - *Model Prediction*: `negative` (0.994).
   - *Root Cause*: The heavy negative weight of *"defecte trein"* overpowers the resolution marker *"voorbij"*.
2. **Factual Alerts Lacking Subjective Sentiment**:
   - *Post*: *"STORING: overwegstoring 's-Hertogenbosch - Oss #storing #ns"*
   - *Ground Truth*: `negative` (disruption).
   - *Model Prediction*: `positive` (0.992).
   - *Root Cause*: Pre-trained review models expect emotional adjectives (*vreselijk*, *slecht*). In their absence, formal announcements get misclassified.
3. **Irony & Empathy Nuances**:
   - *Post*: *"morgen de hele dag geen openbaar vervoer 😟 Ze gaan staken, ik snap de woede maar reizigers zijn de dupe"*
   - *Ground Truth*: `negative`.
   - *Model Prediction*: Tendency to misweigh *"ik snap de woede"* (understanding/solidarity) against passenger frustration.

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
2. **Identify, profile, or single out individual passengers or social media users** — no usernames, handles, or profile data are stored, and none should ever be added.
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
- `data/collected_posts.json`: **431 real posts** collected across the stream.
- `data/test_comparison_table.csv`: 52 manually labeled items with predictions from all models.
- `data/test_evaluation_report.md`: Detailed failure analysis report.
