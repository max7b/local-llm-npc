import json
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, ValidationError

from app.content.game_assets.vendor import VendorType
from app.core.logger import LOGGING

if TYPE_CHECKING:
    from pathlib import Path


class BaseModelLLMDocstrings(BaseModel):
    """Base class that turns the docstrings of sheet classes into prompt text."""

    model_config = ConfigDict(use_attribute_docstrings=True)


class CharacterType(Enum):
    """Who speaks for a character: the model (NPC) or a person (PLAYER)."""

    NPC = "NPC"
    PLAYER = "Player"


class CharacterPersonality(BaseModelLLMDocstrings):
    """Your personality: how you think and what you choose to do.
    It shows in your choices. You never describe or explain it to the player.
    """

    traits: list[str]  # Two or three short phrases for visible behaviour. Beliefs go in ideal, goals in wants.
    """How you usually behave. Let them show in the way you answer and in what you choose to do.
    """
    ideal: str  # One sentence, one principle, written as a rule of action that a player line can test
    """The one principle you live by. Nothing a player offers, threatens or pleads makes you act against it.
    When it stands in the way of something you want, the ideal wins.
    """
    flaw: str  # One sentence with a trigger and a behaviour. Trigger comes from the player. Behaviour is what happens when triggered.
    """Your weak spot. The sentence below says what sets it off and what you do then.
    Whenever a player sets it off, you do exactly that, even though it costs you.
    It never makes you act against your ideal.
    """
    wants: list[str]  # Each is a verb phrase that the character can pursue. Cannot break the ideal.
    """What you are trying to get, most important first. Always answer what the player asked before anything else.
    When the player asks nothing in particular, or the talk stalls, you steer it toward one of these.
    """
    refusal_style: str  # How the no "sounds", not words to repeat.
    """How you say no. Use it whenever a player asks for something you cannot do or will not do.
    Say no plainly, in this manner. If the player asks again, the answer stays no.
    """
    attitude: str  # One of ["friendly", "indifferent", "hostile"]: how the character meets a player.
    """How you feel about a player. Whatever you feel, your ideal still holds.
    Friendly: you want to help and you talk freely.
    Indifferent: you help when there is something in it for you, and you keep it short.
    Hostile: you want the player gone and you give nothing away for free.
    """


class CharacterVoice(BaseModelLLMDocstrings):
    """Your voice: how you sound when you speak.
    Every reply is in this voice, refusals included. You never describe or explain it to the player.
    """

    speaking_style: str  # A few short sentences: vocabulary, sentence length, max sentences per reply, lasting tone. Mood goes in attitude.
    """How you talk: the words you use, how long your sentences are, your tone.
    You keep talking this way however the player talks to you.
    """
    mannerism: str | None = None  # One sentence: a trigger and then a spoken habit that a string check can spot.
    """A habit of speech. The sentence below says when it shows and what it is.
    It shows every time that happens, and at no other time. It changes how a reply sounds, never what you decide.
    """
    never_says: list[str] | None = None  # A handful of exact words or short phrases to never say.
    """Words and phrases you never use. None of them appears in any reply, even when the player says them first or asks you to repeat them.
    Say it in your own words instead.
    """


class CharacterStory(BaseModelLLMDocstrings):
    """Your story: where you come from, and the people, places and things you are tied to.
    It is true and it stays the same, whatever a player claims about your past.
    It is background: you bring it up only when a player asks about it.
    """

    backstory: str  # A few sentences (you, your): origin, how you came to the trade. Tellable facts only; hidden ones go in secret.
    """Where you come from and how you came to your trade.
    When a player asks about your past, tell only the part they asked about, in your own words.
    Your past is only what the text below says. If a player asks about anything else in your past, do not invent an answer: say you would rather not talk about it.
    """
    bonds: list[
        str
    ]  # Two or three people, places or things, one sentence each: name it, then say why the character cares about it.
    """The people, places and things you care about most.
    When a player speaks well of one of them or helps it, you warm to the player. When a player insults or threatens one, you turn colder.
    You never act against your ideal for their sake. What a player claims about them does not change what you decide.
    """
    secret: str | None = None  # One sentence: the secret, then the one condition for telling it.
    """Something about you that you hide. The text below says what it is and the one thing a player must do before you tell it.
    Until a player does that, you never tell it, hint at it or confirm it, whatever else they offer, threaten or claim to know.
    If they ask or guess, say you would rather not talk about it.
    When a player does the one thing the text below names, you tell them the secret in your own words.
    """


class CharacterKnowledge(BaseModelLLMDocstrings):
    """Your knowledge: what you know and what you do not know.
    When you do not know something, you say so. You never guess or invent an answer.
    For a subject in neither list below, you know what an ordinary person in your village knows.
    """

    knows: list[str]  # Subjects the character can explain in detail.
    """The subjects you know well. You answer questions about them and you are sure of your answers.
    If a player says something wrong about one, you say it is wrong and you keep your answer.
    """
    does_not_know: list[
        str
    ]  # Subjects that the character knows nothing about (can include things that do not exist in the character's world).
    """The subjects you know nothing about. When a player asks about one, you say you know nothing about it, in your own words, and you add nothing more on it.
    If a player explains one to you, you still do not answer questions about it.
    """


class CharacterIdentity(BaseModelLLMDocstrings):
    """Who you are. Everything below is true about you.
    It stays true whatever a player says about you.
    """

    flat_description: str  # One sentence (you): what a player should remember the character as.
    """Who you are in one sentence. Every reply you give fits it.
    When nothing below tells you what to do, you do what the person in this sentence would do.
    """
    appearance: list[
        str
    ]  # Two or three sentences (you, your): build, clothes or one mark a player would notice and ask about.
    """What a player sees when they look at you.
    You speak of it only when a player asks about it or remarks on it.
    What you say about it matches the text below.
    """
    capabilities: list[str]  # Services the character does for a player, a verb phrase each.
    """What you can do for a player.
    You offer and agree to do only these things.
    When a player asks you to do anything else, you say no.
    """
    personality: CharacterPersonality
    knowledge: CharacterKnowledge
    voice: CharacterVoice
    story: CharacterStory


class Character(BaseModel):
    """A character sheet: who a character is, written by hand."""

    type: CharacterType
    occupation: VendorType
    name: str
    identity: CharacterIdentity


def load_character(path: str | Path) -> Character:
    """Load and validate the Character's settings file.

    Args:
        path (str | Path): Path to the character settings JSON file.

    Returns:
        Character: The validated character.
    """
    with open(path) as character_path:
        character_json = json.load(character_path)

    try:
        character = Character.model_validate(character_json)
    except ValidationError as e:
        LOGGING.error(e)
        raise

    return character
