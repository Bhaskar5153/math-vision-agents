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
    solve_probability_problem,
    animation_tool
)

from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
# from math_agents.animation_agent import AnimationDirector, story_generator, critic, reviser, grammar_check, tone_check, animation_generator
from google.adk.agents.invocation_context import InvocationContext
from math_agents.animation_agent import AnimationDirector

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
animation_tool_generator = FunctionTool(func=animation_tool)

# --- Composite tool for math solution and animation ---
async def solve_and_animate(problem: str, tool_context: InvocationContext) -> dict:
    # Try all math solvers in order (algebra, geometry, calculus, etc.)
    # You can make this smarter with intent detection if needed
    for solver in [
        solve_algebra_problem,
        solve_geometry_problem,
        solve_calculus_problem,
        solve_trigonometry_problem,
        solve_linear_algebra_problem,
        solve_statistics_problem,
        solve_probability_problem,
        
    ]:
        math_result = solver(problem, tool_context)
        if math_result.get("status") == "success":
            solution = math_result["answer"]
            break
    else:
        return {"status": "error", "error_message": "Could not solve the problem with any math tool."}
    # Generate animation plan and code
    animation_result = await animation_tool(solution, problem)
    return {
        "status": "success",
        "solution": solution,
        "animation_plan": animation_result.get("animation_plan"),
        "blender_code": animation_result.get("blender_code"),
    }

solve_and_animate_tool = FunctionTool(func=solve_and_animate)

root_agent = Agent(
    name="RootAgent",
    model=AGENT_MODEL, # Can be a string for Gemini or a LiteLlm object
    description="Provides math problem-solving assistance.",
    instruction="You are a helpful math assistant. "
                "When the user asks for help with a math problem, "
                "use the solve_and_animate tool to find the solution and generate an animation plan and Blender code. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the solution, animation plan, and Blender code clearly.",
    tools=[
        solve_and_animate_tool,
        solve_algebra_problem_tool,
        solve_geometry_problem_tool,
        solve_calculus_problem_tool,
        solve_trigonometry_problem_tool,
        solve_linear_algebra_problem_tool,
        solve_statistics_problem_tool,
        solve_probability_problem_tool,
        animation_tool_generator,
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
    query = "Find the area of a triangle with base 10 cm and height 12 cm"
    print(f"User Query: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    # The runner's run method handles the async loop internally
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    final_response = None
    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response:", final_response)

# Standard way to run the main async function
# if __name__ == "__main__":
#     # asyncio.run(main())
#     main()

if __name__ == "__main__":
    # Just call main() normally
    asyncio.get_event_loop().run_until_complete(main())


# print(f"Agent '{root_agent.name}' created using model '{AGENT_MODEL}'.")