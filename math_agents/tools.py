# @title Import necessary libraries
import os
import asyncio
from google import genai
from google.adk.tools import FunctionTool
from google.adk.tools import ToolContext



from math_agents.animation_agent import AnimationDirector
from google.adk.agents.invocation_context import InvocationContext

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.agents.invocation_context import InvocationContext

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment. Please set it in your .env file.")

logging.info("GOOGLE_API_KEY loaded: %s", os.getenv("GOOGLE_API_KEY"))

print("Libraries imported.")

# @title Define the tool function to solve algebra problems and provide solution steps.
def solve_algebra_problem(problem: str, tool_context: ToolContext) -> dict:
    """Solves an algebra problem and provides step-by-step solution.

    Args:
        problem (str): The algebra problem to solve (e.g., "2x + 2 = 4", "5x - 3 = 12").

    Returns:
        dict: A dictionary containing the solution steps and final answer.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'steps' key with solution steps.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: solve_algebra_problem called for problem: {problem} ---") # Log tool execution

    # make the call to genai to solve the algebra problem.
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"solve the algebra problem '{problem}' and explain step by step",
        config={
            "max_output_tokens": 10000,
            "temperature": 0.2,
            "top_p": 0.8,
        }
    )
    # add question and answer to the tool context state
    tool_context.state["last_algebra_problem"] = problem
    tool_context.state["last_algebra_answer"] = response.text

    if response:
        return {"status": "success", "steps": response.text, "answer": response.text}
    else:
        return {"status": "error", "error_message": f"Sorry, I couldn't solve the problem '{problem}'."}

# # Example tool usage (optional test)
# print(solve_algebra_problem("2x + 2 = 4"))
# print(solve_algebra_problem("5x - 3 = 12"))
# print(solve_algebra_problem("10 - 4x = 6"))


def solve_geometry_problem(problem: str, tool_context: ToolContext) -> dict:
    """Solves a geometry problem and provides step-by-step solution.

    Args:
        problem (str): The geometry problem to solve (e.g., "Area of circle with radius 3", "Volume of cube with side 4").

    Returns:
        dict: A dictionary containing the solution steps and final answer.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'steps' key with solution steps.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: solve_geometry_problem called for problem: {problem} ---") # Log tool execution

    # Mock geometry problem solving
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"solve the geometry problem '{problem}' and explain step by step",
        config={
            "max_output_tokens": 10000,
            "temperature": 0.2,
            "top_p": 0.8,
        }
    )

    tool_context.state["last_geometry_problem"] = problem
    tool_context.state["last_geometry_answer"] = response.text

    if response:
        return {"status": "success", "steps": response.text, "answer": response.text}
    else:
        return {"status": "error", "error_message": f"Sorry, I couldn't solve the problem '{problem}'."}
    


def solve_calculus_problem(problem: str, tool_context: ToolContext) -> dict:
    """Solves a calculus problem and provides step-by-step solution.

    Args:
        problem (str): The calculus problem to solve (e.g., "Derivative of x^2", "Integral of 2x").

    Returns:
        dict: A dictionary containing the solution steps and final answer.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'steps' key with solution steps.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: solve_calculus_problem called for problem: {problem} ---") # Log tool execution

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"solve the calculus problem '{problem}' and explain step by step",
        config={
            "max_output_tokens": 10000,
            "temperature": 0.2,
            "top_p": 0.8,
        }
    )
    tool_context.state["last_calculus_problem"] = problem
    tool_context.state["last_calculus_answer"] = response.text

    if response:
        return {"status": "success", "steps": response.text, "answer": response.text}
    else:
        return {"status": "error", "error_message": f"Sorry, I couldn't solve the problem '{problem}'."}
    

def solve_trigonometry_problem(problem: str, tool_context: ToolContext) -> dict:
    """Solves a trigonometry problem and provides step-by-step solution.

    Args:
        problem (str): The trigonometry problem to solve (e.g., "sin(30 degrees)", "cos(60 degrees)").

    Returns:
        dict: A dictionary containing the solution steps and final answer.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'steps' key with solution steps.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: solve_trigonometry_problem called for problem: {problem} ---") # Log tool execution

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"solve the trigonometry problem '{problem}' and explain step by step",
        config={
            "max_output_tokens": 10000,
            "temperature": 0.2,
            "top_p": 0.8,
        }
    )
    tool_context.state["last_trigonometry_problem"] = problem
    tool_context.state["last_trigonometry_answer"] = response.text

    if response:
        return {"status": "success", "steps": response.text, "answer": response.text}
    else:
        return {"status": "error", "error_message": f"Sorry, I couldn't solve the problem '{problem}'."}
    


