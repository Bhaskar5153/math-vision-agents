

# @title Import necessary libraries
import os
import asyncio
from google import genai
from google.adk.tools import FunctionTool
from google.adk.tools import ToolContext




import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

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
            "max_output_tokens": 4000,
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
            "max_output_tokens": 4000,
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
            "max_output_tokens": 4000,
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
            "max_output_tokens": 4000,
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
            "max_output_tokens": 4000,
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
            "max_output_tokens": 4000,
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
            "max_output_tokens": 4000,
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
