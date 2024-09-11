from langchain_core.prompts.prompt import PromptTemplate

BASIC_CONTEXT = """
Some extra information about the graph database:
All Position Nodes:
(:Position {{POSITION_CODE: "MC", MAIN_POSITION: "Midfielder", ALIAS: "Number 8", POSITION_NAME: "Central Midfield"}})
(:Position {{POSITION_CODE: "DM", MAIN_POSITION: "Midfielder", ALIAS: "Number 6", POSITION_NAME: "Defensive Midfield"}})
(:Position {{POSITION_CODE: "ST", MAIN_POSITION: "Forward", ALIAS: "Number 9", POSITION_NAME: "Centre Forward"}})
(:Position {{POSITION_CODE: "DL", MAIN_POSITION: "Defender", ALIAS: NaN, POSITION_NAME: "Left Back"}})
(:Position {{POSITION_CODE: "LW", MAIN_POSITION: "Forward", ALIAS: NaN, POSITION_NAME: "Left Wing"}})
(:Position {{POSITION_CODE: "GK", MAIN_POSITION: "Goalkeeper", ALIAS: NaN, POSITION_NAME: "Goalkeeper"}})
(:Position {{POSITION_CODE: "MR", MAIN_POSITION: "Midfielder", ALIAS: NaN, POSITION_NAME: "Right Midfield"}})
(:Position {{POSITION_CODE: "DC", MAIN_POSITION: "Defender", ALIAS: NaN, POSITION_NAME: "Centre Back"}})
(:Position {{POSITION_CODE: "ML", MAIN_POSITION: "Midfielder", ALIAS: NaN, POSITION_NAME: "Left Midfield"}})
(:Position {{POSITION_CODE: "RW", MAIN_POSITION: "Forward", ALIAS: NaN, POSITION_NAME: "Right Wing"}})
(:Position {{POSITION_CODE: "DR", MAIN_POSITION: "Defender", ALIAS: NaN, POSITION_NAME: "Right Back"}})
(:Position {{POSITION_CODE: "AM", MAIN_POSITION: "Midfielder", ALIAS: "Number 10", POSITION_NAME: "Attacking Midfield"}})

All Strength nodes:
(:Strength {{STRENGTH: "Aerial duels"}})
(:Strength {{STRENGTH: "Ball control"}})
(:Strength {{STRENGTH: "Positioning"}})
(:Strength {{STRENGTH: "Tackling"}})
(:Strength {{STRENGTH: "Runs out"}})
(:Strength {{STRENGTH: "Discipline"}})
(:Strength {{STRENGTH: "High pressing"}})
(:Strength {{STRENGTH: "Finishing"}})
(:Strength {{STRENGTH: "High claims"}})
(:Strength {{STRENGTH: "Penalty taking"}})
(:Strength {{STRENGTH: "Passing"}})
(:Strength {{STRENGTH: "Long balls"}})
(:Strength {{STRENGTH: "Ball interception"}})
(:Strength {{STRENGTH: "Anchor play"}})
(:Strength {{STRENGTH: "Direct free kicks"}})
(:Strength {{STRENGTH: "Long shots saving"}})
(:Strength {{STRENGTH: "Reflexes"}})
(:Strength {{STRENGTH: "Long shots"}})
(:Strength {{STRENGTH: "Handling"}})
(:Strength {{STRENGTH: "Playmaking"}})
(:Strength {{STRENGTH: "Penalty saving"}})
(:Strength {{STRENGTH: "Error proneness"}})
(:Strength {{STRENGTH: "Consistency"}})
(:Strength {{STRENGTH: "Ground duels"}})

Some Tournament nodes:
(:Tournament {{TOURNAMENT_SLUG: "european-championship", COUNTRY: Europe, TOURNAMENT_ID: 1, TOURNAMENT_NAME: EURO}})
(:Tournament {{TOURNAMENT_SLUG: "trophee-des-champions", COUNTRY: France, TOURNAMENT_ID: 339, TOURNAMENT_NAME: Trophée des Champions}})
(:Tournament {{TOURNAMENT_SLUG: "european-championship-qualification", COUNTRY: Europe, TOURNAMENT_ID: 27, TOURNAMENT_NAME: EURO, Qualification}})
(:Tournament {{TOURNAMENT_SLUG: "ligue-1", COUNTRY: France, TOURNAMENT_ID: 34, TOURNAMENT_NAME: Ligue 1}})
(:Tournament {{TOURNAMENT_SLUG: "uefa-champions-league", COUNTRY: Europe, TOURNAMENT_ID: 7, TOURNAMENT_NAME: UEFA Champions League}})
(:Tournament {{TOURNAMENT_SLUG: "world-championship", COUNTRY: World, TOURNAMENT_ID: 16, TOURNAMENT_NAME: World Championship}})
(:Tournament {{TOURNAMENT_SLUG: "uefa-nations-league", COUNTRY: Europe, TOURNAMENT_ID: 10783, TOURNAMENT_NAME: UEFA Nations League}})
(:Tournament {{TOURNAMENT_SLUG: "world-championship-qual-uefa", COUNTRY: Europe, TOURNAMENT_ID: 11, TOURNAMENT_NAME: World Championship Qual. UEFA}})
(:Tournament {{TOURNAMENT_SLUG: "coupe-de-france", COUNTRY: France, TOURNAMENT_ID: 335, TOURNAMENT_NAME: Coupe de France}})
(:Tournament {{TOURNAMENT_SLUG: "coupe-de-la-ligue", COUNTRY: France, TOURNAMENT_ID: 333, TOURNAMENT_NAME: Coupe de la Ligue}})
(:Tournament {{TOURNAMENT_SLUG: "u19-european-championship", COUNTRY: Europe, TOURNAMENT_ID: 258, TOURNAMENT_NAME: U19 European Championship}})
(:Tournament {{TOURNAMENT_SLUG: "uefa-europa-leagu"e, COUNTRY: Europe, TOURNAMENT_ID: 679, TOURNAMENT_NAME: UEFA Europa League}})
(:Tournament {{TOURNAMENT_SLUG: "copa-america", COUNTRY: South America, TOURNAMENT_ID: 133, TOURNAMENT_NAME: Copa América}})
(:Tournament {{TOURNAMENT_SLUG: "supercopa-de-espana", COUNTRY: Spain, TOURNAMENT_ID: 213, TOURNAMENT_NAME: Supercopa de Espana}})
(:Tournament {{TOURNAMENT_SLUG: "world-championship-qual-conmebol", COUNTRY: South America, TOURNAMENT_ID: 295, TOURNAMENT_NAME: World Championship Qual. CONMEBOL}})
(:Tournament {{TOURNAMENT_SLUG: "laliga", COUNTRY: Spain, TOURNAMENT_ID: 8, TOURNAMENT_NAME: LaLiga}})
(:Tournament {{TOURNAMENT_SLUG: "club-world-championship", COUNTRY: World, TOURNAMENT_ID: 357, TOURNAMENT_NAME: Club World Championship}})
(:Tournament {{TOURNAMENT_SLUG: "uefa-super-cup", COUNTRY: Europe, TOURNAMENT_ID: 465, TOURNAMENT_NAME: UEFA Super Cup}})
(:Tournament {{TOURNAMENT_SLUG: "copa-del-rey", COUNTRY: Spain, TOURNAMENT_ID: 329, TOURNAMENT_NAME: Copa del Rey}})
(:Tournament {{TOURNAMENT_SLUG: "brasileirao-serie-a", COUNTRY: Brazil, TOURNAMENT_ID: 325, TOURNAMENT_NAME: Brasileirio Serie A}})
(:Tournament {{TOURNAMENT_SLUG: "bundesliga", COUNTRY: Germany, TOURNAMENT_ID: 35, TOURNAMENT_NAME: Bundesliga}})
(:Tournament {{TOURNAMENT_SLUG: "championship", COUNTRY: England, TOURNAMENT_ID: 18, TOURNAMENT_NAME: Championship}})
(:Tournament {{TOURNAMENT_SLUG: "trendyol-super-lig", COUNTRY: Turkey, TOURNAMENT_ID: 52, TOURNAMENT_NAME: Trendyol Süper Lig}})
(:Tournament {{TOURNAMENT_SLUG: "uefa-europa-conference-league", COUNTRY: Europe, TOURNAMENT_ID: 17015, TOURNAMENT_NAME: UEFA Europa Conference League}})
(:Tournament {{TOURNAMENT_SLUG: "serie-a", COUNTRY: Italy, TOURNAMENT_ID: 23, TOURNAMENT_NAME: Serie A}})
(:Tournament {{TOURNAMENT_SLUG: "premier-league", COUNTRY: England, TOURNAMENT_ID: 17, TOURNAMENT_NAME: Premier League}})
(:Tournament {{TOURNAMENT_SLUG: "olympic-games", COUNTRY: World, TOURNAMENT_ID: 436, TOURNAMENT_NAME: Olympic Games}})
(:Tournament {{TOURNAMENT_SLUG: "laliga-2", COUNTRY: Spain, TOURNAMENT_ID: 54, TOURNAMENT_NAME: LaLiga 2}})
(:Tournament {{TOURNAMENT_SLUG: "liga-portugal-betclic", COUNTRY: Portugal, TOURNAMENT_ID: 238, TOURNAMENT_NAME: Liga Portugal Betclic}})
(:Tournament {{TOURNAMENT_SLUG: "ligue-2", COUNTRY: France, TOURNAMENT_ID: 182, TOURNAMENT_NAME: Ligue 2}})
(:Tournament {{TOURNAMENT_SLUG: "premier-league", COUNTRY: Ukraine, TOURNAMENT_ID: 218, TOURNAMENT_NAME: Ukrainian Premier League}})
(:Tournament {{TOURNAMENT_SLUG: "liga-portugal-2", COUNTRY: Portugal, TOURNAMENT_ID: 239, TOURNAMENT_NAME: Liga Portugal 2}})
(:Tournament {{TOURNAMENT_SLUG: "eredivisie", COUNTRY: Netherlands, TOURNAMENT_ID: 37, TOURNAMENT_NAME: Eredivisie}})
(:Tournament {{TOURNAMENT_SLUG: "eerste-divisie", COUNTRY: Netherlands, TOURNAMENT_ID: 131, TOURNAMENT_NAME: Eerste Divisie}})
(:Tournament {{TOURNAMENT_SLUG: "primera-division", COUNTRY: Uruguay, TOURNAMENT_ID: 278, TOURNAMENT_NAME: Uruguayan Primera Division}})
(:Tournament {{TOURNAMENT_SLUG: "1-nl", COUNTRY: Croatia, TOURNAMENT_ID: 724, TOURNAMENT_NAME: 1. NL}})
(:Tournament {{TOURNAMENT_SLUG: "mls", COUNTRY: USA, TOURNAMENT_ID: 242, TOURNAMENT_NAME: MLS}})
(:Tournament {{TOURNAMENT_SLUG: "superliga", COUNTRY: Denmark, TOURNAMENT_ID: 39, TOURNAMENT_NAME: Danish Superliga}})
(:Tournament {{TOURNAMENT_SLUG: "liga-profesional-de-futbol", COUNTRY: Argentina, TOURNAMENT_ID: 155, TOURNAMENT_NAME: Liga Profesional de Futbol}})
(:Tournament {{TOURNAMENT_SLUG: "pro-league", COUNTRY: Belgium, TOURNAMENT_ID: 38, TOURNAMENT_NAME: Pro League}})
(:Tournament {{TOURNAMENT_SLUG: "bundesliga", COUNTRY: Austria, TOURNAMENT_ID: 45, TOURNAMENT_NAME: Bundesliga}})
(:Tournament {{TOURNAMENT_SLUG: "premier-liga", COUNTRY: Russia, TOURNAMENT_ID: 203, TOURNAMENT_NAME: Russian Premier League}})
(:Tournament {{TOURNAMENT_SLUG: "africa-cup-of-nations", COUNTRY: Africa, TOURNAMENT_ID: 270, TOURNAMENT_NAME: Africa Cup of Nations}})
(:Tournament {{TOURNAMENT_SLUG: "africa-cup-of-nations-qual", COUNTRY: Africa, TOURNAMENT_ID: 1848, TOURNAMENT_NAME: Africa Cup of Nations Qual.}})
(:Tournament {{TOURNAMENT_SLUG: "superliga", COUNTRY: Romania, TOURNAMENT_ID: 152, TOURNAMENT_NAME: Romanian Super Liga}})
(:Tournament {{TOURNAMENT_SLUG: "mozzart-bet-superliga", COUNTRY: Serbia, TOURNAMENT_ID: 210, TOURNAMENT_NAME: Mozzart Bet Superliga}})
(:Tournament {{TOURNAMENT_SLUG: "serie-b", COUNTRY: Italy, TOURNAMENT_ID: 53, TOURNAMENT_NAME: Serie B}})
(:Tournament {{TOURNAMENT_SLUG: "premiership", COUNTRY: Scotland, TOURNAMENT_ID: 36, TOURNAMENT_NAME: Scottish Premiership}})
(:Tournament {{TOURNAMENT_SLUG: "j1-league", COUNTRY: Japan, TOURNAMENT_ID: 196, TOURNAMENT_NAME: J1 League}})
(:Tournament {{TOURNAMENT_SLUG: "saudi-pro-league", COUNTRY: Saudi Arabia, TOURNAMENT_ID: 955, TOURNAMENT_NAME: Saudi Pro League}})
(:Tournament {{TOURNAMENT_SLUG: "eliteserien", COUNTRY: Norway, TOURNAMENT_ID: 20, TOURNAMENT_NAME: Eliteserien}})
(:Tournament {{TOURNAMENT_SLUG: "trendyol-1lig", COUNTRY: Turkey, TOURNAMENT_ID: 98, TOURNAMENT_NAME: Trendyol 1.Lig}})
NOTE: Ligue 1 of France, Bundesliga of Germany, La Liga of Spain, Premier League of England, and Serie A of Italy are referred to as 'Top 5 Leagues'
"""

