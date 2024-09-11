from langchain_core.prompts.prompt import PromptTemplate
from chat.prompts.general import GENERAL_CYPHER_TEMPLATE, GENERAL_CYPHER_TEMPLATE_W_CONTEXT

FIND_CYPHER_COMMANDS = """
If the following descriptions or their synonyms / paraphrases are mentioned in the question, look for the provided properties and/or relationships. The variables in user question will be denoted between <> For example, if user question is "plays for Real Madrid", template is "plays for <name of a football team>":
"aged <age number>" : PLAYER_BIRTH_DATE of Player node. The current year is 2024. Subtrack and find the age. If age is below 25, consider the player young.
"Played in <name of a tournament>" : PLAYED_IN_WITH_STATS relationship exists to the Tournament node specified. Property to match is TOURNAMENT_SLUG. 
"Plays for <name of a football team>" : PLAYS_FOR relationship exists to the Team node specified. Property to match is TEAM_SLUG
"worth <a number of value>" : PLAYER_MARKET_VALUE property of Player node. If the user question number is written out like 1m, 1M, 1 million, put the actual number in the query, which is 1000000. If user says "around X", it means "between X-2000000 and X+2000000"
"tall" : PLAYER_HEIGHT property of Player node is above 180
Note: Normalise user input for names. For example, if user input is "plays for Çaykur Rizespor", query should have "t:Team {{TEAM_NAME : "caykur-rizespor"}}"

After applying these filters, return all properties and relationships of the matching nodes.
IMPORTANT NOTE: If the user query includes subjective descriptions such as fast, strong, intelligent, etc. ignore them

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.


Examples: Here are a few examples of generated Cypher statements for particular questions:

Question: Players with good physique that play for Real Madrid as a defender?
Query:
MATCH (p:Player)-[:PLAYS_FOR]->(t:Team {{TEAM_NAME: 'Real Madrid'}})
MATCH (p)-[:PLAYS_IN_THE_POSITION_OF]->(pos:Position {{MAIN_POSITION: 'Defender'}})
MATCH (p)-[r]->(n)
RETURN p

Question: Find intelligent number 8 players worth around 10 million from top 5 leagues aged between 20-27
Query:
MATCH (p)-[:PLAYS_IN_THE_POSITION_OF]->(pos:Position {{POSITION_NAME: 'Central Midfield'}})
WHERE 8000000 < p.PLAYER_MARKET_VALUE < 12000000  
AND p.LEAGUE_NAME IN ["LaLiga", "SerieA", "PremierLeague", "Bundesliga", "Ligue1"] 
AND date("1997-01-01") < p.PLAYER_BIRTH_DATE < date("2005-01-01")
RETURN p

NOTE: There is no BETWEEN as an expression in cypher. Always use "value1 < variable < value2" format

The question is:
{question}
"""


FIND_CYPHER_TEMPLATE = GENERAL_CYPHER_TEMPLATE + FIND_CYPHER_COMMANDS
FIND_CYPHER_TEMPLATE_W_CONTEXT = GENERAL_CYPHER_TEMPLATE_W_CONTEXT + FIND_CYPHER_COMMANDS

FIND_CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question", "chat_history"], template=FIND_CYPHER_TEMPLATE
)

FIND_CYPHER_PROMPT_W_CONTEXT = PromptTemplate(
    input_variables=["schema", "question", "chat_history"], template=FIND_CYPHER_TEMPLATE_W_CONTEXT
)

FIND_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers for football player analysis.
The information part contains the provided information that you must use to construct an answer.
The information will include various data. Make use of it, analyze the data and report you findings in your answer.
The information will consist of some players and their attributes. List them with brief descriptions of the players. You can group the players based on the criteria mentioned in the question.
For example, if question includes "from top 5 league", you can group the players based on the league they are playing.

The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
You can use internal knowledge to support your answer ONLY if the question explicity asks you to. If question does not say that, do ONLY and ONLY use context information.

If the provided information is empty, say that you don't know the answer.
Information:
{context}

Question: {question}
Helpful Answer:"""

FIND_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question", "chat_history"], template=FIND_QA_TEMPLATE
)