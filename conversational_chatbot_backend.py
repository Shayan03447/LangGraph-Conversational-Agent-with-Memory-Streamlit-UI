from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
import os
from langchain_openai import ChatOpenAI

load_dotenv()
model=ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7)

#-------------------------State Graph--------------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#-------------------------Nodes--------------------------
def chat_node(state: ChatState):
    message=state['messages']
    response=model.invoke(message)
    return {'messages': [response]}

#-------------------------Graph--------------------------
graph=StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

#-------------------------Checkpoint--------------------------
checkpoint=InMemorySaver()

#---------------------------Compile---------------------------
chatbot=graph.compile(checkpointer=checkpoint)