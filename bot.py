import discord
from discord.ext import commands
from discord import app_commands
import random
import os
from dotenv import load_dotenv
from typing import Dict, Set, List, Tuple

# Initialize bot
intents = discord.Intents.default()
# intents.message_content = True  # Removed - not needed for slash commands
bot = commands.Bot(command_prefix="/", intents=intents)

# Store active loot sessions: {message_id: {"item": str, "participants": Set[User], "ended": bool}}
loot_sessions: Dict[int, dict] = {}


class LootView(discord.ui.View):
    def __init__(self, item_name: str, message_id: int, initiator_id: int):
        super().__init__(timeout=None)
        self.item_name = item_name
        self.message_id = message_id
        self.initiator_id = initiator_id
        self.participants: Set[discord.User] = set()
        self.ended = False

    @discord.ui.button(label="Join", style=discord.ButtonStyle.green, custom_id="loot_join")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ended:
            await interaction.response.send_message(
                "❌ This loot has already ended! No more participants can join.",
                ephemeral=True
            )
            return

        if interaction.user in self.participants:
            await interaction.response.send_message(
                f"✅ You're already in the participant list for **{self.item_name}**!",
                ephemeral=True
            )
            return

        self.participants.add(interaction.user)
        await interaction.response.send_message(
            f"✅ You've joined the loot for **{self.item_name}**! Current participants: {len(self.participants)}",
            ephemeral=True
        )

        # Update the message
        await self.update_message(interaction)

    @discord.ui.button(label="End Loot", style=discord.ButtonStyle.red, custom_id="loot_end")
    async def end_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.initiator_id:
            await interaction.response.send_message(
                "❌ Only the user who started this loot can end it!",
                ephemeral=True
            )
            return

        if self.ended:
            await interaction.response.send_message(
                "❌ This loot has already ended!",
                ephemeral=True
            )
            return

        if len(self.participants) == 0:
            await interaction.response.send_message(
                "❌ No participants have joined yet! Can't end an empty loot.",
                ephemeral=True
            )
            return

        self.ended = True
        await interaction.response.defer()

        # Roll for each participant
        results: List[Tuple[discord.User, int]] = []
        for participant in self.participants:
            roll = random.randint(1, 100)
            results.append((participant, roll))

        # Sort by roll (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        winner = results[0]

        # Build results embed
        embed = discord.Embed(
            title=f"✅ Loot Complete: {self.item_name}",
            color=discord.Color.gold(),
            description="Rolling complete!"
        )

        # Add all participants and their rolls
        results_text = "\n".join(
            [f"**{i+1}.** {user.mention} - **{roll}**" 
             for i, (user, roll) in enumerate(results)]
        )
        embed.add_field(name="Participants & Rolls", value=results_text, inline=False)

        # Highlight winner
        embed.add_field(
            name="🏆 Winner",
            value=f"{winner[0].mention} with a roll of **{winner[1]}**!",
            inline=False
        )

        # Update the message with results
        await interaction.message.edit(
            content=None,  # Remove content to avoid duplication
            embed=embed,   # Embed contains all results and winner info
            view=None      # Remove buttons after ending
        )

    async def update_message(self, interaction: discord.Interaction):
        """Update the loot message with current participant count"""
        try:
            participant_list = "\n".join([f"• {user.mention}" for user in self.participants])
            content = f"**Loot: {self.item_name}**\n\nParticipants ({len(self.participants)}):\n{participant_list if participant_list else 'No participants yet'}"
            
            # Create a new embed (without participant count - it's in the content)
            embed = discord.Embed(
                title=f"🎲 Loot: {self.item_name}",
                description="Click the buttons below to join or end the loot!",
                color=discord.Color.blurple()
            )
            embed.set_footer(text="React with Join to participate in the loot roll")
            
            await interaction.message.edit(content=content, embed=embed, view=self)
        except Exception as e:
            print(f"Error updating message {self.message_id}: {e}")
            try:
                await interaction.response.send_message(
                    "❌ Could not update the loot message. Please make sure the bot has permission to edit messages.",
                    ephemeral=True
                )
            except Exception:
                pass


@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Connected to {len(bot.guilds)} server(s)")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
        for cmd in synced:
            print(f"  - /{cmd.name}: {cmd.description}")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")
        print("Make sure the bot has 'applications.commands' scope and proper permissions!")


@bot.tree.command(name="loot", description="Start a loot roll for an item")
@app_commands.describe(item="The name of the item to loot")
async def loot_command(interaction: discord.Interaction, item: str):
    """Start a loot session for an item"""
    
    # Defer the response to avoid timeout with emojis/special characters
    await interaction.response.defer()
    
    view = LootView(item, 0, interaction.user.id)  # Placeholder message_id, will be set after sending
    
    embed = discord.Embed(
        title=f"🎲 Loot: {item}",
        description="Click the buttons below to join or end the loot!",
        color=discord.Color.blurple()
    )
    embed.set_footer(text="React with Join to participate in the loot roll")
    
    initial_content = f"**Loot: {item}**\n\nParticipants (0):\nNo participants yet"
    
    # Use followup.send instead of response.send_message since we deferred
    await interaction.followup.send(content=initial_content, embed=embed, view=view)
    
    # Get the actual message ID and update the view
    message = await interaction.original_response()
    view.message_id = message.id
    loot_sessions[message.id] = {
        "item": item,
        "participants": view.participants,
        "ended": False,
        "view": view
    }


@bot.tree.command(name="ping", description="Check if the bot is alive")
async def ping_command(interaction: discord.Interaction):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")


@bot.tree.command(name="sync", description="Sync bot commands (Admin only)")
async def sync_command(interaction: discord.Interaction):
    """Manually sync slash commands"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need administrator permissions to use this command!", ephemeral=True)
        return

    await interaction.response.defer()
    try:
        synced = await bot.tree.sync()
        await interaction.followup.send(f"✅ Synced {len(synced)} command(s) successfully!")
    except Exception as e:
        await interaction.followup.send(f"❌ Failed to sync commands: {e}")


# Run the bot
if __name__ == "__main__":
    load_dotenv(".env")
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN environment variable is not set!")
    bot.run(TOKEN)
