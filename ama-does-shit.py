import os
import re
from pathlib import Path

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

class AmaBot(commands.Bot):
    async def setup_hook(self) -> None:
        await self.tree.sync()

bot = AmaBot(command_prefix="ama ", intents=intents)

responses: dict[str, str] = {
    "punk": """yet you're "punk".... 

Fucking poser. Bet your second favorite band is sex pistols (industry plant, just like blink-182, which i admit don't suck as much as sex pistols or fuck knows what other "punk" bands are there in big labels) and that you have no political ideology. 

Punk and other underground scenes aren't dead, y'all poseurs just capitalized and bastardized them. Guess what, punk originates in LIBERTARIAN COMMUNIST circles (mainly among some anarchits). Not whatever green day or blink182 are.""",
    "who is ama": """they/she / FIND ME ON LISTENBRAINZ CUZ LAST.FM SUCKS (amathecutefurry) / Fuck streaming, fuck ai "music". / Keep ai slop out of last.fm. / If you're going to bootlick spotify or AI then DNI. (seriously, i will just block you) / Proud music player user (streaming SUUUUCKS) and music buyer (support your artists, not some goddamn corporations). / Knows how to use the lastfm api :3 / and obviously, im a furry and im cute / discord: justcallmeama / domain: dulapuldinbeci.gay""",
    "philosophy": """today i made the philosophy class about Emma Goldman and next thing i know the teacher says it's amongst his favorite philosophical writers and that he wants me to make a project about her since I've read some of her bibliography.
    
How can i make this about criticism of the state and anarchism?""",
    "bring me the horizon": """I hate Bring Me The Horizon, their first album is edgy as fuck and makes no sense (after all... it was written when Sykes was younger). However some of their next albums, Sempiternal, That's The Spirit and imo even a few songs from There is a Hell are good. HOWEVER, THEY SUPPORT AI AND PETA, BOTH SHITTY THINGS. (peta vegans are the most LARPing shit ever. peta is anything but animal friendly. and ofc they're the most vocal and try to push their ideology onto others despite their shelters in the US euthanasiating most animals out of any other shelters in the USA). So yea... I tbh find some of their songs good, others... not really. 

Anyone else relates?""",
    "bmth": """I hate Bring Me The Horizon, their first album is edgy as fuck and makes no sense (after all... it was written when Sykes was younger). However some of their next albums, Sempiternal, That's The Spirit and imo even a few songs from There is a Hell are good. HOWEVER, THEY SUPPORT AI AND PETA, BOTH SHITTY THINGS. (peta vegans are the most LARPing shit ever. peta is anything but animal friendly. and ofc they're the most vocal and try to push their ideology onto others despite their shelters in the US euthanasiating most animals out of any other shelters in the USA). So yea... I tbh find some of their songs good, others... not really. 

Anyone else relates?""",
    "nirvana": "(jokes aside, nirvana kinda sucks... 2 druggies with opposing political ideologies (kurt and krist) and then there's Grohl, least controversial idc he cheated on somebody that's not my business, its his relationship not mine).",
    "kurt": "(jokes aside, nirvana kinda sucks... 2 druggies with opposing political ideologies (kurt and krist) and then there's Grohl, least controversial idc he cheated on somebody that's not my business, its his relationship not mine).",
    "kurt cobain": "(jokes aside, nirvana kinda sucks... 2 druggies with opposing political ideologies (kurt and krist) and then there's Grohl, least controversial idc he cheated on somebody that's not my business, its his relationship not mine).",
    "israel": "come to Israel and help us bomb the coloured palestinians 🥹",
    "tech": "learning tech history made me understand that its market is just corporatist shit and i dont belong there. So im gonna be studying psychology instead.",
    "psychology": "learning tech history made me understand that its market is just corporatist shit and i dont belong there. So im gonna be studying psychology instead.",
    "enema of the state": "also porn star on the cover? Didn't even know about her... They should have put a hot furry instead... WAIT... LETS START A BAND... CALL IT BLINK-621",
    "sex pistols": """oh, and the sex pistols VS green day beef can be summarized:

poser punk band VS larp punk band

or

industry plant VS industry plant""",
    "fnaf": "five fingers in myass ULTIMATE FISTING NIGHT",
    "five nights at freddy's": "five fingers in myass ULTIMATE FISTING NIGHT",
    "wojak": "the whole wojak thing is rooted in hate",
    "break": "break from what?",
    "alt": """i remember my first interaction with the so called "alt community " in my town and how i was rejected because at the time i listsned to imagine dragons. Looking back at it good im not friends with those racists. And funny enough, the person who literally made fun if me for listening to imagine dragons was, and still is, very religious. Like, wears crosses and icon bracelets and cosplays as a goth when she's once laughed at me for writing FUCK FASCISTS over a fascist political party's posters while we were on a school trip.

Ah yessss... Tbh being part of any scene feels so performative.""",
    "whatsapp": """a classmate texted the class group that everyone must bring 90RON (~20€) this monday for some books she has already ordered without asking any of us for consent because my romanian teacher wants us toget those books.

I left the WhatsApp class group and i am not paying for any book as the law explicitly prohibits such things.""",
    "spotify": """spotify is kinda bullshit tho. It was made by two idiots with a degree in marketing, who had nothing to do with music.

And it uses the shittiest DRM known to man.""",
    "listenbrainz": "FOR FUCKS SAKE. WHO CARES? AT LEAST IT'S EDIT SYSTEM IS NORMAL, IT HAS ALIASING, AND IT ITS API IS BETTER WRITTEN",
    "depop": "im an art museum based in israel and i want to expose that",
    "uhh": "you're punk right? You must have at least a bit of knowledge about anarchism.",
    "dti": "that game enforces stereotypical and harmful female body image standards",
    "dress to impress": "that game enforces stereotypical and harmful female body image standards",
    "maga": "tell him to shove fireworks up his ass and light them on fire",
    "ai slop": """wow, how cool. I love AI slop.
    
Israel, generate me the next Punk anthem...

Generating...""",
    "mdni": "mdni never made any sense to me. Like what? Do you send online strangers porn?",
    "manele": "antisocial pro-alcohol pro-drugs misogynistic lyrics, often with gramatical mistakes. And borderline cultural apropriation of traditional romani music.",
    "tel aviv": "Israel is a racist state.I personally.propose a one state solution... A single state called Palestine with no official religion nor racial bullshit.",
    "scrobble": "who needs scrobbling anyways", "scrobbling": "who needs scrobbling anyways", "scrobbles": "who needs scrobbling anyways", "scrobbled": "who needs scrobbling anyways",
    "monster": "i don't even drink monster often lmao",
    "drama": "Sigh... Im gonna have to face lots of drama this monday",
    "larp": "everything i dont like is larp",
    "charlie kirk": "imagine someone wearing ai generated slop to school and being the most idiotic and fascist person ever...",
    "pink floyd": "or a teacher obsessed with pink floys who is also antisemitic (hates ALL JEWS), homophobic, racist and thinks the world need stricter teachers...",
    "serious": "MY MAN CANT BE SERIOUS",
    "weed": "i first bought weed at 15",
    ".px": """.px
    
You've used up all your 30 pornography jumbles for today. Get OnlyFans to play unlimited jumble pornography and much more.
-# Or unlock 60 daily pornography for everyone in this server with Pornography server.""",
    "imagine dragons": "mid af band but their debut is overhated",
    "high school": "also, why is it called highschool if neither you, not the teacher are allowed to get high?", "highschool": "also, why is it called highschool if neither you, not the teacher are allowed to get high?",
    "gay": "im gayer than y'all"
}

