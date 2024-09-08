from langchain_core.prompts.prompt import PromptTemplate
from chat.prompts.general import GENERAL_CYPHER_TEMPLATE, GENERAL_CYPHER_TEMPLATE_W_CONTEXT

COMPARISON_CYPHER_COMMANDS = """
 The question will be to analyze and report on multiple (two or more) football player that the user asks for. 
 The question will include the names of the players and you will search for them in PLAYER_NAME property of Player nodes. 
 
 The user may or may not ask for specific aspects of the players. 
 
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

 If user question asks for specific aspects generate the query so that only the node and / or relationship properties of those aspects are turned by the query.
 IMPORTANT NOTE: Some properties are in multiple aspects categories. If the user selects those aspects or does not select an aspect at all, write those properties ONLY ONCE to prevent duplication 


 For every player name in the question write a seperate query and return them in a list

 For example,
 Question: 
 Compare Erling Haaland's performance in Premier League and Kylian Mbappe's in Ligue 1
 Query:
 [
    "MATCH (p:Player)-[r:PLAYED_IN_WITH_STATS]->(t:Tournament) WHERE p.PLAYER_NAME = 'Kylian Mbappe' AND t.TOURNAMENT_NAME = 'Ligue 1' RETURN p, r.totalDuelsWonPercentage AS totalDuelsWonPercentage, r.aerialDuelsWon AS aerialDuelsWon, r.totalDuelsWon AS totalDuelsWon, r.duelLost AS duelLost, r.groundDuelsWonPercentage AS groundDuelsWonPercentage, r.groundDuelsWon AS groundDuelsWon, r.expectedAssists AS expectedAssists, r.totalChippedPasses AS totalChippedPasses, r.totalCross AS totalCross, r.totalPasses AS totalPasses, r.accuratePasses AS accuratePasses, r.totalLongBalls AS totalLongBalls, r.accurateCrossesPercentage AS accurateCrossesPercentage, r.accuratePassesPercentage AS accuratePassesPercentage, r.accurateOppositionHalfPasses AS accurateOppositionHalfPasses, r.totalOwnHalfPasses AS totalOwnHalfPasses, r.inaccuratePasses AS inaccuratePasses, r.accurateLongBallsPercentage AS accurateLongBallsPercentage, r.accurateChippedPasses AS accurateChippedPasses, r.passToAssist AS passToAssist, r.accurateCrosses AS accurateCrosses, r.accurateLongBalls AS accurateLongBalls, r.accurateFinalThirdPasses AS accurateFinalThirdPasses, r.crossesNotClaimed AS crossesNotClaimed, r.bigChancesMissed AS bigChancesMissed, r.attemptPenaltyTarget AS attemptPenaltyTarget, r.attemptPenaltyPost AS attemptPenaltyPost, r.penaltyGoals AS penaltyGoals, r.goals AS goals, r.penaltyConversion AS penaltyConversion, r.goalsFromInsideTheBox AS goalsFromInsideTheBox, r.penaltiesTaken AS penaltiesTaken, r.goalsFromOutsideTheBox AS goalsFromOutsideTheBox, r.goalsAssistsSum AS goalsAssistsSum, r.scoringFrequency AS scoringFrequency, r.goalConversionPercentage AS goalConversionPercentage, r.goalKicks AS goalKicks, r.hitWoodwork AS hitWoodwork, r.goalsPrevented AS goalsPrevented, r.freeKickGoal AS freeKickGoal, r.setPieceConversion AS setPieceConversion, r.shotsOffTarget AS shotsOffTarget, r.totalShots AS totalShots, r.shotsFromOutsideTheBox AS shotsFromOutsideTheBox, r.blockedShots AS blockedShots, r.shotsOnTarget AS shotsOnTarget, r.shotsFromInsideTheBox AS shotsFromInsideTheBox, r.shotFromSetPiece AS shotFromSetPiece, r.clearances AS clearances, r.tacklesWon AS tacklesWon, r.tacklesWonPercentage AS tacklesWonPercentage, r.interceptions AS interceptions, r.errorLeadToShot AS errorLeadToShot, r.errorLeadToGoal AS errorLeadToGoal, r.ownGoals AS ownGoals, r.ballRecovery AS ballRecovery, r.tackles AS tackles, r.highClaims AS highClaims, r.savedShotsFromInsideTheBox AS savedShotsFromInsideTheBox, r.savesParried AS savesParried, r.penaltyFaced AS penaltyFaced, r.saves AS saves, r.penaltySave AS penaltySave, r.savesCaught AS savesCaught, r.cleanSheet AS cleanSheet, r.successfulRunsOut AS successfulRunsOut, r.savedShotsFromOutsideTheBox AS savedShotsFromOutsideTheBox, r.punches AS punches, r.goalsConceded AS goalsConceded, r.goalsConcededOutsideTheBox AS goalsConcededOutsideTheBox, r.goalsConcededInsideTheBox AS goalsConcededInsideTheBox, r.dispossessed AS dispossessed, r.possessionLost AS possessionLost, r.possessionWonAttThird AS possessionWonAttThird, r.yellowRedCards AS yellowRedCards, r.redCards AS redCards, r.fouls AS fouls, r.yellowCards AS yellowCards, r.directRedCards AS directRedCards, r.aerialLost AS aerialLost, r.aerialDuelsWonPercentage AS aerialDuelsWonPercentage, r.touches AS touches, r.totalRating AS totalRating, r.appearances AS appearances, r.type AS type, r.countRating AS countRating, r.totwAppearances AS totwAppearances, r.rating AS rating, r.minutesPlayed AS minutesPlayed, r.substitutionsOut AS substitutionsOut, r.substitutionsIn AS substitutionsIn, r.wasFouled AS wasFouled, r.dribbledPast AS dribbledPast, r.successfulDribbles AS successfulDribbles, r.successfulDribblesPercentage AS successfulDribblesPercentage, r.offsides AS offsides, r.penaltyWon AS penaltyWon, t;",
    "MATCH (p:Player)-[r:PLAYED_IN_WITH_STATS]->(t:Tournament) WHERE p.PLAYER_NAME = 'Erling Haaland' AND t.TOURNAMENT_NAME = 'Premier League' RETURN p, r.totalDuelsWonPercentage AS totalDuelsWonPercentage, r.aerialDuelsWon AS aerialDuelsWon, r.totalDuelsWon AS totalDuelsWon, r.duelLost AS duelLost, r.groundDuelsWonPercentage AS groundDuelsWonPercentage, r.groundDuelsWon AS groundDuelsWon, r.expectedAssists AS expectedAssists, r.totalChippedPasses AS totalChippedPasses, r.totalCross AS totalCross, r.totalPasses AS totalPasses, r.accuratePasses AS accuratePasses, r.totalLongBalls AS totalLongBalls, r.accurateCrossesPercentage AS accurateCrossesPercentage, r.accuratePassesPercentage AS accuratePassesPercentage, r.accurateOppositionHalfPasses AS accurateOppositionHalfPasses, r.totalOwnHalfPasses AS totalOwnHalfPasses, r.inaccuratePasses AS inaccuratePasses, r.accurateLongBallsPercentage AS accurateLongBallsPercentage, r.accurateChippedPasses AS accurateChippedPasses, r.passToAssist AS passToAssist, r.accurateCrosses AS accurateCrosses, r.accurateLongBalls AS accurateLongBalls, r.accurateFinalThirdPasses AS accurateFinalThirdPasses, r.crossesNotClaimed AS crossesNotClaimed, r.bigChancesMissed AS bigChancesMissed, r.attemptPenaltyTarget AS attemptPenaltyTarget, r.attemptPenaltyPost AS attemptPenaltyPost, r.penaltyGoals AS penaltyGoals, r.goals AS goals, r.penaltyConversion AS penaltyConversion, r.goalsFromInsideTheBox AS goalsFromInsideTheBox, r.penaltiesTaken AS penaltiesTaken, r.goalsFromOutsideTheBox AS goalsFromOutsideTheBox, r.goalsAssistsSum AS goalsAssistsSum, r.scoringFrequency AS scoringFrequency, r.goalConversionPercentage AS goalConversionPercentage, r.goalKicks AS goalKicks, r.hitWoodwork AS hitWoodwork, r.goalsPrevented AS goalsPrevented, r.freeKickGoal AS freeKickGoal, r.setPieceConversion AS setPieceConversion, r.shotsOffTarget AS shotsOffTarget, r.totalShots AS totalShots, r.shotsFromOutsideTheBox AS shotsFromOutsideTheBox, r.blockedShots AS blockedShots, r.shotsOnTarget AS shotsOnTarget, r.shotsFromInsideTheBox AS shotsFromInsideTheBox, r.shotFromSetPiece AS shotFromSetPiece, r.clearances AS clearances, r.tacklesWon AS tacklesWon, r.tacklesWonPercentage AS tacklesWonPercentage, r.interceptions AS interceptions, r.errorLeadToShot AS errorLeadToShot, r.errorLeadToGoal AS errorLeadToGoal, r.ownGoals AS ownGoals, r.ballRecovery AS ballRecovery, r.tackles AS tackles, r.highClaims AS highClaims, r.savedShotsFromInsideTheBox AS savedShotsFromInsideTheBox, r.savesParried AS savesParried, r.penaltyFaced AS penaltyFaced, r.saves AS saves, r.penaltySave AS penaltySave, r.savesCaught AS savesCaught, r.cleanSheet AS cleanSheet, r.successfulRunsOut AS successfulRunsOut, r.savedShotsFromOutsideTheBox AS savedShotsFromOutsideTheBox, r.punches AS punches, r.goalsConceded AS goalsConceded, r.goalsConcededOutsideTheBox AS goalsConcededOutsideTheBox, r.goalsConcededInsideTheBox AS goalsConcededInsideTheBox, r.dispossessed AS dispossessed, r.possessionLost AS possessionLost, r.possessionWonAttThird AS possessionWonAttThird, r.yellowRedCards AS yellowRedCards, r.redCards AS redCards, r.fouls AS fouls, r.yellowCards AS yellowCards, r.directRedCards AS directRedCards, r.aerialLost AS aerialLost, r.aerialDuelsWonPercentage AS aerialDuelsWonPercentage, r.touches AS touches, r.totalRating AS totalRating, r.appearances AS appearances, r.type AS type, r.countRating AS countRating, r.totwAppearances AS totwAppearances, r.rating AS rating, r.minutesPlayed AS minutesPlayed, r.substitutionsOut AS substitutionsOut, r.substitutionsIn AS substitutionsIn, r.wasFouled AS wasFouled, r.dribbledPast AS dribbledPast, r.successfulDribbles AS successfulDribbles, r.successfulDribblesPercentage AS successfulDribblesPercentage, r.offsides AS offsides, r.penaltyWon AS penaltyWon, t;"
 ]

 The question will include the name of the player and you will search for it in PLAYER_NAME property of Player nodes.

 The question is:
 {question}

 IMPORTANT NOTE: If the question does not include multiple football player names, then just write 'False' and nothing else. Obey this rule at all cost.

"""

