import streamlit as st
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from neo4j import GraphDatabase
import ast
from langchain.prompts import PromptTemplate
import tiktoken

# Import prompt templates
from chat.prompts.analyze import ANALYSIS_CYPHER_PROMPT_W_CONTEXT, ANALYSIS_QA_PROMPT
from chat.prompts.compare import COMPARISON_CYPHER_PROMPT_W_CONTEXT, COMPARISON_QA_PROMPT
from chat.prompts.find import FIND_CYPHER_PROMPT_W_CONTEXT, FIND_QA_PROMPT
from chat.prompts.general import SUMMARY_PROMPT, DISPATCH_PROMPT

# Initialize the Neo4j driver
uri = "neo4j+s://d1c92482.databases.neo4j.io"
username = "neo4j"
password = "H3mFJDVvmjPz1s5aDFi46XN8JFLGuYitPy6weie8stk"
driver = GraphDatabase.driver(uri, auth=(username, password))

graph = Neo4jGraph(url=uri, username="neo4j", password=password)

# Initialize the models
tokenizer = tiktoken.encoding_for_model("gpt-4")

llm = ChatOpenAI(temperature=0, model="gpt-4o", streaming=True)  # Enable streaming

dispatch_chain = LLMChain(llm=llm, prompt=DISPATCH_PROMPT)
summary_chain = LLMChain(llm=llm, prompt=SUMMARY_PROMPT)

def get_summarized_chat_history(chat_history, token_limit=5000):
    chat_history_str = "\n".join(chat_history)
    summary_response = summary_chain.invoke({"chat_history": chat_history_str, "token_limit": token_limit})
    return [summary_response['text']]  # Replace full history with the summary
    

# Analyze chain
def analyze_player(question, chat_history):
    analysis_cypher_chain = LLMChain(llm=llm, prompt=ANALYSIS_CYPHER_PROMPT_W_CONTEXT)
    analysis_cypher_response = analysis_cypher_chain.invoke({
        "schema": graph.schema,
        "question": question,
        "chat_history": chat_history
    })
    analysis_cypher = clean_cypher_response(analysis_cypher_response['text'])
    analysis_context = graph.query(analysis_cypher)
    
    analysis_qa_chain = LLMChain(llm=llm, prompt=ANALYSIS_QA_PROMPT)
    return stream_response(analysis_qa_chain, {
        "context": analysis_context,
        "question": question,
        "chat_history": chat_history
    })

# Compare chain
def compare_players(question, chat_history):
    comparison_cypher_chain = LLMChain(llm=llm, prompt=COMPARISON_CYPHER_PROMPT_W_CONTEXT)
    comparison_cypher_response = comparison_cypher_chain.invoke({
        "schema": graph.schema,
        "question": question,
        "chat_history": chat_history
    })

    comparison_cypher = clean_cypher_response(comparison_cypher_response['text'])

    comparison_cypher_list = ast.literal_eval(comparison_cypher)
    comparison_context = [graph.query(cypher_query) for cypher_query in comparison_cypher_list]
    
    comparison_qa_chain = LLMChain(llm=llm, prompt=COMPARISON_QA_PROMPT)
    return stream_response(comparison_qa_chain, {
        "context": comparison_context,
        "question": question,
        "chat_history": chat_history
    })

# Find players chain
def find_players(question, chat_history):
    find_cypher_chain = LLMChain(llm=llm, prompt=FIND_CYPHER_PROMPT_W_CONTEXT)
    find_cypher_response = find_cypher_chain.invoke({
        "schema": graph.schema,
        "question": question,
        "chat_history": chat_history
    })
    find_cypher = clean_cypher_response(find_cypher_response['text'])
    find_context = graph.query(find_cypher)
    
    find_qa_chain = LLMChain(llm=llm, prompt=FIND_QA_PROMPT)
    return stream_response(find_qa_chain, {
        "context": find_context,
        "question": question,
        "chat_history": chat_history
    })

# Utility to clean cypher responses
def clean_cypher_response(cypher):
    for code_block in ["```cypher", "```json", "```"]:
        if code_block in cypher:
            cypher = cypher.replace(code_block, "")
    return cypher

# Function to stream responses token by token
def stream_response(chain, inputs):
    response_container = st.empty()  # Placeholder for the response
    current_response = ""

    for token in chain.stream(inputs):
        #st.write(token)
        current_response += token['text']
        response_container.text(current_response)  # Update the placeholder dynamically
    
    return current_response


# Main Streamlit app function
def main():
    st.title("Football Player Insights")

    # Initialize the chat history and token limit
    chat_history = []
    token_limit = 5000
    
    # Input for the user question
    question = st.text_input("Ask a football question:")
    
    # When user submits the question
    if question:
        chat_history_str = "\n".join(chat_history)
        if len(tokenizer.encode(chat_history_str)) > token_limit:
            chat_history = get_summarized_chat_history(chat_history=chat_history, token_limit=token_limit)
        
        # Determine the type of question (analysis, comparison, or find)
        dispatch_response = dispatch_chain.invoke({"question": question, "chat_history": chat_history})
        task_type = dispatch_response['text'].strip().lower()
        #st.write("Dispatch output: " + task_type)
        
        # Stream the response based on the task type
        if task_type == "analysis":
            response = analyze_player(question, chat_history)
        elif task_type == "comparison":
            response = compare_players(question, chat_history)
        elif task_type == "find":
            response = find_players(question, chat_history)
        else:
            response = "I couldn't understand your question."
        st.write("FULL RESPONSE:")
        st.write(response)
        chat_history.append(f"User: {question}\nBot: {response}")
        #st.write("\nChat History:")
        #st.write("\n".join(chat_history))


if __name__ == "__main__":
    main()