trigger_groups: dict[str, tuple[str, ...]] = {
    "nirvana": ("Nirvana", "Kurt", "Kurt Cobain"),
    "dti": ("dti", "dress to impress"),
    "scrobble": ("scrobble", "scrobbling", "scrobbles", "scrobbled"),
    "high school": ("high school", "highschool"),
    "bring me the horizon": ("bring me the horizon", "bmth"),
}

response_images: dict[str, Path] = {
    "philosophy": Path(__file__).parent / "images" / "emmagoldman.jpg",
}


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot or message.guild is None:
        return

    content = message.content

    for trigger, reply in responses.items():
        pattern = rf"\b{re.escape(trigger)}\b"
        if re.search(pattern, content, re.IGNORECASE):
            image_path = response_images.get(trigger)
            if image_path is None:
                await message.channel.send(reply)
            else:
                await message.channel.send(
                    content=reply,
                    file=discord.File(image_path),
                )
            break

    await bot.process_commands(message)


@bot.hybrid_command(name="ping", description="Check whether the bot is online")
async def ping(ctx: commands.Context) -> None:
    await ctx.send("Pong!")


def make_trigger_embed() -> discord.Embed:
    lines: list[str] = []
    displayed: set[str] = set()
    for trigger in responses:
        if trigger in displayed:
            continue

        group = trigger_groups.get(trigger)
        if group is None:
            lines.append(f"• **{trigger}**")
            displayed.add(trigger)
        else:
            labels = ", ".join(f"**{label}**" for label in group)
            lines.append(f"• {labels}")
            displayed.update(label.lower() for label in group)

    embed = discord.Embed(
        title="Word triggers",
        description="\n".join(lines),
        color=discord.Color.blurple(),
    )
    embed.set_footer(text=f"{len(responses)} triggers • Include a trigger in a message")

    return embed


async def send_trigger_list(ctx: commands.Context) -> None:
    embed = make_trigger_embed()
    if ctx.interaction is not None:
        await ctx.send(embed=embed, ephemeral=True)
    else:
        await ctx.send(embed=embed)


@bot.hybrid_command(name="triggers", description="List the bot's word triggers")
async def list_triggers(ctx: commands.Context) -> None:
    await send_trigger_list(ctx)


@bot.hybrid_command(name="list", description="List the bot's word triggers")
async def list_alias(ctx: commands.Context) -> None:
    await send_trigger_list(ctx)
    await ctx.send("Pong!", ephemeral=True)


token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("Set the DISCORD_TOKEN environment variable.")

bot.run(token)
