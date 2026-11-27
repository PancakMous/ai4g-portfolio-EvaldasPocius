# Learning Goal 1
**Title: Build a Local AI Backend with Python and Ollama**

## 1. What Will You Achieve?

I will build a Python backend that communicates with a locally hosted language model through Ollama. The backend will accept a text message, send it to the model, receive the generated response and return the response in a format that can be used by Pepper.

I will also investigate how the backend can communicate with Choregraphe. I plan to keep the modern Python backend separate from Choregraphe's older Python environment and connect the two through HTTP, if the available Pepper setup supports this.

**I will be finished when:**
I can demonstrate a Python program sending at least 10 test messages to a local Ollama model and receiving responses, with basic error handling. I will also demonstrate or document a successful connection to the Pepper/Choregraphe workflow.

## 2. Why Do You Want To Achieve It?

I want to understand how an AI application works behind the scenes instead of only using existing chatbots or AI services. I have used AI tools, but I want practical experience building the software that communicates with a language model.

This goal is directly connected to my role in the Pepper project because Pepper needs an AI component to generate conversational responses. I am especially interested in running a model locally with Ollama because it gives us more control over the model and allows us to explore privacy-conscious AI development. Learning how to connect Python, an AI model and another application will also be useful for my future work in software development and AI.

## 3. How Will You Achieve It?

1. Check my computer's hardware and software requirements, install Ollama and run a suitable local model, starting with Gemma 3 (1B) if it performs adequately.
2. Read the Ollama API documentation and test sending a prompt to the model.
3. Write a Python program that sends HTTP requests to Ollama, processes the JSON response and returns the generated text.
4. Add reusable functions and basic error handling for problems such as Ollama not running, connection failures or invalid responses.
5. Test the backend with at least 10 different messages and record whether each request works.
6. Agree on a message format with the team member responsible for Choregraphe, then investigate or implement communication between the backend and Pepper.
7. Document the code, test results, problems and solutions.

## 4. Who Or What Do You Need?

### People:
- The team member responsible for Choregraphe and Pepper integration: to agree on how Pepper will send messages to the backend and receive responses.
- The team member responsible for speech recognition: to agree on the text format that will be passed to the AI backend.
- My project group: to test the backend and provide feedback.
- The project instructor or technical support: for advice if I encounter compatibility or robot-access problems.

### Tools & Software:
- A computer capable of running a small local language model.
- Python 3 and an editor such as Visual Studio Code.
- Ollama and a suitable model, such as Gemma 3 (1B), subject to hardware and compatibility testing.
- HTTP requests and JSON for communication.
- Choregraphe and access to Pepper for integration testing.
- Git and GitHub to track and document my code.

### Data & Resources:
- Ollama's official documentation and API reference.
- Python documentation.
- Example messages that represent the kinds of conversations Pepper should support.
- The team's agreed interface or message format for communication with Pepper.

### Possible Obstacles, And What I Will Do About Them:
- The model may run slowly: I will test a small model first, measure response time and consider another lightweight model if necessary.
- Ollama may not be reachable from the Pepper environment: I will test the network connection early and use a separate backend process with HTTP communication.
- Choregraphe uses an older Python environment: I will keep the backend in a separate modern Python environment rather than requiring modern packages inside Choregraphe.
- The AI may return an unexpected response format: I will validate the response and handle missing or invalid fields.
- Pepper may not be available for every test: I will test the backend independently on my computer and use Pepper when access is available.

## 5. Timeline

**Start date: Term 2, Week 11 (add the exact calendar date from the course schedule).**
**Target completion date: Term 2, Week 20 (add the exact calendar date from the course schedule).**

### Milestones:
1. Ollama is installed, a local model runs, and I have tested a basic request. Deadline: Week 12.
2. A Python backend sends messages to Ollama and processes JSON responses. Deadline: Week 14.
3. Error handling is added and at least 10 test messages have been tested and recorded. Deadline: Week 15.
4. The backend is demonstrated or documented as connected to the Pepper/Choregraphe workflow. Deadline: Week 19.

### Gantt Chart – Text Version
Weeks:       11  12  13  14  15  16  17  18  19  20
Research/
Ollama:      ██  ██
API tests:       ██  ██
Python
backend:             ██  ██
Error
handling:                ██  ██
Message
testing:                     ██
Pepper
integration:                    ██  ██  ██
Final demo
and review:                              ██  ██

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
