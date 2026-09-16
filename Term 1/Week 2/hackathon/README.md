# Daily Mental Health Check-in

**AI for Good - Hackathon 2: Flow State**
**Tool:** n8n · **SDG:** 3 - Good Health & Well-being

## What it does

Every day at 18:00, the workflow automatically emails the user a link to a short check-in form. The form asks them to rate their mood, stress, and energy (1–10), pick their main concern from a list, and optionally add a short note about what's on their mind.

On submission, an AI node reads the answers and generates a short, personal response made up of an affirmation, a reflection on what they shared, and one small, low-effort action for the day. The response is shown on-screen and also emailed to the user. If the mood score is very low or the stress score is very high, the message automatically includes local support resources (113 Zelfmoordpreventie, GP contact) before it's sent. Every check-in is logged to a Google Sheet (date, scores, concern, note, AI response) so mood trends are visible over time.

## Who it's for

Anyone who wants a low-effort daily habit of checking in with their own mental state - not a clinical tool, but a lightweight nudge toward self-awareness and small, doable actions.

## Why SDG 3

SDG 3 (Good Health and Well-being) explicitly includes mental health alongside physical health. This project targets one of the biggest barriers to mental well-being: most people never check in with themselves regularly, and by the time they notice they're struggling, it's already a harder problem. A daily, automated, near-zero-effort check-in lowers that barrier, and the AI-generated response makes each check-in feel individually acknowledged rather than like filling out a form into a void.

## How it works (workflow structure)

1. **Daily Reminder 18:00** (Schedule Trigger) → **Email Reminder** - sends the daily link to the check-in form.
2. **Daily Check-in** (Form Trigger) - user submits mood, stress, energy, concern, and an optional note.
3. **Edit Fields** - normalizes the submitted data and adds the date.
4. **Generate Response** (AI node, LLM chain + OpenAI chat model) - produces a personalized affirmation, reflection, and small action based on the check-in answers.
5. **Build Sheet Row** → **Log to Google Sheet** - logs the check-in and AI response for later review.
6. **Needs Support?** (IF node) - checks whether mood is very low or stress is very high.
   - If yes → **Add Support Resources** appends crisis/support contact info to the message.
   - If no → **Pass Response Through** leaves the message as generated.
7. **Email Final Message** and **Show Response** - the final message (with or without added resources) is emailed to the user and shown on-screen.

## How to run it

1. Import `Daily Mental Health Check-in.json` into your own n8n instance (Cloud or self-hosted).
2. Set up credentials:
   - An OpenAI (or other supported) API credential for the **OpenAI Chat Model** node.
   - An SMTP credential for **Email Reminder** and **Email Final Message** (Gmail with an App Password is the most reliable option).
   - A Google Sheets OAuth2 credential for **Log to Google Sheet**, pointed at a sheet with columns: `date, mood, stress, energy, concern, note, ai_response`.
3. Update the `fromEmail`/`toEmail` fields in both email nodes to your own addresses.
4. Update the form link inside the **Email Reminder** node's message to match your own instance's form URL.
5. Activate the workflow (toggle top right). It will now run automatically every day at 18:00.
