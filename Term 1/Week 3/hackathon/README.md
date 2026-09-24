# 🇳🇱 Dutch4You

### AI for Good - Hackathon 3: Equal Access

Dutch4You is an AI-powered Streamlit application that helps non-Dutch speakers understand Dutch letters, notices, and official communications.

The user pastes Dutch text into the application and receives:

* 🇬🇧 An English translation
* 🧠 A plain-language explanation
* 📌 Important practical information, such as:

  * Deadlines
  * Amounts
  * Required actions
* ⚠️ A warning and confidence level when the input is unclear or the AI is uncertain

**Live demo:** https://dutch4you.streamlit.app/

---

## User group

Intended users: international and exchange students, and other newcomers with little or no Dutch. They paste text from a phone or laptop, often under time pressure, and act on the result themselves.
Not intended users:
People who need a certified or legally valid translation.
People in a legal or immigration dispute (for example a decision from the IND).
People who need to translate images, scans, audio or handwriting. The prototype accepts pasted text only.

---

## 🎯 The Problem

Many important communications in the Netherlands are written in Dutch. For someone who is still learning Dutch, understanding an official letter can be difficult, especially when the text contains deadlines, payments, required documents, or other actions.

This creates an information-access problem: a person may receive the same information as everyone else but still have more difficulty understanding what they are expected to do.

Dutch4You focuses on reducing this specific language-accessibility barrier.

The Netherlands had about **18.0 million inhabitants on 1 January 2025**, of whom **16.8% - just over 3 million people - were born abroad**, according to Statistics Netherlands (CBS).

This does not mean that everyone born abroad has difficulty with Dutch. However, it shows that a substantial part of the population has an international background, making accessible communication an important consideration.

---

## 🌍 Sustainable Development Goal

### SDG 10 - Reduced Inequalities

Dutch4You addresses **United Nations Sustainable Development Goal 10: Reduced Inequalities**.

More specifically, it connects to **Target 10.2**, which calls for promoting the social, economic and political inclusion of everyone, regardless of characteristics including origin, ethnicity, disability, religion or economic status.

The project focuses on **language and information accessibility**.

The goal is not to replace official communication or professional interpreters. Instead, Dutch4You provides an additional layer of understanding so that someone who struggles with Dutch can more easily understand what a piece of text says and what practical actions it mentions.

---

## 💡 What the Tool Does

The application uses Google's Gemini API through Python.

### Input

The user pastes Dutch text, for example:

> U dient uiterlijk 30 september uw documenten in te leveren.

### AI processing

The application sends the text to the Gemini API with instructions to:

1. Translate the text into English.
2. Explain the meaning using simple language.
3. Extract important practical information.
4. Identify uncertainty or ambiguity.
5. Return the result in a structured JSON format.

### Output

The application displays:

**Translation**

> You must submit your documents by 30 September at the latest.

**Explanation**

A simple explanation of what the message means.

**Important information**

* Deadline: 30 September
* Required action: Submit the documents

The structured response makes the result easier for the application to display consistently.

---

## 🧑‍🤝‍🧑 Target Users

Dutch4You is designed primarily for people who:

* Live, study or work in the Netherlands
* Are still learning Dutch
* Receive Dutch administrative or official communications
* Need help understanding practical information in Dutch

Potential examples include international students, newcomers, migrants, and other non-Dutch speakers.

The tool can be useful for university, housing, healthcare, and public-service communications.

---

## 🤖 Technology

| Component             | Technology                |
| --------------------- | ------------------------- |
| Programming language  | Python                    |
| User interface        | Streamlit                 |
| AI model              | Google Gemini             |
| AI API                | Google GenAI SDK          |
| Environment variables | python-dotenv             |
| Deployment            | Streamlit Community Cloud |
| Version control       | Git + GitHub              |

### Project structure

```text
hackathon/
├── app.py
└── dutch4you_core.py
```

The repository also contains a root-level `requirements.txt` used for deployment.

---

## ⚙️ How It Works

The application has two main Python files.

### `app.py`

Responsible for the Streamlit interface.

It:

* Creates the text input area
* Displays the Translate & Explain button
* Shows the translation
* Shows the explanation
* Displays extracted deadlines, amounts and actions
* Displays warnings and confidence information

### `dutch4you_core.py`

Contains the main AI logic.

It:

* Loads the Gemini API key
* Creates the Gemini client
* Builds the prompt
* Calls the Gemini API
* Retries temporary server errors
* Parses the AI's JSON response
* Handles invalid or failed responses

---

## 🛡️ Handling AI Errors and Edge Cases

Because an LLM can produce incorrect or incomplete information, Dutch4You does not assume that every response is reliable.

