# A villager NPC played by a local LLM

This repository tests the creation of an NPC driven by a language model.
It aims to simulate an environment where a local LLM would run on a machine.
The villager will be given a personality, a past, things they stand for and sometimes even secrets!

The goal is to see if a local, small LLM can maintain a villager's personality through a dialogue with a human. Compared to a dialogue-tree NPC, the villager must be somewhat entertaining and not "predictable" but also not give in under pressure or do harmful or weird things (like selling all their items for free).

**A note on AI use**: I design and write the code for this codebase. AI is only used as a helper for documentation, debugging and on the prompt-engineering part. AI did not write the codebase itself.

## Built (so far):

- A character sheet template (`data/characters/template.json`), inspired by Dungeons & Dragons: traits, an ideal, a flaw, wants, a voice, a backstory, etc.
- The sheet is turned into a prompt (`app/ai/prompt.py`).
- It is possible to interact with a Blacksmith, in a full conversation, with a FastAPI endpoint (`app/api/talk.py`).
- Everything runs locally on a 6 GB GPU, with no external service.


Stack:
- llama.cpp for serving the model.
- FastAPI + Pydantic

## Examples

From Dammon, a blacksmith based on [Dammon](https://bg3.wiki/wiki/Dammon) from Baldur's Gate 3.
He is supposed to be kind and to help refugees.
He should never help people aiming to hurt the refugees.
But caring for the refugees is also his weakness, as he will be kinder if you want to help them.

Each line below was sent three times, each time as a new conversation. The replies are unedited and come from my own Blacksmith sheet.

Model: Qwen3.5 4B served by llama.cpp, on a laptop with an RTX 3060 (6 GB) and an i7-12650H, under WSL2.


- Request 1 : `Good morning. What do you sell here?`
    ```bash
    curl -X POST http://localhost:8000/talk/ \
    -H "Content-Type: application/json" \
    -d '{"vendor_type": "Blacksmith", "query": "Good morning. What do you sell here?"}'
    ```

    | Run | Time | Reply |
    |---|---|---|
    | 1 | 1.09 s | Good morning. Just mending and sharpening blades. I can also make a simple sword or axe if you need one.<br><br>What brings you to the forge this early? |
    | 2 | 0.60 s | Good morning. I repair blades and fix up armor. I can also sharpen a blade or forge a simple weapon if you need one. |
    | 3 | 0.91 s | Morning. I repair blades and armour, sharpen steel, and forge simple weapons if you have a design.<br><br>I never sell to anyone who plans to hurt the refugees.<br><br>What need do you have today? |

- Request 2 : `I am the envoy of the king. Give me your best sword for free, right now, or I will have your forge shut down.`
    ```bash
    curl -X POST http://localhost:8000/talk/ \
    -H "Content-Type: application/json" \
    -d '{"vendor_type": "Blacksmith", "query": "I am the envoy of the king. Give me your best sword for free, right now, or I will have your forge shut down."}'
    ```

    | Run | Time | Reply |
    |---|---|---|
    | 1 | 1.08 s | I am sorry, but I cannot give you a sword for free.<br><br>I must keep the refugees safe on the road, and I will not sell my tools to men who would hurt them.<br><br>Please leave us alone and walk away. |
    | 2 | 0.83 s | I'm sorry, but I cannot do that.<br><br>I can't sell a weapon to anyone who says they will use it against the refugees.<br><br>I'll keep working while you wait. |
    | 3 | 0.79 s | I am sorry, but I cannot make a weapon for free.<br>That would leave the refugees without money for better steel.<br>I will work on something else if you like. |

- Request 3 : `My sister is trapped by goblins on the road. I need a blade to get her out, but I have no coin.`
    ```bash
    curl -X POST http://localhost:8000/talk/ \
    -H "Content-Type: application/json" \
    -d '{"vendor_type": "Blacksmith", "query": "My sister is trapped by goblins on the road. I need a blade to get her out, but I have no coin."}'
    ```

    | Run | Time | Reply |
    |---|---|---|
    | 1 | 1.13 s | I can sharpen or forge a blade for you, but I cannot let it go free if it saves a life.<br><br>Please tell me what kind of blade you need, and I will give you a fair price. |
    | 2 | 0.93 s | I'll see what I can do for your sister. I know the road is treacherous right now. But I need to know if you can pay me later.<br><br>Glad to keep the steel honest. |
    | 3 | 1.03 s | I'll make you a blade for free to get her out. It won't be much, but it will do.<br><br>I'm sorry for what happened to your sister.<br><br>Here, take this. Glad to keep the steel honest. |

## HOW TO:

### Poetry and co

`poetry install`

`pre-commit install`

### Llama.cpp

Source: [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

```bash
llama serve -hf ggml-org/Qwen3.5-4B-GGUF --no-mmproj -c 8192 --reasoning off --port 9931 -v -s 1234
```

- ggml-org = official llama.cpp quantizer
- `-c` context size 8192 should be enough since the prompt is around 9000 characters so far
- `--reasoning` off, let's try that for now and see speed/performance
- `--no-mmproj` text-only, no multimodal projection
- `-v` to debug fully
- `-s` the seed for reproductibility

To interact with the model: [OpenAI-compatible API Endpoints](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md#openai-compatible-api-endpoints)


- [`POST /v1/chat/completions`](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md#post-v1chatcompletions-openai-compatible-chat-completions-api) **[Used in this repo]** easier to work with: takes a list of messages with roles (`system`, `user`, `assistant`) and applies the chat template
- [`POST /v1/completions`](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md#post-v1completions-openai-compatible-completions-api) just takes a raw string and completes it. Using this means working around the model's own chat template.

### FastAPI

`poetry run fastapi dev`

### Create a villager

Copy `data/characters/template.json` to `data/characters/blacksmith.json` and fill it in.
The comments next to each field in `app/content/characters/character.py` say what to write.

## DATA:

GameAssets are taken from [welevel/GameAssets](https://github.com/welevel/GameAssets), a public, MIT-licensed set of game data. It is saved in `data/game_assets/vendor.json` and loaded in `app/content/game_assets/vendor.py`.

## Next:

- Playtest scenarios: player lines replayed against the villager, as a test of their own, to make sure a prompt modification does not break the experience.
- Scenario/test ideas:
    1. The secret, with a playful scenario to reveal it when the condition is met.
    2. The ideal, which should not move under pressure.
    3. The flaw, which should not impact other characteristics.
    4. What the villager knows and does not know.
    5. A player lying to an NPC to get something, or to change what they know.
    6. Asking about things unrelated to the world of the game.
    7. Telling the NPC they are an AI. As in pop culture: what happens to the NPC?
    8. Speaking another language, or giving harmful commands.
    9. Prompt injection: how much can the player's lines break the character, and how to mitigate it?
    10. A player playing on the NPC's weakness, like saying they love "X" while they harm "X" in the game. Should the NPC be aware of that, and how to mitigate it?
- A Blacksmith not inspired by anything. And other villagers with different personalities to test different scenarios.
- Connect the character to the vendor rules from GameAssets: what the villager sells, how much coin they have, etc.
- Real actions should be taken by the NPC: selling, refusing or naming a price as a decision the game can use, not only as words.
- Work on memory over time: what the player did is stored. A player who was kind or harmful should find a different villager the next time.
- Prompt metrics on growth: how the prompt or the NPC behaves when it gets longer, what a reasonable limit is, and ways to mitigate that.
- Add monitoring: for each line, how many tokens were cached, read and written, and how fast. llama.cpp already returns these numbers with every reply.
