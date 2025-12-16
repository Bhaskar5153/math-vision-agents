# import the necessary libraries and modules
from google.adk.agents import Agent
# from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from math_agents.tools import (
    solve_algebra_problem,
    solve_geometry_problem,
    solve_calculus_problem,
    solve_trigonometry_problem,
    solve_linear_algebra_problem,
    solve_statistics_problem,
    solve_probability_problem
)




AGENT_MODEL = "gemini-2.5-flash" # Starting with Gemini

root_agent = Agent(
    name="RootAgent",
    model=AGENT_MODEL, # Can be a string for Gemini or a LiteLlm object
    description="Provides math problem-solving assistance.",
    instruction="You are a helpful math assistant. "
                "When the user asks for help with a math problem, "
                "use the appropriate tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the solution clearly.",
    tools=[
        solve_algebra_problem,
        solve_geometry_problem,
        solve_calculus_problem,
        solve_trigonometry_problem,
        solve_linear_algebra_problem,
        solve_statistics_problem,
        solve_probability_problem
    ],
)

print(f"Agent '{root_agent.name}' created using model '{AGENT_MODEL}'.")