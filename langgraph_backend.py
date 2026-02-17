from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
model = ChatOpenAI()
class ChatSchema(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatSchema):
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages':[response]}



graph = StateGraph(ChatSchema, checkpointer=InMemorySaver())
graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile()





