# Learning Goal 3
**Title: Test the Reliability, Privacy and Responsible Use of Pepper's Local AI**

## 1. What Will You Achieve?

I will create and carry out a test plan to evaluate the reliability and responsible behaviour of the AI component used in Pepper.

I will test at least 10 situations that could cause problems, including unclear questions, requests outside Pepper's purpose, questions involving personal information, incorrect assumptions and questions for which the model does not know the answer.

I will document the results and define practical rules for how the AI should respond. I will also investigate what conversation information is processed or stored by the local Ollama setup and make recommendations about what the project should retain or avoid collecting.

**I will be finished when:**
I have completed and documented at least 10 risk-focused tests, identified the main limitations or failure cases, and written a short set of practical privacy and response rules for the Pepper AI component.

## 2. Why Do You Want To Achieve It?

AI-generated answers can sound confident even when they are incorrect. Since Pepper is intended to interact with people, it is important that the AI does not give misleading information or create unrealistic expectations about what it can do.

I want to learn how to identify risks in an AI application and test those risks in practice. I am also interested in understanding what running an AI model locally means for privacy, rather than assuming that local hosting automatically makes a system completely private or safe.

This goal will help me become more critical and responsible when developing AI systems. It is relevant to the Pepper project because the AI should be helpful while being clear about its limitations.

## 3. How Will You Achieve It?

1. Research common risks of generative AI, including hallucinations, bias, inappropriate output and privacy issues.
2. Identify the types of questions and information that are appropriate for Pepper to handle.
3. Check how the local Ollama setup processes requests and whether prompts or conversation history are stored by the application or surrounding code.
4. Create at least 10 test cases, including unclear questions, out-of-scope requests, requests for sensitive information and questions with no reliable answer.
5. Run the test cases and record the model's responses.
6. Assess each response against criteria such as safety, honesty, relevance and whether it admits uncertainty.
7. Write practical system rules for handling sensitive information, uncertain answers and requests outside Pepper's purpose.
8. Share the findings with the team and add relevant rules to the AI prompt or backend where appropriate.

## 4. Who Or What Do You Need?

### People:
- The team member responsible for conversation design: to agree on appropriate response rules and boundaries.
- The team member responsible for AI integration: to implement any agreed changes in the prompt or backend.
- My project group and instructor: to review the test plan and discuss risks.
- If available, a teacher or domain expert familiar with responsible AI or privacy: to provide feedback on the approach.

### Tools & Software:
- Ollama and the local language model.
- The Python backend and prompt configuration used by Pepper.
- A document or spreadsheet for the test plan and results.
- GitHub for documenting changes and findings.

### Data & Resources:
- Official Ollama documentation, especially information about local operation and configuration.
- Reliable guidance on responsible AI, privacy and generative-AI limitations.
- Example prompts and test scenarios that do not require real personal information.
- The project's intended-use description and agreed boundaries.

### Possible Obstacles, And What I Will Do About Them:
- The model may give different answers to the same test: I will record the prompt and relevant settings and repeat important tests.
- It may be difficult to decide whether an answer is safe or appropriate: I will use written evaluation criteria and discuss uncertain cases with the team.
- Local hosting may create a false sense of privacy: I will check the full data flow, including application logs and stored conversation history, rather than assuming that local means no data is retained.
- There may not be time to fix every issue: I will prioritise the most important risks and document remaining limitations clearly.
- Testing with real residents may not be possible: I will use realistic fictional scenarios and avoid collecting sensitive personal data.

## 5. Timeline

**Start date: Term 2, Week 11 (add the exact calendar date from the course schedule).**
**Target completion date: Term 2, Week 20 (add the exact calendar date from the course schedule).**

### Milestones:
1. Research AI risks and identify Pepper's intended-use boundaries. Deadline: Week 13.
2. Prepare at least 10 risk-focused test cases and an evaluation checklist. Deadline: Week 15.
3. Run the tests, document failures and identify improvements. Deadline: Week 18.
4. Write privacy and response recommendations and share the final results with the team. Deadline: Week 20.

### Gantt Chart – Text Version
Weeks:        11  12  13  14  15  16  17  18  19  20
Risk and
privacy research: ██  ██  ██
Define
boundaries:           ██
Test case
preparation:              ██  ██
Run risk
tests:                         ██  ██  ██
Review and
prioritise:                             ██
Rules and
recommendations:                          ██  ██
Final report
and reflection:                                ██

## 6. Progress Log

Update this section throughout Term 2. Only add entries for work that I have actually completed.

Date: ____________________
What I did: ______________________________________________
Where I am now: __________________________________________

Date: ____________________
What I did: ______________________________________________
Where I am now: __________________________________________

Date: ____________________
What I did: ______________________________________________
Where I am now: __________________________________________
