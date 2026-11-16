import json
import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import httpx
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.ai.prompt import get_character_prompt
from app.constants.paths import DATA_DIR
from app.constants.vendor import VendorType, mapping_vendor_type_to_path_assets
from app.content.characters.character import load_character

router = APIRouter()

path_stored_conversations = f"{DATA_DIR}/conversations/"
os.makedirs(os.path.dirname(path_stored_conversations), exist_ok=True)


class TalkRequest(BaseModel):
    """What a client sends to talk to a character.

    Attributes:
        vendor_type (VendorType): The occupation of the character to talk to.
        query (str): What the player says to the character.
    """

    vendor_type: VendorType
    query: str
    talk_id: str = Field(default_factory=lambda: uuid4().hex)


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

    path_talk_memory = sorted(Path(f"{path_stored_conversations}").glob(f"*{talk_request.talk_id}.json"))
    if path_talk_memory:
        path_talk_memory = path_talk_memory[0]
        with open(path_talk_memory) as f:
            memory_content = json.load(f)
            data_messages = [*memory_content, {"role": "user", "content": talk_request.query}]
    else:
        path_talk_memory = (
            f"{path_stored_conversations}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{talk_request.talk_id}.json"
        )
        data_messages = [
            {"role": "system", "content": character_prompt},
            {"role": "user", "content": talk_request.query},
        ]

    llamacpp_url = "http://localhost:9931/v1/chat/completions"
    data = {"messages": data_messages}

    request = httpx.post(llamacpp_url, json=data)
    request_content = request.json()["choices"][0]["message"]["content"]

    with open(path_talk_memory, "w") as f:
        data_messages += [{"role": "assistant", "content": request_content}]
        json.dump(data_messages, f)

    return request_content
