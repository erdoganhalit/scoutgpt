from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from neo4j import GraphDatabase

from neo4j import GraphDatabase
from datetime import datetime

from chat.prompts.find import FIND_CYPHER_PROMPT_W_CONTEXT, FIND_QA_PROMPT

question = "How did Haaland perform in Premier League in 23/24 season"

# Initialize the Neo4j driver
uri = "neo4j+s://d1c92482.databases.neo4j.io"
username = "neo4j"
password = "H3mFJDVvmjPz1s5aDFi46XN8JFLGuYitPy6weie8stk"
driver = GraphDatabase.driver(uri, auth=(username, password))

graph = Neo4jGraph(url=uri, username="neo4j", password=password)

question = "Find fast left back players from top 5 league worth around 10 million aged between 20-28"

find_cypher_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model="gpt-4o"),
    prompt=FIND_CYPHER_PROMPT_W_CONTEXT
)

find_cypher_response = find_cypher_chain.invoke(
    {
        "schema": graph.schema,
        "question": question
    }
)

find_cypher = find_cypher_response['text']

for code_block in ["```cypher", "```json", "```"]:
    if code_block in find_cypher:
        analysis_cypher = find_cypher.replace(code_block, "")

find_context = graph.query(find_cypher)

find_qa_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model='gpt-4o'),
    prompt=FIND_QA_PROMPT
)

find_qa_response = find_qa_chain.invoke(
    {
        "context": find_qa_chain,
        "question": question
    }
)

print(find_qa_response['text'])