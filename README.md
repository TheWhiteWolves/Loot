# Loot Discord Bot

A Discord bot that handles loot distribution with random number rolling between participants.

## Features

- **`/loot {item}`** - Start a loot roll for a specific item
- **Join Button** - Users can click to join the loot
- **End Button** - End the loot and trigger random number rolls (1-100)
- **Automatic Winner Selection** - The participant with the highest roll wins
- **Results Display** - Shows all participants, their rolls, and announces the winner

## Requirements

- Python 3.10+
- discord.py 2.4.1+

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a Discord Bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application"
   - Give it a name (e.g., "Loot Bot")
   - Go to "Bot" section and click "Add Bot"
   - Copy the token

3. **Set Bot Permissions**
   - In Developer Portal, go to OAuth2 → URL Generator
   - Select scopes: `bot`, `applications.commands`
   - Select permissions:
     - `Send Messages`
     - `Read Messages/View Channels`
     - `Embed Links`
   - Copy the generated URL and visit it to invite the bot to your server

4. **Configure the Token**
   - Open `bot.py`
   - Replace `YOUR_DISCORD_BOT_TOKEN_HERE` with your actual bot token
   - **Or better yet**, use an environment variable:
     ```python
     import os
     from dotenv import load_dotenv
     load_dotenv()
     TOKEN = os.getenv("DISCORD_TOKEN")
     ```

5. **Run the Bot**
   ```bash
   python bot.py
   ```

## Usage

1. Type `/loot diamond` in any channel
2. Users click "Join" to participate
3. Click "End Loot" to finish accepting participants
4. The bot rolls 1-100 for each participant
5. The winner (highest roll) is announced!

## Example Flow

```
User: /loot epic sword
Bot: Creates message with Join/End buttons

User A: Clicks Join (Participants: 1)
User B: Clicks Join (Participants: 2)
User C: Clicks Join (Participants: 3)

User A: Clicks End Loot
Bot: Rolls and announces results:
     1. User B - 87
     2. User C - 72
     3. User A - 45
     🏆 Winner: User B with a roll of 87!
```

## Notes

- Users can only join once per loot
- Buttons persist until the loot ends
- Results are displayed with an embed for clarity
- The bot requires permissions to send messages and embeds
