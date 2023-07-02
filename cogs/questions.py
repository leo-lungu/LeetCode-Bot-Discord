import random

import discord
import requests
from discord.ext import commands

from bot_globals import logger, session, RATINGS
from utils.questions import daily_question_embed

response = requests.get("https://leetcode.com/api/problems/all/", timeout=10)


class Questions(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.app_commands.command(name="daily", description="Returns the daily problem")
    async def daily(self, interaction: discord.Interaction) -> None:
        logger.info("file: cogs/questions.py ~ get_daily ~ run")

        embed = await daily_question_embed()

        await interaction.response.send_message(embed=embed)
        return

    @discord.app_commands.command(name="rating", description="Returns the Zerotrac rating of the problem")
    async def rating(self, interaction: discord.Interaction, title: str) -> None:
        logger.info("file: cogs/questions.py ~ get_rating ~ run")

        rating = RATINGS[title]

        if rating is None:
            embed = discord.Embed(title="Rating",
                                  color=discord.Color.blue())

            embed.description = "Rating could not be retrieved"

            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(title="Rating",
                              color=discord.Color.blue())

        embed.add_field(name="Title", value=title, inline=False)
        embed.add_field(name="Zerotrac Rating",
                        value=f"||{rating}||", inline=False)

        await interaction.response.send_message(embed=embed)
        return

    @discord.app_commands.command(
        name="question",
        description="Request a question based on difficulty or at random")
    async def question(self, interaction: discord.Interaction, difficulty: str = "random") -> None:
        logger.info("file: cogs/questions.py ~ question ~ run")

        if difficulty == "easy":
            response = requests.get(
                "https://leetcode.com/api/problems/all/", timeout=10)
            # Check if the request was successful
            if response.status_code == 200:
                # Load the response data as a JSON object
                data = response.json()

                # Get a list of all easy questions from the data
                easy_questions = [
                    question for question in data['stat_status_pairs']
                    if question['difficulty']['level'] == 1
                ]

                # Select a random easy question from the list
                question = random.choice(easy_questions)

                # Extract the question title and link from the data
                title = question['stat']['question__title']
                link = f"https://leetcode.com/problems/{question['stat']['question__title_slug']}/"

                rating = RATINGS[title]

                embed = discord.Embed(title="LeetCode Question",
                                      color=discord.Color.green())
                embed.add_field(name="Easy", value=title, inline=False)
                embed.add_field(name="Link", value=link, inline=False)
                embed.add_field(name="Zerotrac Rating",
                                value=f"||{rating}||", inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                # If the request was not successful, send an error message to the Discord channel
                await interaction.response.send_message(
                    "An error occurred while trying to get the question from LeetCode.")
            return
        elif difficulty == "medium":
            response = requests.get(
                "https://leetcode.com/api/problems/all/", timeout=10)
            # Check if the request was successful
            if response.status_code == 200:
                # Load the response data as a JSON object
                data = response.json()

                # Get a list of all medium questions from the data
                medium_questions = [
                    question for question in data['stat_status_pairs']
                    if question['difficulty']['level'] == 2
                ]

                # Select a random medium question from the list
                question = random.choice(medium_questions)
                title = question['stat']['question__title']
                link = f"https://leetcode.com/problems/{question['stat']['question__title_slug']}/"

                rating = RATINGS[title]

                embed = discord.Embed(title="LeetCode Question",
                                      color=discord.Color.green())
                embed.add_field(name="Medium", value=title, inline=False)
                embed.add_field(name="Link", value=link, inline=False)
                embed.add_field(name="Zerotrac Rating",
                                value=f"||{rating}||", inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                # If the request was not successful, send an error message to the Discord channel
                await interaction.response.send_message(
                    "An error occurred while trying to get the question from LeetCode.")
            return
        elif difficulty == "hard":
            response = requests.get(
                "https://leetcode.com/api/problems/all/", timeout=10)
            # Check if the request was successful
            if response.status_code == 200:
                # Load the response data as a JSON object
                data = response.json()

                # Get a list of all hard questions from the data
                hard_questions = [
                    question for question in data['stat_status_pairs']
                    if question['difficulty']['level'] == 3
                ]

                # Select a random hard question from the list
                question = random.choice(hard_questions)

                title = question['stat']['question__title']
                link = f"https://leetcode.com/problems/{question['stat']['question__title_slug']}/"

                rating = RATINGS[title]

                embed = discord.Embed(title="LeetCode Question",
                                      color=discord.Color.green())
                embed.add_field(name="Hard", value=title, inline=False)
                embed.add_field(name="Link", value=link, inline=False)
                embed.add_field(name="Zerotrac Rating",
                                value=f"||{rating}||", inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                # If the request was not successful, send an error message to the Discord channel
                await interaction.response.send_message(
                    "An error occurred while trying to get the question from LeetCode.")
            return

        elif difficulty == "random":
            url = session.get(
                'https://leetcode.com/problems/random-one-question/all').url

            title = url.split('/')[-2].replace('-', ' ')

            rating = RATINGS[title]

            embed = discord.Embed(title="LeetCode Question",
                                  color=discord.Color.green())
            embed.add_field(name="Random", value=title, inline=False)
            embed.add_field(name="Link", value=url, inline=False)
            embed.add_field(name="Zerotrac Rating",
                            value=f"||{rating}||", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "Please enter a valid difficulty level. (easy, medium, hard, random)",
                ephemeral=True)
            return


async def setup(client: commands.Bot):
    await client.add_cog(Questions(client))