def solve_linear_algebra_problem(problem: str, tool_context: ToolContext) -> dict:
    """Solves a linear algebra problem and provides step-by-step solution.

    Args:
        problem (str): The linear algebra problem to solve (e.g., "Solve 2x + 3y = 6 and x - y = 2").

    Returns:
        dict: A dictionary containing the solution steps and final answer.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'steps' key with solution steps.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: solve_linear_algebra_problem called for problem: {problem} ---") # Log tool execution

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"solve the algebra problem '{problem}' and explain step by step",
        config={
            "max_output_tokens": 10000,
            "temperature": 0.2,
            "top_p": 0.8,
        }
    )
    tool_context.state["last_linear_algebra_problem"] = problem
    tool_context.state["last_linear_algebra_answer"] = response.text


    if response:
        return {"status": "success", "steps": response.text, "answer": response.text}
    else:
        return {"status": "error", "error_message": f"Sorry, I couldn't solve the problem '{problem}'."}
    

def solve_statistics_problem(problem: str, tool_context: ToolContext) -> dict:
    """Solves a statistics problem and provides step-by-step solution.

    Args:
        problem (str): The statistics problem to solve (e.g., "Mean of [2, 4, 6, 8]", "Standard deviation of [1, 3, 5, 7]").

    Returns:
        dict: A dictionary containing the solution steps and final answer.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'steps' key with solution steps.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: solve_statistics_problem called for problem: {problem} ---") # Log tool execution

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"solve the statistics problem '{problem}' and explain step by step",
        config={
            "max_output_tokens": 10000,
            "temperature": 0.2,
            "top_p": 0.8,
        }
    )
    tool_context.state["last_statistics_problem"] = problem
    tool_context.state["last_statistics_answer"] = response.text

    if response:
        return {"status": "success", "steps": response.text, "answer": response.text}
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have a solution for '{problem}'."}
    

