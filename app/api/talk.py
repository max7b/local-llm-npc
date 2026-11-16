import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.prompt import get_character_prompt
from app.constants.vendor import VendorType, mapping_vendor_type_to_path_assets
from app.content.characters.character import load_character

router = APIRouter()


class TalkRequest(BaseModel):
    """What a client sends to talk to a character.

    Attributes:
        vendor_type (VendorType): The occupation of the character to talk to.
        query (str): What the player says to the character.
    """

    vendor_type: VendorType
    query: str


@router.post("/talk/")
async def talk(talk_request: TalkRequest) -> str:
    """Send one player line to a character and return the character's reply.

    Args:
        talk_request (TalkRequest): The character to talk to and the player's line.

    Returns:
        str: The character's reply.
    """
    character = load_character(path=mapping_vendor_type_to_path_assets[talk_request.vendor_type])
    character_prompt = get_character_prompt(character=character)

    llamacpp_url = "http://localhost:9931/v1/chat/completions"
    data = {
        "messages": [{"role": "system", "content": character_prompt}, {"role": "user", "content": talk_request.query}]
    }

    request = httpx.post(llamacpp_url, json=data)

    return request.json()["choices"][0]["message"]["content"]
