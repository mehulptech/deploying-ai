import gradio as gr
from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import os

from prompts import return_instructions


load_dotenv(".env")
load_dotenv("../.secrets")

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("Missing OPENAI_API_KEY")


chat_model = init_chat_model("openai:gpt-4o-mini")

instructions = return_instructions()


def call_model(state: MessagesState):
    messages = state["messages"]

    # simple memory trimming
    if len(messages) > 20:
        messages = messages[-20:]

    response = chat_model.invoke(
        [SystemMessage(content=instructions)] + messages
    )

    return {"messages": [response]}


def get_graph():
    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_edge(START, "call_model")
    return builder.compile()


graph = get_graph()


def chat(message, history):
    result = graph.invoke({
        "messages": history + [{"role": "user", "content": message}]
    })

    return result["messages"][-1].content


gr.ChatInterface(fn=chat).launch()