def solve_probability_problem(problem: str, tool_context: ToolContext) -> dict:
    """Solves a probability problem and provides step-by-step solution.

    Args:
        problem (str): The probability problem to solve (e.g., "Probability of rolling a 3 on a fair six-sided die").

    Returns:
        dict: A dictionary containing the solution steps and final answer.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'steps' key with solution steps.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: solve_probability_problem called for problem: {problem} ---") # Log tool execution

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"solve the probability problem '{problem}' and explain step by step",
        config={
            "max_output_tokens": 10000,
            "temperature": 0.2,
            "top_p": 0.8,
        }
    )
    tool_context.state["last_probability_problem"] = problem
    tool_context.state["last_probability_answer"] = response.text

    if response:
        return {"status": "success", "steps": response.text, "answer": response.text}
    else:
        return {"status": "error", "error_message": f"Sorry, I couldn't solve the problem '{problem}'."}
    



from google.adk.runners import RunConfig

run_config = RunConfig(response_modalities=None)








# async def animation_tool(solution: str, question_summary: str, tool_context=None) -> dict:
#     import logging
#     logging.info('[AnimationTool] Called with solution: %s, question: %s', solution, question_summary)
    
#     from google.adk.agents import LlmAgent, SequentialAgent

#     # Create agents for the main workflow
#     local_story_generator = LlmAgent(
#         name="StoryGenerator",
#         model="gemini-2.5-flash",
#         instruction="You are a story writer. Write a short story (around 100 words), on the following topic: {topic}",
#         input_schema=None,
#         output_key="current_story",
#     )
#     local_critic = LlmAgent(
#         name="Critic",
#         model="gemini-2.5-flash",
#         instruction="You are a story critic. Review the story provided: {{current_story}}. Provide 1-2 sentences of constructive criticism on how to improve it. Focus on plot or character.",
#         input_schema=None,
#         output_key="criticism",
#     )
#     local_reviser = LlmAgent(
#         name="Reviser",
#         model="gemini-2.5-flash",
#         instruction="You are a story reviser. Revise the story provided: {{current_story}}, based on the criticism in {{criticism}}. Output only the revised story.",
#         input_schema=None,
#         output_key="current_story",
#     )
#     local_grammar_check = LlmAgent(
#         name="GrammarCheck",
#         model="gemini-2.5-flash",
#         instruction="You are a grammar checker. Check the grammar of the story provided: {current_story}. Output only the suggested corrections as a list, or output 'Grammar is good!' if there are no errors.",
#         input_schema=None,
#         output_key="grammar_suggestions",
#     )
#     local_tone_check = LlmAgent(
#         name="ToneCheck",
#         model="gemini-2.5-flash",
#         instruction="You are a tone analyzer. Analyze the tone of the story provided: {current_story}. Output only one word: 'positive' if the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral' otherwise.",
#         input_schema=None,
#         output_key="tone_check_result",
#     )
#     local_animation_generator = LlmAgent(
#         name="AnimationGenerator",
#         model="gemini-2.5-flash",
#         instruction="You are an animation expert. Given a math solution and a creative animation idea, generate a detailed animation plan in markdown format, and then generate Blender 4.4.3 compatible Python code for the animation as described in the plan. Output the plan as 'animation_plan:' and the code as 'blender_code:' in your response.",
#         input_schema=None,
#         output_key="animation_output"  # Store both plan and code in a single key
#     )

#     # Remove creation of critic_reviser_sequence and only pass individual agents to AnimationDirector
#     animation_director = AnimationDirector(
#         name="AnimationDirector",
#         story_generator=local_story_generator,
#         critic=local_critic,
#         reviser=local_reviser,
#         grammar_check=local_grammar_check,
#         tone_check=local_tone_check,
#         animation_generator=local_animation_generator
#     )

#     from google.adk.sessions import InMemorySessionService

#     session_service = InMemorySessionService()
#     # Fix: Await the coroutine to get the session object
#     import asyncio
#     session = await session_service.create_session(app_name="Math_Vision_Animation", user_id="user1234", session_id="1234")
#     # session = asyncio.get_event_loop().run_until_complete(
#     #     session_service.create_session(app_name="Math_Vision_Animation", user_id="user1234", session_id="1234")
#     # )
#     session.state["current_story"] = question_summary
#     session.state["topic"] = solution
#     session.state["criticism"] = ""  # Ensure criticism key exists for Reviser

#     ctx = InvocationContext(
#         session_service=session_service,
#         invocation_id="animation_tool_invocation",
#         agent=animation_director,
#         session=session,
#         run_config=run_config
#     )

#     async def run_animation_director(agent, ctx):
#         events = []
#         async for event in agent._run_async_impl(ctx):
#             events.append(event)
#         return events

#     # events = asyncio.get_event_loop().run_until_complete(run_animation_director(animation_director, ctx))
#     events = await run_animation_director(animation_director, ctx)
#     # Extract both plan and code from the output
#     animation_output = ctx.session.state.get("animation_output", "")
#     plan = None
#     code = None
#     if animation_output:
#         # Simple parsing: look for 'animation_plan:' and 'blender_code:'
#         import re
#         plan_match = re.search(r"animation_plan:(.*?)(blender_code:|$)", animation_output, re.DOTALL)
#         code_match = re.search(r"blender_code:(.*)", animation_output, re.DOTALL)
#         if plan_match:
#             plan = plan_match.group(1).strip()
#         if code_match:
#             code = code_match.group(1).strip()
#     logging.info('[AnimationTool] Animation plan: %s', plan)
#     logging.info('[AnimationTool] Blender code: %s', code)
#     return {"animation_plan": plan, "blender_code": code}


async def animation_tool(solution: str, question_summary: str, tool_context=None) -> dict:
    import logging
    logging.info('[AnimationTool] Called with solution: %s, question: %s', solution, question_summary)

    

    local_animation_generator = LlmAgent(
        name="AnimationGenerator",
        model="gemini-2.5-flash",
        instruction=(
            "You are an animation expert. Given a math problem and its solution, "
            "generate a detailed animation plan in markdown format, and then generate "
            "Blender 4.4.3 compatible Python code for the animation as described in the plan. "
            "Output the plan as 'animation_plan:' and the code as 'blender_code:' in your response."
        ),
        input_schema=None,
        output_key="animation_output"
    )

    animation_director = AnimationDirector(
        name="AnimationDirector",
        animation_generator=local_animation_generator
    )

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="Math_Vision_Animation", user_id="user1234", session_id="1234"
    )
    session.state["problem"] = question_summary
    session.state["solution"] = solution

    ctx = InvocationContext(
        session_service=session_service,
        invocation_id="animation_tool_invocation",
        agent=animation_director,
        session=session,
        run_config=run_config
    )

    events = []
    async for event in animation_director._run_async_impl(ctx):
        events.append(event)

    animation_output = ctx.session.state.get("animation_output", "")
    plan, code = None, None
    if animation_output:
        if "animation_plan:" in animation_output:
            plan = animation_output.split("animation_plan:")[1].split("blender_code:")[0].strip()
        if "blender_code:" in animation_output:
            code = animation_output.split("blender_code:")[1].strip()

    logging.info('[AnimationTool] Animation plan: %s', plan)
    logging.info('[AnimationTool] Blender code: %s', code)
    return {"animation_plan": plan, "blender_code": code}




