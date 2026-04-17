# 🎲 Loot Discord Bot

A Discord bot that handles loot distribution with random number rolling between participants. Perfect for gaming communities, giveaways, or any scenario where fair random selection is needed!

## ✨ Features

- **`/loot {item}`** - Start a loot roll for a specific item
- **`/ping`** - Check if the bot is alive and responsive
- **`/sync`** - Sync bot commands (Admin only)
- **Interactive Join Button** - Users can click to join the loot
- **End Button** - End the loot and trigger random number rolls (1-100)
- **Automatic Winner Selection** - The participant with the highest roll wins
- **Results Display** - Shows all participants, their rolls, and announces the winner with a beautiful embed
- **Duplicate Prevention** - Users can only join once per loot session
- **Persistent UI** - Buttons remain active until the loot ends

## 📋 Requirements

- Python 3.10+
- discord.py 2.7.1
- python-dotenv 1.0.0

## 🚀 Setup

### 1. **Clone/Download the Repository**
```bash
cd your-desired-directory
# Place the bot files here
```

### 2. **Create Virtual Environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Create a Discord Bot**
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Click "New Application"
- Give it a name (e.g., "Loot Bot")
- Go to "Bot" section and click "Add Bot"
- Copy the **Token** (keep this secret!)

### 5. **Set Bot Permissions**
- In Developer Portal, go to **OAuth2 → URL Generator**
- Select scopes: `bot`, `applications.commands`
- Select permissions:
  - `Send Messages`
  - `Read Messages/View Channels`
  - `Embed Links`
  - `Use Slash Commands`
- Copy the generated URL and visit it to invite the bot to your server

### 6. **Configure Environment Variables**
Create a `.env` file in the same directory as `bot.py`:
```env
DISCORD_TOKEN=your_bot_token_here
```

### 7. **Run the Bot**
```bash
# Make sure you're in the virtual environment
python bot.py
```

## 🎮 Usage

### Basic Loot Flow:
1. Type `/loot diamond sword` in any channel
2. Users click the **"Join"** button to participate
3. Click the **"End Loot"** button to finish accepting participants
4. The bot rolls 1-100 for each participant
5. The winner (highest roll) is announced with a celebration! 🎉

### Available Commands:
- `/loot {item_name}` - Start a new loot session
- `/ping` - Test if the bot is online
- `/sync` - Sync commands (admin only, use if commands don't appear)

## 📖 Example Flow

```
User: /loot legendary sword
Bot: Creates message with Join/End buttons

User A: Clicks Join (Participants: 1)
User B: Clicks Join (Participants: 2)
User C: Clicks Join (Participants: 3)

User A: Clicks "End Loot"
Bot: Rolls and announces results:
     1. User B - 87
     2. User C - 72
     3. User A - 45
     🏆 Winner: User B with a roll of 87!
```

## 🔧 Troubleshooting

### Bot Not Responding to Commands:
- Make sure the bot has been invited with proper permissions
- Try `/sync` to refresh the bot's commands
- Check that the bot is online in your server

### Import Errors:
- Ensure you're running from the virtual environment
- Run `pip install -r requirements.txt` again

### Permission Issues:
- Regenerate the invite URL with correct scopes and permissions
- Make sure the bot has "Use Slash Commands" permission

## 📝 Notes

- Users can only join once per loot session
- Buttons remain active until the loot ends
- Results are displayed with colored embeds for clarity
- The bot requires message and embed permissions to function
- Loot sessions are stored in memory (resets on bot restart)
- Random rolls use Python's `random` module for fair distribution

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the bot!

## 📄 License

This project is open source. Use it however you like!
