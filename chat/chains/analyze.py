from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from neo4j import GraphDatabase

from neo4j import GraphDatabase
from datetime import datetime

from chat.prompts.analyze import ANALYSIS_CYPHER_PROMPT_W_CONTEXT, ANALYSIS_QA_PROMPT

question = "How did Haaland perform in Premier League in 23/24 season"

# Initialize the Neo4j driver
uri = "neo4j+s://d1c92482.databases.neo4j.io"
username = "neo4j"
password = "H3mFJDVvmjPz1s5aDFi46XN8JFLGuYitPy6weie8stk"
driver = GraphDatabase.driver(uri, auth=(username, password))

graph = Neo4jGraph(url=uri, username="neo4j", password=password)

analysis_cypher_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model="gpt-4o"),
    prompt=ANALYSIS_CYPHER_PROMPT_W_CONTEXT
)

analysis_cypher_response = analysis_cypher_chain.invoke(
    {
        "schema": graph.schema,
        "question": question
    }
)

analysis_cypher = analysis_cypher_response['text']

for code_block in ["```cypher", "```json", "```"]:
    if code_block in analysis_cypher:
        analysis_cypher = analysis_cypher.replace(code_block, "")

analysis_context = graph.query(analysis_cypher)

analysis_qa_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model='gpt-4o'),
    prompt=ANALYSIS_QA_PROMPT
)

analysis_qa_response = analysis_qa_chain.invoke(
    {
        "context": analysis_context,
        "question": question
    }
)

print(analysis_qa_response['text'])