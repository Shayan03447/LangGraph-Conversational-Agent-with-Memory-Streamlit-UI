from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
import os


checkpoint=InMemorySaver()
load_dotenv()

model=ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=os.getenv('OPENAI_API_KEY'))

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    messages=state['messages']
    response=model.invoke(messages)
    return {'messages':[response]}
#Node 
graph=StateGraph(ChatState)

#Adding node
graph.add_node('chat_node', chat_node)

#Adding edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

#Compiling the graph
chatbot=graph.compile(checkpointer=checkpoint)





