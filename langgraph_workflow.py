from typing import TypedDict
from langgraph.graph import StateGraph, END
from intent_identifier_agent import identify_intent
from response_generator_agent import generate_response
from functions import retrieve_context

class AgenticAiState(TypedDict):
    user_input: str
    intent_agent_output: str
    rag_docs: str
    rag_context: str
    final_output: str


def intent_agent(state: AgenticAiState):
    user_query = state["user_input"]
    state["intent_agent_output"] = identify_intent(user_query)
    return state


def benefits_policy(state: AgenticAiState):
    user_query = state["user_input"]
    docs, context = retrieve_context(r".\vectorDBs\benefits_policy", user_query)
    state["rag_docs"] = docs
    state["rag_context"] = context
    return state


def travel_policy(state: AgenticAiState):
    user_query = state["user_input"]
    docs, context = retrieve_context(r".\vectorDBs\travel_policy", user_query)
    state["rag_docs"] = docs
    state["rag_context"] = context
    return state


def employee_handbook(state: AgenticAiState):
    user_query = state["user_input"]
    docs, context = retrieve_context(r".\vectorDBs\employee_handbook", user_query)
    state["rag_docs"] = docs
    state["rag_context"] = context
    return state


def response_generator(state: AgenticAiState):
    if state["intent_agent_output"]=="extra":
        state["final_output"] = "I can not answer as this is out of the context"
        
    else:
        user_query = state["user_input"]
        context = state["rag_context"]
        state["final_output"] = generate_response(user_query, context)
    return state


def router(state: AgenticAiState):
    return state["intent_agent_output"]


# Build graph
builder = StateGraph(AgenticAiState)


# Add nodes
builder.add_node("intent_identifier_agent", intent_agent)
builder.add_node("benefits_policy_fetcher", benefits_policy)
builder.add_node("employee_handbook_fetcher", employee_handbook)
builder.add_node("travel_policy_fetcher", travel_policy)
builder.add_node("response_generator_agent", response_generator)


# Work Flow
builder.set_entry_point("intent_identifier_agent")

builder.add_conditional_edges(
    "intent_identifier_agent",
    router,
    {
        "extra": "response_generator_agent",
        "benefits_policy": "benefits_policy_fetcher",
        "employee_handbook": "employee_handbook_fetcher",
        "travel_policy": "travel_policy_fetcher"
    },
)

builder.add_edge("benefits_policy_fetcher", "response_generator_agent")
builder.add_edge("employee_handbook_fetcher", "response_generator_agent")
builder.add_edge("travel_policy_fetcher", "response_generator_agent")
builder.add_edge("response_generator_agent", END)

# Compile graph
graph = builder.compile()



with open("workflow.txt", "w", encoding="utf-8") as f:
    print(graph.get_graph().draw_ascii(), file=f)

if __name__=="__main__":
    # Run workflow
    result = graph.invoke(
        {
            "user_input": "Tell me about the meal allowance"
        }
    )

    print(result["final_output"])