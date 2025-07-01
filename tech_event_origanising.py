import warnings
import os
import re
import json
import unicodedata
from crewai import Agent, Crew, Task
from pydantic import BaseModel
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from utils import get_openai_api_key, get_serper_api_key

warnings.filterwarnings('ignore')

def clean_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', ' ', text)

def safe_ascii_env(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()

# Set environment variables
os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["SERPER_API_KEY"] = get_serper_api_key()
os.environ["OPENAI_MODEL_NAME"] = safe_ascii_env("gpt-3.5-turbo")
os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"

# Sanitize text in dictionary
def sanitize_dict(d):
    for k, v in d.items():
        if isinstance(v, str):
            d[k] = clean_ascii(v)
        elif isinstance(v, list):
            d[k] = [clean_ascii(i) if isinstance(i, str) else i for i in v]
    return d

# Initialize tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Agents
venue_coordinator = Agent(
    role="Venue Coordinator",
    goal=clean_ascii("Identify and book an appropriate venue based on event requirements"),
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=clean_ascii(
        "With a keen sense of space and understanding of event logistics, you excel at finding and securing "
        "the perfect venue that fits the event's theme, size, and budget constraints."
    )
)

logistics_manager = Agent(
    role='Logistics Manager',
    goal=clean_ascii("Manage all logistics for the event including catering and equipment"),
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=clean_ascii(
        "Organized and detail-oriented, you ensure that every logistical aspect of the event from catering to "
        "equipment setup is flawlessly executed to create a seamless experience."
    )
)

marketing_communications_agent = Agent(
    role="Marketing and Communications Agent",
    goal=clean_ascii("Effectively market the event and communicate with participants"),
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=clean_ascii(
        "Creative and communicative, you craft compelling messages and engage with potential attendees to maximize "
        "event exposure and participation."
    )
)

# Pydantic model for structured output
class VenueDetails(BaseModel):
    name: str
    address: str
    capacity: int
    booking_status: str

# Tasks
venue_task = Task(
    description=clean_ascii("Find a venue in {event_city} that meets criteria for {event_topic}."),
    expected_output=clean_ascii("A structured JSON containing details of a venue: name, address, capacity, and booking status."),
    human_input=True,
    output_pydantic=VenueDetails,
    output_file="venue_details.json",
    agent=venue_coordinator
)

logistics_task = Task(
    description=clean_ascii("Coordinate catering and equipment for an event with {expected_participants} participants on {tentative_date}."),
    expected_output=clean_ascii("Confirmation of all logistics arrangements including catering and equipment setup."),
    human_input=True,
    async_execution=False,
    agent=logistics_manager
)

marketing_task = Task(
    description=clean_ascii("Promote the {event_topic} aiming to engage at least {expected_participants} potential attendees."),
    expected_output=clean_ascii("Report on marketing activities and attendee engagement formatted as markdown."),
    async_execution=True,
    output_file="marketing_report.md",
    agent=marketing_communications_agent
)

# Crew setup
event_management_crew = Crew(
    agents=[venue_coordinator, logistics_manager, marketing_communications_agent],
    tasks=[venue_task, logistics_task, marketing_task],
    verbose=True
)

# Event details
event_details = sanitize_dict({
    "event_topic": "AI Innovation Conference 2025",
    "event_description": (
        "An exclusive gathering of AI innovators, entrepreneurs, researchers, and industry leaders to explore "
        "groundbreaking advancements in Artificial Intelligence, Machine Learning, and responsible AI practices. "
        "The conference will include keynote talks, panel discussions, networking sessions, and live demonstrations."
    ),
    "event_city": "Mumbai",
    "tentative_date": "2025-07-15",
    "expected_participants": 200,
    "budget": 200000,
    "venue_type": "Modern Conference Hall with AV and Wi-Fi",
    "duration": "1 day",
    "key_requirements": [
        "High-speed internet/Wi-Fi",
        "Audio/Visual equipment (projectors, microphones)",
        "On-site catering for 200 attendees",
        "Green room for speakers",
        "Accessibility features (ramps, elevators)",
        "Backup power supply"
    ],
    "target_audience": [
        "AI researchers and engineers",
        "Tech executives and founders",
        "VCs and investors",
        "Product managers and analysts",
        "University students and professors"
    ]
})

# Execute crew and process output
try:
    result = event_management_crew.kickoff(inputs=event_details)

    print(f"\n🔍 Type of result: {type(result)}")
    print(f"\n📦 Crew Final Output:\n{str(result)}")

    # Process each task output
    for task_output in result.task_outputs:
        print(f"\n📝 Output from task: {task_output.task.name}")
        if hasattr(task_output, "pydantic_output"):
            venue_data = task_output.pydantic_output.model_dump()
            print("\n📍 Parsed Venue Details:")
            print(json.dumps(venue_data, indent=2))
            # Optional: Save to JSON
            with open("venue_data.json", "w", encoding="utf-8") as f:
                json.dump(venue_data, f, indent=2)
        else:
            print(task_output.output)

    # Save summary
    with open("event_summary.md", "w", encoding="utf-8") as f:
        f.write(str(result))

    print("\n✅ Event summary saved to event_summary.md")

except Exception as e:
    print(f"❌ Error running or processing crew output: {e}")
