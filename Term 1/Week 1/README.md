# QuickStudy Hub

## What it does
QuickStudy Hub is a study app for History (extensible to other subjects). Students can:
- Upload their own PDF notes/textbook chapters
- Have AI (Google Gemini, via the Lovable AI gateway) automatically generate flashcards and multiple-choice quiz questions directly from that PDF's text
- Study with an interactive flip-card flashcard viewer
- Take auto-graded quizzes with immediate scoring
- Track progress (cards studied, quiz scores, completion %) over time

The AI step is the core of the app: raw PDF text is extracted, chunked, and sent to Gemini with a strict system prompt ("never invent facts not present in the text") and a structured output schema, so the generated material stays grounded in what the student actually uploaded - rather than generic quiz content.

## Who it's for
Students who have their own study materials (lecture PDFs, textbook excerpts, notes) but don't have time to manually turn them into flashcards and practice questions. It assumes the learner:
- Has a digital, text-based (not scanned-image) PDF
- Has a reasonably stable internet connection
- Can read/write in the language the PDF is written in

## Which SDG it addresses and why
**SDG 4 - Quality Education.** A major barrier to effective studying isn't access to material, it's time: converting a 20-page reading into usable active-recall practice (flashcards, quiz questions) can take far longer than reading it once, so many students skip active recall entirely and re-read passively instead, which is a much less effective study method. QuickStudy Hub removes that bottleneck, making evidence-based study techniques (flashcards, retrieval practice) accessible to any student with a PDF, not just those with time to build their own materials by hand.

## How to run it
```sh
git clone https://github.com/PancakMous/quickstudy-hub.git
cd quickstudy-hub
npm i
npm run dev
```
Requires a `LOVABLE_API_KEY` environment variable (for AI generation) and a configured Supabase project (for storage/auth) - see `.env` setup in the Lovable project settings.

## Ethical reflection
**Who is excluded?** Students without reliable internet (the AI generation step requires a live connection), without a digital/searchable PDF (scanned handwritten notes produce no extractable text and are rejected), or who can't afford data/device costs. Students who rely on screen readers may also be underserved, since PDF layout extraction isn't accessibility-tested.

**What does it assume?** That the learner already has a PDF worth studying, can read it independently, and has some baseline digital literacy (uploading files, navigating a web app).

**Misuse risk.** Because the AI is instructed not to invent facts, output is reasonably grounded - but it can still misread ambiguous or poorly-formatted source text and generate a subtly wrong flashcard that a student then studies as fact, with no second check. There's also a risk of over-reliance: a student could use the app to generate "study material" without ever reading the source PDF themselves, mistaking recognition of an AI-written answer for actual understanding. Mitigation: the in-app PDF reader is kept alongside the generated cards specifically so students can verify against the source, and answers are capped short (max 15 words) to reduce room for confident-sounding fabrication.
