# event_organiser_ai_agents
# 🤖 AI Event Organizer with CrewAI

This project helps you organize an **AI Conference** using smart agents powered by AI!

We built a team of **virtual assistants** (we call them "agents") that work together to plan an event. These agents talk to tools on the internet to find venues, arrange logistics, and promote the event.

---

## 🧠 What It Does

There are 3 smart agents:

1. **Venue Coordinator**  
   👉 Finds a suitable venue in the city you give (like a hotel or hall in Mumbai).

2. **Logistics Manager**  
   👉 Plans food, seating, lights, microphones—everything the event needs.

3. **Marketing & Communication Agent**  
   👉 Spreads the word and helps bring people to your event.

They work **together as a team** to handle everything smoothly.

---

## 📦 Files You Will See

| File Name          | What It Does                                      |
|-------------------|---------------------------------------------------|
| `main.py`         | Main script that runs the show                    |
| `utils.py`        | Fetches your secret API keys                      |
| `venue_data.json` | Shows the venue details chosen by the AI          |
| `event_summary.md`| Summary of the event planning report              |

---

## 🚀 How to Run

Follow these steps to run this on your computer:

### ✅ Step 1: Set Up Your Environment

You need Python installed (version 3.10 or higher).

Install the required packages:

```bash
pip install crewai openai crewai-tools pydantic


✅ Step 2: Set Your API Keys
You need:

OpenAI API Key

Serper.dev API Key

Create a .env file or set them in your terminal like this:

export OPENAI_API_KEY=your_openai_key
export SERPER_API_KEY=your_serper_key

Or you can store these in a utils.py file:

✅ Step 3: Run the Script
Now simply run:

python tech_event_origanising.py

INPUT

You want to plan an event in Mumbai for 200 people about AI.
This tool helps you:

Find a hall

Arrange speakers, mics, food

Advertise it online

All with the help of AI agents!

OUTPUT

It will print outputs in your terminal and create:

A summary file event_summary.md

A JSON file venue_data.json with selected venue info

❤️ Made For Learning
This project is a hands-on way to learn about:

Generative AI

Agent collaboration

Real-world applications of Python and APIs

Enjoy organizing your own tech event using AI! 🎉
