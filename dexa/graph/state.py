from typing import TypedDict, List, Dict, Any, Optional, Annotated
import operator

class DexaState(TypedDict, total=False):
    # Input
    query: str

    # Understanding
    intent: str
    goal: str

    # Planning
    plan: List[str]
    current_step: int

    # Execution
    step_input: str
    step_output: Any

    # Tracking
    history: Annotated[List[Dict[str, Any]], operator.add]  # step + output + reflection

    # Reflection
    reflection: Dict[str, Any]
    decision: str  # continue | replan | stop

    # Output
    final_reasoning: str
    final_response: str
    data_profile: Dict[str, Any]