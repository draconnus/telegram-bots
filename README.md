# telegram-bots


# GameOrganizerBot
Bot responsible for organization of volleybal games.

Features
- Players are registed by adding the bot and sending /register message.
- Sends question message to which players respond with 'I'm game' or 'I'm not game'. 
    Messages are sent automatically few days before the game. 
    Messages are being sent to a player until he responds.
- Prioritize participants by frequency of show ups.
    Initialy send messages to first 12 players.
    If there are not enough players (12 usauly) by one and a half days before the game, send additional messages to next players from priority list.
    When player shows up, he is confirmed by an admin.


Future stuff:
- Extend responses with driver information so that we can organize car trips.
