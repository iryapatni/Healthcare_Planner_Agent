import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.tools import CheckResourceAvailabilityTool

def run_healthcare_planner(api_key: str, user_goal: str) -> str:
    """
    Initializes and runs the CrewAI healthcare planning process.
    """
    # Set the Google API key in the environment
    os.environ["GOOGLE_API_KEY"] = api_key

    # Initialize the LLM (Gemini 2.5 Flash)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        verbose=True,
        temperature=0.4,
        google_api_key=api_key
    )

    # Initialize the custom Mock Tool
    resource_tool = CheckResourceAvailabilityTool()

    # Define the Medical Planning Coordinator Agent
    planner_agent = Agent(
        role='Medical Planning Coordinator',
        goal='Orchestrate complex healthcare tasks, validate resources, and generate detailed execution schedules.',
        backstory="""You are an expert Medical Planning Coordinator with years of experience 
        managing hospital operations and patient care logistics. Your job is to take high-level 
        medical goals, break them down into actionable steps, verify resource availability using 
        the tools at your disposal, and output a structured execution schedule that safely and 
        efficiently accomplishes the goal. You are meticulous and always ensure dependencies are met.""",
        verbose=True,
        allow_delegation=False,
        tools=[resource_tool],
        llm=llm
    )

    # Define the Planning Task
    planning_task = Task(
        description=f"""Process this high-level healthcare goal: '{user_goal}'.
        
        Follow these exact steps:
        1. Decompose the goal into actionable, sequential steps.
        2. Identify the specific medical resources (e.g., Doctors, Specialists, MRI Scanners, ICU Beds, Rooms) needed for each step.
        3. Use the 'Check Resource Availability Tool' to validate if each identified resource is available.
        4. Based on the steps and resource availability, generate a detailed execution schedule. 
        
        Important constraints:
        - Handle dependencies carefully (e.g., 'Blood Test Results' must be available before 'Consultation').
        - If a resource is absolutely unavailable according to the tool, suggest an alternative or note the delay.
        - Assume most standard resources are available unless the tool says otherwise.
        """,
        expected_output="""A detailed execution schedule in markdown format, including:
        - A list of the decomposed steps.
        - The resources validated for each step, and their availability status.
        - A clear, chronological schedule with dependencies explicitly stated for each step.
        """,
        agent=planner_agent
    )

    # Define the Crew and its execution process
    crew = Crew(
        agents=[planner_agent],
        tasks=[planning_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the workflow
    result = crew.kickoff()
    
    # Return the raw string output of the agent
    return str(result.raw if hasattr(result, 'raw') else result)