GENERAL_CYPHER_TEMPLATE = """Task:Generate Cypher statement to query a graph database. The database is of football (soccer) players data.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Only apply filters on objective attributes mentioned below. If the user question includes subjective descriptions also mentioned below, ignore them.
Subjective descriptions: fast, has pace, strong, etc.
IMPORTANT INSRUCTION: Your response should only be the cypher query and nothing else. Never write any introductory or explanation sentences before or after the query. Obey this rule at all cost
Schema:
{schema}

"""

GENERAL_CYPHER_TEMPLATE_W_CONTEXT = GENERAL_CYPHER_TEMPLATE + BASIC_CONTEXT

GENERAL_CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=GENERAL_CYPHER_TEMPLATE
)

GENERAL_CYPHER_PROMPT_W_CONTEXT = PromptTemplate(
    input_variables=["schema", "question"], template=GENERAL_CYPHER_TEMPLATE_W_CONTEXT
)

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["chat_history"],
    template="""
    Summarize the following conversation between a user and an AI assistant, keeping only the important context needed for future responses. Chat will be about football players. Be sure to keep key information like player names, team names, tournament / league names etc.

    Limit your answer to this number of tokens: {token_limit}

    Chat History: {chat_history}
    """
)

DISPATCH_PROMPT = PromptTemplate(
    input_variables=["question", "chat_history"],
    template="""
    Given the below question about football players and the previous conversation history, determine whether this is an 'analysis', 'comparison', or 'find' query.
    Your answer should be one of the following words: 'analysis', 'comparison', or 'find'. Always with one of these words and one word only. Do not complete it with a sentence.
    If the question is asking about a specific player it is 'analysis'. If the question is asking about multiple players and their respective qualities it is 'comparison'. If the question describes a player with some criteria, it is 'find'.

    Example:
    Question: Who are some Central Midfield players from Bundesliga worth between 20-25 million
    Answer: find
    Question: Which one is the best at passing
    Answer: compare
    Question: How was Haaland's performance last season
    Answer: analysis

    Chat History: {chat_history}
    Question: {question} 
    """
)