The application handles several edge cases.

### Empty input

If the user does not enter any text, the application asks them to provide text instead of making an unnecessary API request.

### API failure

If the Gemini API call fails, the application returns an error result rather than crashing.

Temporary server overload errors are retried automatically.

### Invalid AI response

The AI is instructed to return JSON. If the response cannot be parsed as valid JSON, the application returns a warning instead of displaying unpredictable output.

### Non-Dutch or unreadable text

The prompt instructs the model not to guess when the input does not look like Dutch or is unreadable.

The application assigns a low confidence level and provides a warning.

### Low-confidence output

When the model returns low confidence, the application tells the user to double-check the information with an official source or a Dutch speaker before acting on it.

---

## ⚠️ Ethical Reflection

The biggest risk of Dutch4You is that a user could **trust an incorrect AI explanation when they cannot independently verify the original Dutch text**. This could be particularly harmful if the text contains a legal deadline, healthcare information, payment requirement, or another important instruction.

The tool therefore does not present itself as an official translator or professional advisor. It provides a confidence level and warning system, and low-confidence results explicitly tell users to verify the information with an official source or Dutch speaker. The application also extracts practical information separately rather than pretending that the AI interpretation is authoritative. This limitation is important because the same technology intended to reduce an information-access inequality could create another inequality if people with less ability to verify AI output become more dependent on it.

---

## 📊 Why This Problem Matters

Language accessibility is relevant to the broader goal of reducing inequalities because people cannot effectively act on information they cannot understand.

CBS reported that on **1 January 2025, more than 3 million people living in the Netherlands had been born abroad**, representing **16.8% of the population**. CBS also reported that around **2.1 million people born in the Netherlands were children of migrants**.

These numbers do **not** indicate how many people experience language difficulties, and Dutch4You does not claim that all internationally born residents need translation assistance. They simply demonstrate that the Netherlands has a large population with international backgrounds, making accessible communication a relevant problem to investigate.

Globally, the UN identifies inclusion regardless of origin and other characteristics as part of SDG 10, specifically Target 10.2.

---

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/PancakMous/ai4g-portfolio-EvaldasPocius.git
cd ai4g-portfolio-EvaldasPocius
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

The required packages are:

```text
streamlit
python-dotenv
google-genai
```

### 3. Create a `.env` file

Create a `.env` file for local development:

```text
GEMINI_API_KEY=your-key-here
```

**Do not commit this file to GitHub.**

The API key should remain private.

### 4. Run the application

From the repository root:

```bash
streamlit run "Term 1/Week 3/hackathon/app.py"
```

The application should open in your browser.

---

## ☁️ Deployment

The application is deployed using Streamlit Community Cloud.

The deployed application uses Streamlit Secrets for the Gemini API key rather than storing the key in the GitHub repository.

The live application is available at:

**https://dutch4you.streamlit.app/**

---

## 🎥 Demo

A short screen recording demonstrates the working application.

The demo shows:

1. Entering Dutch text
2. Sending the text to the AI
3. Receiving an English translation
4. Receiving a plain-language explanation
5. Extracting practical information
6. Handling uncertain or unsuitable input

---

## 📝 Hackathon Requirements Checklist

| Requirement                     | Dutch4You                                        |
| -------------------------------- | ------------------------------------------------ |
| Python-native application       | ✅ Streamlit + Python                            |
| Live LLM API calls              | ✅ Google Gemini API                              |
| Addresses a concrete inequality | ✅ Dutch language/information accessibility      |
| Handles AI failure/edge cases   | ✅ Errors, retries, invalid JSON, low confidence |
| Ethical reflection              | ✅ Included above                                |
| Working product                 | ✅ Live Streamlit deployment                     |
| README                          | ✅ This document                                 |
| Demo                             | 🎥 Screen recording                              |

---

## 🔐 Privacy & Security

Dutch4You requires a Gemini API key to make AI requests.

The API key is **not stored in the GitHub repository**.

For local development, the key is stored in `.env`.

For the deployed application, the key is stored using Streamlit Secrets.

Users should avoid submitting highly sensitive personal information unless they understand how the underlying AI service processes submitted data.

---

## 📚 Sources

* United Nations - **SDG 10: Reduced Inequalities**
* United Nations - **Goal 10: Reduced Inequalities**
* Statistics Netherlands (CBS) - **Residents of the Netherlands born abroad**
* Statistics Netherlands (CBS) - **Population by origin and country of birth**

---

## 👥 Hackathon

**Course:** AI for Good
**Hackathon:** Hackathon 3 - Equal Access
**Theme:** Equal Access
**SDG:** 10 - Reduced Inequalities
**Technology:** Python + Gemini API + Streamlit
