from dexa.graph.state import DexaState
from dexa.agents.intent.agent import IntentAgent
from dexa.agents.planner.agent import PlannerAgent
from dexa.agents.execution.agent import ExecutionAgent
from dexa.agents.reasoning.agent import ReasoningAgent
from dexa.agents.response.agent import ResponseAgent
from dexa.agents.profiler.agent import ProfilerAgent
from dexa.agents.visualization.agent import VisualizationAgent
from dexa.agents.reflection.agent import ReflectionAgent
from dexa.agents.goal.agent import GoalAgent

from dexa.execution.executor import Executor


intent_agent = IntentAgent()
goal_agent = GoalAgent()
planner_agent = PlannerAgent()
execution_agent = ExecutionAgent()
reflection_agent = ReflectionAgent()
reasoning_agent = ReasoningAgent()
response_agent = ResponseAgent()
profiler_agent = ProfilerAgent()
visualization_agent = VisualizationAgent()

executor = Executor()


from dexa.execution.data_store import get_data, set_data

def extract_json(text: str):
    import json
    
    # Clean text
    text = text.strip()
    
    # Try fully formed markdown block
    if "```json" in text:
        block = text.split("```json")[1].split("```")[0].strip()
        try: return json.loads(block)
        except: pass
    elif "```" in text:
        block = text.split("```")[1].split("```")[0].strip()
        try: return json.loads(block)
        except: pass
        
    # Try finding the outermost brackets if no markdown
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except:
            pass
            
    return None

# -------------------------
# PROFILER NODE
# -------------------------
def profiler_node(state: DexaState):
    profile = profiler_agent.run(get_data())
    return {"data_profile": profile}


# -------------------------
# PLANNING NODE (Consolidated)
# -------------------------
def planning_node(state: DexaState):
    # Combine Intent, Goal, and Planner into one call
    query = state["query"]
    history = state.get("history", [])[-10:]
    profile = state.get("data_profile", {})
    
    prompt = f"""
    You are the central brain of Dexa AI.
    User Query: {query}
    Session History: {history}
    Data Profile: {profile}

    1. Classify intent (analyze, visualize, train_model, diagnose).
    2. Detect if there is a specific Machine Learning Goal.
    3. Create a concise execution plan (max 3 steps).

    Output Format:
    INTENT: <intent>
    GOAL: <yes/no>
    PLAN:
    - step 1
    - step 2
    """
    
    from dexa.llm.abstraction import chat
    result = chat(prompt)
    
    try:
        lines = [l.strip() for l in result.split("\n") if ":" in l or l.strip().startswith("-")]
        intent = "analyze"
        goal = "no"
        plan = []
        
        current_section = None
        for line in result.split("\n"):
            line = line.strip()
            if not line: continue
            
            if line.upper().startswith("INTENT:"):
                intent = line.split(":")[1].strip().lower()
            elif line.upper().startswith("GOAL:"):
                goal = line.split(":")[1].strip().lower()
            elif line.upper().startswith("PLAN:"):
                current_section = "PLAN"
                # Check if there's content on the same line after PLAN:
                parts = line.split(":", 1)
                if len(parts) > 1 and parts[1].strip():
                    plan.append(parts[1].strip().lstrip("- 123. "))
            elif current_section == "PLAN":
                # Clean the line and add to plan if it looks like a step
                step = line.lstrip("- 123. ").strip()
                if step:
                    plan.append(step)

        if goal == "yes" or intent == "goal":
            intent = "goal"
            
        if not plan:
            plan = ["summarise the data"]

        return {
            "intent": intent,
            "goal": goal,
            "plan": plan[:3], # strictly max 3 steps for speed
            "current_step": 0
        }
    except Exception as e:
        return {"intent": "analyze", "plan": ["describe the data"], "current_step": 0}


# -------------------------
# EXECUTION & REFLECTION NODE (Consolidated)
# -------------------------
def execution_node(state: DexaState):
    import hashlib
    query_str = state.get("query", "")
    query_id = hashlib.md5(query_str.encode()).hexdigest()[:8] if query_str else "plot"
    
    # Get current step
    plan = state.get("plan", [])
    idx = state.get("current_step", 0)
    if idx >= len(plan):
        return {"decision": "stop"}
        
    step = plan[idx]
    
    # Run execution
    execution_result = execution_agent.run(
        query=state["query"], 
        plan=step,
        history=state.get("history", [])[-10:],
        data_profile=state.get("data_profile", {})
    )
    
    res = extract_json(execution_result)
    output = ""
    try:
        if res and res.get("type") == "tool":
            from dexa.execution.tools.registry import TOOLS
            tool_name = res.get("tool_name")
            args = res.get("args", {})
            if tool_name in TOOLS:
                tool_result = TOOLS[tool_name].run(df=get_data(), query_id=query_id, **args)
                output = tool_result.get("summary", "Tool executed successfully.")
                if tool_result.get("df") is not None:
                    set_data(tool_result["df"])
            else:
                output = f"Tool {tool_name} not found."
        elif res and res.get("type") == "code":
            context = {
                "df": get_data(),
                "data_profile": state.get("data_profile", {}),
                "query_id": query_id
            }
            output = executor.run(res.get("code", ""), context)
            if context.get("df") is not None:
                set_data(context["df"])
        else:
            output = f"Invalid format: {execution_result}"
    except Exception as e:
        output = f"Error: {str(e)}"

    # Implicit reflection to save time
    # If it's the last step or successful, continue to next or stop
    new_history_item = [{
        "step": step,
        "output": output,
        "reflection": {"decision": "continue", "confidence": 1.0}
    }]
    
    return {
        "step_output": output,
        "history": new_history_item,
        "current_step": idx + 1,
        "decision": "continue" if idx + 1 < len(plan) else "stop"
    }


# -------------------------
# FINAL RESPONSE NODE (Consolidated)
# -------------------------
def response_node(state: DexaState):
    # Combine Reasoning and Response
    history = state.get("history", [])[-10:]
    query = state.get("query", "")
    data_profile = state.get("data_profile", {})
    
    final_response = response_agent.run(query=query, reasoning=str(history), data_profile=data_profile)
    return {"final_response": final_response}