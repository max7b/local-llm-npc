import json
import os
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

import httpx
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.ai.prompt import get_character_prompt
from app.constants.envs import settings
from app.constants.paths import PATH_STORED_CONVERSATIONS
from app.constants.vendor import VendorType, mapping_vendor_type_to_path_assets
from app.content.characters.character import load_character

router = APIRouter()


class TalkRequest(BaseModel):
    """What a client sends to talk to a character.

    Attributes:
        vendor_type (VendorType): The occupation of the character to talk to.
        query (str): What the player says to the character.
        talk_id (UUID): The conversation to continue. A new one is created if not given.
    """

    vendor_type: VendorType
    query: str
    talk_id: UUID = Field(default_factory=uuid4)


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

    data_messages, path_talk_memory = load_memory_data_messages(
        talk_request=talk_request, character_prompt=character_prompt
    )

    data = {"messages": data_messages}

    request = httpx.post(settings.LLAMACPP_URL, json=data)
    request_content = request.json()["choices"][0]["message"]["content"]

    save_memory_data_messages(
        data_messages=data_messages, request_content=request_content, path_talk_memory=path_talk_memory
    )

    return request_content


def load_memory_data_messages(
    talk_request: TalkRequest, character_prompt: str
) -> tuple[list[dict[str, str]], Path | str]:
    """Build the messages to send to the model for this turn. Load an already existing conversation to continue from it.

    Args:
        talk_request (TalkRequest): The talk id and the player's line.
        character_prompt (str): The system prompt, used only when the conversation is new.

    Returns:
        tuple[list[dict[str, str]], Path | str]: The messages to send, and the path of the
            file where the conversation is stored or will be stored.
    """
    path_talk_memory = sorted(Path(f"{PATH_STORED_CONVERSATIONS}").glob(f"*{talk_request.talk_id.hex}.json"))
    if path_talk_memory:
        path_talk_memory = path_talk_memory[0]
        with open(path_talk_memory) as f:
            memory_content = json.load(f)
            data_messages = [*memory_content, {"role": "user", "content": talk_request.query}]
    else:
        path_talk_memory = (
            f"{PATH_STORED_CONVERSATIONS}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{talk_request.talk_id.hex}.json"
        )
        data_messages = [
            {"role": "system", "content": character_prompt},
            {"role": "user", "content": talk_request.query},
        ]
    return data_messages, path_talk_memory


def save_memory_data_messages(
    data_messages: list[dict[str, str]], request_content: str, path_talk_memory: Path | str
) -> None:
    """Add the character's reply to the conversation and write it to disk.

    Args:
        data_messages (list[dict[str, str]]): The messages sent to the model.
        request_content (str): The character's reply.
        path_talk_memory (Path | str): The file where the conversation is stored.
    """
    os.makedirs(os.path.dirname(PATH_STORED_CONVERSATIONS), exist_ok=True)
    with open(path_talk_memory, "w") as f:
        data_messages += [{"role": "assistant", "content": request_content}]
        json.dump(data_messages, f)
