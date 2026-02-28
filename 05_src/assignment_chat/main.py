import gradio as gr
from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

from prompts import return_instructions
from tools_api import get_joke
from tools_semantic import semantic_faq_search

# load_dotenv(".env")
# load_dotenv("../.secrets")

# if not os.environ.get("OPENAI_API_KEY"):
#     raise ValueError("Missing OPENAI_API_KEY environment variable")


# Use Ollama (local model) due to quota limits on OpenAI API key
chat_model = init_chat_model("ollama:llama3")

instructions = return_instructions()

def call_model(state: MessagesState):
    messages = state["messages"]

    if len(messages) > 20:
        messages = messages[-20:]

    last_message = messages[-1].content.lower()

    # ---- Manual Tool Routing (safer for Ollama) ----
    if "joke" in last_message:
        return {"messages": [AIMessage(content=get_joke.invoke({}))]}

    if "library" in last_message or "password" in last_message:
        return {
            "messages": [
                AIMessage(
                    content=semantic_faq_search.invoke({"query": last_message})
                )
            ]
        }

    # ---- Otherwise use model ----
    response = chat_model.invoke(
        [SystemMessage(content=instructions)] + messages
    )

    return {"messages": [response]}


def get_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_edge(START, "call_model")
    return builder.compile()


graph = get_graph()


def chat(message: str, history: list):
    langchain_messages = []

    for msg in history:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            langchain_messages.append(AIMessage(content=msg["content"]))

    langchain_messages.append(HumanMessage(content=message))

    result = graph.invoke({"messages": langchain_messages})

    return result["messages"][-1].content


gr.ChatInterface(fn=chat).launch()