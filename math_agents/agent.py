from google.adk.agents.llm_agent import Agent
from google.adk.agents import LlmAgent, BaseAgent
from google.genai import types
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator, Dict
import logging
import json
from pydantic import Field
from .prompts import PROMPTS
import os
import datetime

TEMPERATURE = 0.2

# --- Math Domain Agents ---
algebra_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='algebra_agent',
    generate_content_config=types.GenerateContentConfig(
        temperature=TEMPERATURE,
        seed=42,
    ),
    description='Solve equations, graph functions, and explore algebraic relationships in stunning 3D.',
    instruction=PROMPTS['algebra_agent']['instruction'],
)

geometry_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='geometry_agent',
    generate_content_config=types.GenerateContentConfig(
        temperature=TEMPERATURE,
        seed=42,
    ),
    description='Explore shapes, calculate areas and volumes, and visualize geometric transformations.',
    instruction=PROMPTS['geometry_agent']['instruction'],
)

calculus_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='calculus_agent',
    generate_content_config=types.GenerateContentConfig(
        temperature=TEMPERATURE,
        seed=42,
    ),
    description='Understand derivatives, integrals, and limits through dynamic visualizations.',
    instruction=PROMPTS['calculus_agent']['instruction'],
)

trigonometry_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='trigonometry_agent',
    generate_content_config=types.GenerateContentConfig(
        temperature=TEMPERATURE,
        seed=42,
    ),
    description='Master sine, cosine, tangent and their relationships.',
    instruction=PROMPTS['trigonometry_agent']['instruction'],
)

linear_algebra_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='linear_algebra_agent',
    generate_content_config=types.GenerateContentConfig(
        temperature=TEMPERATURE,
        seed=42,
    ),
    description='Visualize vectors, matrices, and linear transformations.',
    instruction=PROMPTS['linear_algebra_agent']['instruction'],
)

statistics_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='statistics_agent',
    generate_content_config=types.GenerateContentConfig(
        temperature=TEMPERATURE,
        seed=42,
    ),
    description='Understand probability distributions, data analysis, and statistical visualizations.',
    instruction=PROMPTS['statistics_agent']['instruction'],
)

# --- SupervisorAgent ---
class SupervisorAgent(BaseAgent):
    """
    Routes user questions to the selected math domain agent.
    """
    agents: Dict[str, LlmAgent] = Field(default_factory=dict)

    def __init__(self, name: str):
        super().__init__(name=name)
        object.__setattr__(self, 'agents', {
            'algebra_agent': algebra_agent,
            'geometry_agent': geometry_agent,
            'calculus_agent': calculus_agent,
            'trigonometry_agent': trigonometry_agent,
            'linear_algebra_agent': linear_algebra_agent,
            'statistics_agent': statistics_agent,
        })

    def get_greeting(self):
        return ("Hello! I can help you solve math problems across algebra, geometry, calculus, trigonometry, linear algebra, and statistics, "
                "and visualize solutions in 3D. Just type your question, and I will select the right math expert for you!")

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        logging.info(f"{self.name} Starting task workflow...")
        if (
            not ctx.user_content
            or not ctx.user_content.parts
            or len(ctx.user_content.parts) == 0
            or not ctx.user_content.parts[0].text
        ):
            logging.error(f"[{self.name}] No agent name or tool found in the user content. Aborting the workflow.")
            return
        first_message_text = ctx.user_content.parts[0].text
        try:
            task_selection_state = json.loads(first_message_text)
            selected_agent = task_selection_state.get("selected_agent")
            user_question = task_selection_state.get("user_question", "")
            agent = self.agents.get(selected_agent)
            if agent:
                ctx.user_content = types.Content(
                    parts=[types.Part(text=user_question)]
                )
                # Run the agent and collect the response
                response = ""
                async for event in agent.run_async(ctx):
                    if hasattr(event, 'text') and event.text:
                        response += event.text
                    yield event
                # Parse response for animation plan and Blender code
                if '---Animation Plan---' in response and '---Blender Code---' in response:
                    plan = response.split('---Animation Plan---')[1].split('---Blender Code---')[0].strip()
                    code = response.split('---Blender Code---')[1].strip()
                    summary = user_question[:20]
                    anim_path = save_animation_script(summary, plan)
                    blend_path = save_blender_script(summary, code)
                    logging.info(f"Saved animation script: {anim_path}")
                    logging.info(f"Saved Blender script: {blend_path}")
            else:
                logging.error(f"[{self.name}] Unknown agent selected: {selected_agent}. Aborting.")
        except Exception as e:
            logging.error(f"[{self.name}] Error parsing input or running agent: {e}. Trying keyword-based agent selection.")
            # Fallback: keyword-based agent selection for plain text
            question_lower = first_message_text.lower()
            if any(word in question_lower for word in ["derivative", "integral", "limit", "calculus"]):
                agent = self.agents.get('calculus_agent')
            elif any(word in question_lower for word in ["triangle", "circle", "geometry", "angle", "polygon"]):
                agent = self.agents.get('geometry_agent')
            elif any(word in question_lower for word in ["sine", "cosine", "tangent", "trigonometry"]):
                agent = self.agents.get('trigonometry_agent')
            elif any(word in question_lower for word in ["vector", "matrix", "linear algebra"]):
                agent = self.agents.get('linear_algebra_agent')
            elif any(word in question_lower for word in ["probability", "statistics", "mean", "median", "mode"]):
                agent = self.agents.get('statistics_agent')
            else:
                agent = self.agents.get('algebra_agent')
            ctx.user_content = types.Content(
                parts=[types.Part(text=first_message_text)]
            )
            if agent:
                async for event in agent.run_async(ctx):
                    yield event
            else:
                logging.error(f"[{self.name}] No suitable agent found for input. Asking user to specify domain.")
                # Respond with a message asking for domain selection
                yield Event.text("I couldn't determine the math domain for your question. Please specify the domain (e.g., Algebra, Geometry, Calculus, Trigonometry, Linear Algebra, Statistics) or select an agent in the UI.")
        finally:
            logging.info(f"[{self.name}] Task workflow completed.")

def save_animation_script(summary: str, content: str) -> str:
    os.makedirs('animation_scripts', exist_ok=True)
    base = "_".join(summary.lower().split())[:20]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base}_{timestamp}.md"
    filepath = os.path.join('animation_scripts', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

def save_blender_script(summary: str, content: str) -> str:
    os.makedirs('blender_scripts', exist_ok=True)
    base = "_".join(summary.lower().split())[:20]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base}_{timestamp}.py"
    filepath = os.path.join('blender_scripts', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

def read_animation_script(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# --- ADK root agent ---
root_agent = SupervisorAgent(name="SupervisorAgent")
