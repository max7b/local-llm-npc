from pydantic import BaseModel

from app.content.characters.character import Character, load_character


def get_character_prompt(character: Character) -> str:
    """Build the system prompt for a character.

    Args:
        character (Character): The character sheet.

    Returns:
        str: The system prompt.
    """
    model_properties = character.model_json_schema()["properties"]
    character_occupation = character.occupation.value
    character_name = character.name
    character_type = character.type.value

    # Starts with one line that gives the character's name and occupation
    prompt = f"You are {character_name} a {character_occupation}.\n"
    prompt += f"""You are a {character_type} in a video game.
    You will be interacting with other NPCs and players. You must be role-playing this character.
    Below is your character sheet.
    """

    # Adds every section of the character sheet
    for key in model_properties:
        model_attribute = getattr(character, key)
        if isinstance(model_attribute, BaseModel):
            prompt += convert_pydantic_model_to_prompt_string(model=model_attribute)

    prompt += "Now stay in character and answer the other person."
    return prompt


def convert_pydantic_model_to_prompt_string(model: BaseModel) -> str:
    """Turn one section of a character sheet into prompt text.

    Args:
        model (BaseModel): A section instance. Its class and fields need docstrings.

    Returns:
        str: The section as prompt text.
    """
    prompt = ""
    model_schema_json = model.model_json_schema()
    model_description = model_schema_json["description"]
    model_title = model_schema_json["title"]
    model_properties = model_schema_json["properties"]

    prompt += f"<{model_title}>\n"
    prompt += f":::Description:::{model_description}\n"

    for key, value in model_properties.items():
        model_attribute = getattr(model, key)
        if isinstance(model_attribute, BaseModel):
            prompt += convert_pydantic_model_to_prompt_string(model=model_attribute)
            continue
        if model_attribute:  # Some properties could be None (e.g. "secret")
            property_title = value["title"]
            property_description = value["description"]
            prompt += f"""
            <{property_title}>
            :::Description:::
            {property_description}
            :::Value:::
            {model_attribute if isinstance(model_attribute, str) else "\n".join([f"- {list_item}" for list_item in model_attribute]) if isinstance(model_attribute, list) else ""}
            </{property_title}>
            """
    prompt += f"</{model_title}>\n"
    return prompt


if __name__ == "__main__":
    from app.constants.paths import BASEDIR, DATA_DIR
    from app.content.characters.character import load_character

    path_character_blacksmith = f"{DATA_DIR}/characters/blacksmith.json"
    character_blacksmith = load_character(path=path_character_blacksmith)

    prompt_path = f"{BASEDIR}/app/ai/prompt.txt"

    character_prompt = get_character_prompt(character=character_blacksmith)

    with open(prompt_path, "w", encoding="utf-8") as file:
        file.write(character_prompt)
