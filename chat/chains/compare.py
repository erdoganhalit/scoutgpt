from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from neo4j import GraphDatabase

from neo4j import GraphDatabase
from datetime import datetime
import ast

from chat.prompts.compare import COMPARISON_CYPHER_PROMPT_W_CONTEXT, COMPARISON_QA_PROMPT

question = "Compare Haaland and Mbappe performances in UEFA Champions League in 23/24 season"

# Initialize the Neo4j driver
uri = "neo4j+s://d1c92482.databases.neo4j.io"
username = "neo4j"
password = "H3mFJDVvmjPz1s5aDFi46XN8JFLGuYitPy6weie8stk"
driver = GraphDatabase.driver(uri, auth=(username, password))

graph = Neo4jGraph(url=uri, username="neo4j", password=password)

comparison_cypher_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model="gpt-4o"),
    prompt=COMPARISON_CYPHER_PROMPT_W_CONTEXT
)

comparison_cypher_response = comparison_cypher_chain.invoke(
    {
        "schema": graph.schema,
        "question": question
    }
)

comparison_cypher = comparison_cypher_response['text']

for code_block in ["```cypher", "```json", "```"]:
    if code_block in comparison_cypher:
        analysis_cypher = comparison_cypher.replace(code_block, "")

comparison_cypher_list = ast.literal_eval(comparison_cypher_response['text'])

comparison_context = [graph.query(cypher_query) for cypher_query in comparison_cypher_list]

comparison_qa_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model='gpt-4o'),
    prompt=COMPARISON_QA_PROMPT
)

comparison_qa_response = comparison_qa_chain.invoke(
    {
        "context": comparison_context,
        "question": question
    }
)

print(comparison_qa_response['text'])