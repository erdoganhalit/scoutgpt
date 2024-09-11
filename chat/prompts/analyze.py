from langchain_core.prompts.prompt import PromptTemplate
from chat.prompts.general import GENERAL_CYPHER_TEMPLATE, GENERAL_CYPHER_TEMPLATE_W_CONTEXT

ANALYSIS_CYPHER_COMMANDS = """
 The question will be to analyze and report on one football player that the user asks for. 
 The question will include the name of the player and you will search for it in PLAYER_NAME property of Player nodes. 
 
 The user may or may not ask for specific aspects of the player. 
 
 Below is a list of player aspects that user can ask for and relevant relationship types that holds data for that aspect.

 injuries (relationship) : HAD_INJURY {{INJURY_SEASON: STRING, INJURY_START_DATE: DATE, INJURY_FINISH_DATE: DATE, INJURY_DURATION: FLOAT, GAMES_MISSED_DURING_INJURY: FLOAT, CLUBS_DURING_INJURY: LIST}}
 ratings (relationship) : HAS_RATINGS {{RATING_COUNT: INTEGER, RATING_MEAN: FLOAT, RATING_STD_VAR: FLOAT}}
 attributes / characteristics (node properties) : Player {{ATTACKING: FLOAT, TECHNICAL: FLOAT, TACTICAL: INTEGER, DEFENDING: FLOAT, CREATIVITY: FLOAT}}
 Physical stats (relationship properties): PLAYED_IN_WITH_STATS {{totalDuelsWonPercentage , aerialDuelsWon , totalDuelsWon , duelLost , groundDuelsWonPercentage , groundDuelsWon}}
 Passing stats (relationship properties): PLAYED_IN_WITH_STATS {{expectedAssists , totalChippedPasses , totalCross , totalPasses , accuratePasses , totalLongBalls , accurateCrossesPercentage , accuratePassesPercentage , accurateOppositionHalfPasses , totalOwnHalfPasses , inaccuratePasses , accurateLongBallsPercentage , accurateChippedPasses , passToAssist , accurateCrosses , accurateLongBalls , accurateFinalThirdPasses , crossesNotClaimed}}
 Scoring stats (relationship properties): PLAYED_IN_WITH_STATS {{bigChancesMissed , attemptPenaltyTarget , attemptPenaltyPost , penaltyGoals , headedGoals , goals , penaltyConversion , goalsFromInsideTheBox , penaltiesTaken , goalsFromOutsideTheBox , goalsAssistsSum , scoringFrequency , goalConversionPercentage , goalKicks , hitWoodwork , goalsPrevented , freeKickGoal , setPieceConversion}}
 Shooting stats (relationship properties): PLAYED_IN_WITH_STATS {{shotsOffTarget , totalShots , shotsFromOutsideTheBox , blockedShots , shotsOnTarget , shotsFromInsideTheBox , shotFromSetPiece}}
 Defending stats (relationship properties): PLAYED_IN_WITH_STATS {{clearances , tacklesWon , tacklesWonPercentage , interceptions , errorLeadToShot , errorLeadToGoal , ownGoals , ballRecovery , tackles }}
 Goalkeeper stats (relationship properties): PLAYED_IN_WITH_STATS {{highClaims , savedShotsFromInsideTheBox , savesParried , penaltyFaced , saves , penaltySave , savesCaught , cleanSheet , successfulRunsOut , savedShotsFromOutsideTheBox , punches , goalsConceded , goalsConcededOutsideTheBox , goalsConcededInsideTheBox , goalsPrevented}}
 Possession / ball control stats (relationship properties): PLAYED_IN_WITH_STATS {{dispossessed , possessionLost , possessionWonAttThird}}
 Aggressiveness stats (relationship properties): PLAYED_IN_WITH_STATS {{yellowRedCards , redCards , fouls , yellowCards , directRedCards}}
 Aerial stats (relationship properties): PLAYED_IN_WITH_STATS {{aerialLost , aerialDuelsWonPercentage}}
 General stats (relationship properties): PLAYED_IN_WITH_STATS {{touches , totalRating , appearances , type , countRating , totwAppearances , rating , minutesPlayed , substitutionsOut , substitutionsIn , wasFouled}}
 Dribbling stats (relationship properties): PLAYED_IN_WITH_STATS {{dribbledPast , successfulDribbles , successfulDribblesPercentage}}
 Attacking  (relationship properties): PLAYED_IN_WITH_STATS {{offsides , penaltyWon}}

 If question asks for specific aspects generate the query so that only the node and / or relationship properties are turned by the query. 
 For example,

 Question: 
 How is Kylian Mbappe's physicality in 2023-2024 season
 Query:
 MATCH (p:Player {{PLAYER_NAME: 'Kylian Mbappe'}})-[r:PLAYED_IN_WITH_STATS]->(t:Tournament)
 RETURN
  p, 
  r.totalDuelsWonPercentage AS totalDuelsWonPercentage,
  r.aerialDuelsWon AS aerialDuelsWon,
  r.totalDuelsWon AS totalDuelsWon,
  r.duelLost AS duelLost,
  r.groundDuelsWonPercentage AS groundDuelsWonPercentage,
  r.groundDuelsWon AS groundDuelsWon,
  t;

 The question or the chat_history will include the name of the player and you will search for it in PLAYER_NAME property of Player nodes.
 Chat history:
 {chat_history}

 The question is:
 {question}

 IMPORTANT NOTE: If the question or the chat history does not include a football player, then just write 'False' and nothing else. Obey this rule at all cost.
 """

ANALYSIS_CYPHER_TEMPLATE = GENERAL_CYPHER_TEMPLATE + ANALYSIS_CYPHER_COMMANDS
ANALYSIS_CYPHER_TEMPLATE_W_CONTEXT = GENERAL_CYPHER_TEMPLATE_W_CONTEXT + ANALYSIS_CYPHER_COMMANDS

ANALYSIS_CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question", "chat_history"], template=ANALYSIS_CYPHER_TEMPLATE
)

ANALYSIS_CYPHER_PROMPT_W_CONTEXT = PromptTemplate(
    input_variables=["schema", "question", "chat_history"], template=ANALYSIS_CYPHER_TEMPLATE_W_CONTEXT
)

ANALYSIS_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers for football player analysis.
The information part contains the provided information that you must use to construct an answer.
The information will include various data. Make use of it, analyze the data and report you findings in your answer.
Also the information may include multiple instances of the same data field. Account for all instances. Sum, aggregate them if necessary.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
You can use internal knowledge to support your answer ONLY if the question explicity asks you to. If question does not say that, do ONLY and ONLY use context information.

If the provided information is empty, say that you don't know the answer.
Information:
{context}

Chat history:
{chat_history}

Question: {question}
Helpful Answer:"""

ANALYSIS_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question", "chat_history"], template=ANALYSIS_QA_TEMPLATE
)