COMPARISON_CYPHER_TEMPLATE = GENERAL_CYPHER_TEMPLATE + COMPARISON_CYPHER_COMMANDS
COMPARISON_CYPHER_TEMPLATE_W_CONTEXT = GENERAL_CYPHER_TEMPLATE_W_CONTEXT + COMPARISON_CYPHER_COMMANDS

COMPARISON_CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=COMPARISON_CYPHER_TEMPLATE
)

COMPARISON_CYPHER_PROMPT_W_CONTEXT = PromptTemplate(
    input_variables=["schema", "question"], template=COMPARISON_CYPHER_TEMPLATE_W_CONTEXT
)

COMPARISON_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers for football player analysis.
The information part contains the provided information that you must use to construct an answer.
The information will include various data. Make use of it, analyze the data and report you findings in your answer.
The information will consist of stats of multiple football players and you will be asked to compare them in some way. You can group the stats as passing, attacking, defense etc. to better format your answer.
Also the information may include multiple instances of the same data field. Account for all instances. Sum, aggregate them if necessary.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
You can use internal knowledge to support your answer ONLY if the question explicity asks you to. If question does not say that, do ONLY and ONLY use context information.

If the provided information is empty, say that you don't know the answer.
Information:
{context}

Question: {question}
Helpful Answer:"""

COMPARISON_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"], template=COMPARISON_QA_TEMPLATE
)

