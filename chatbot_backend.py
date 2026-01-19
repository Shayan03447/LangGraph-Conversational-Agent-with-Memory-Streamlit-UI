from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
import os

load_dotenv()
model=ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=os.getenv('OPENAI_API_KEY'))

#----------------------------State--------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#---------------------------Node----------------
def chat_node(state: ChatState):
    messages=state['messages']
    response=model.invoke(messages)
    return {'messages':[response]}

#---------------------------Graph----------------
graph=StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

#---------------------------Checkpoint----------------
checkpoint=InMemorySaver()

#---------------------------Compile----------------
chatbot=graph.compile(checkpointer=checkpoint)