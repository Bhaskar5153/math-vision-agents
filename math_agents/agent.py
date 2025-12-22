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

from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio


APP_NAME = "Math_Vision_Animation"
USER_ID="user1234"
SESSION_ID="1234"

AGENT_MODEL = "gemini-2.5-flash" # Starting with Gemini

solve_algebra_problem_tool = FunctionTool(func=solve_algebra_problem)
solve_calculus_problem_tool = FunctionTool(func=solve_calculus_problem)
solve_geometry_problem_tool = FunctionTool(func=solve_geometry_problem)
solve_linear_algebra_problem_tool = FunctionTool(func=solve_linear_algebra_problem)
solve_probability_problem_tool = FunctionTool(func=solve_probability_problem)
solve_statistics_problem_tool = FunctionTool(func=solve_statistics_problem)
solve_trigonometry_problem_tool = FunctionTool(func=solve_trigonometry_problem)






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
        solve_algebra_problem_tool,
        solve_geometry_problem_tool,
        solve_calculus_problem_tool,
        solve_trigonometry_problem_tool,
        solve_linear_algebra_problem_tool,
        solve_statistics_problem_tool,
        solve_probability_problem_tool
    ],
)


async def main():
    """Main function to run the agent asynchronously."""
    # Session and Runner Setup
    session_service = InMemorySessionService()
    # Use 'await' to correctly create the session
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    # Agent Interaction
    query = "explain (a+b)**2"
    print(f"User Query: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    # The runner's run method handles the async loop internally
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response:", final_response)

# Standard way to run the main async function
if __name__ == "__main__":
    asyncio.run(main())

# print(f"Agent '{root_agent.name}' created using model '{AGENT_MODEL}'.")