# Villager NPC LLM

Stack :
- llama.cpp for serving the model.


## HOW TO :

### Llama.cpp

```bash
llama serve -hf ggml-org/Qwen3.5-4B-GGUF --no-mmproj -c 8192 --reasoning off -v
```

- ggml-org = official llama.cpp quantizer
- `-c` context size 8192 should be enough
- `--reasoning` off, let's try that for now and see speed/performance
- `--no-mmproj` text-only, no multimodal projection
- `-v` to debug fully

To interact with the model : [OpenAI-compatible API Endpoints](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md#api-endpoints)


- [`POST /v1/chat/completions`](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md#post-v1chatcompletions-openai-compatible-chat-completions-api) **[Using in this repo]** easier to work with : takes a list of messages with roles (`system`, `user`, `assistant`) and applies the chat template
- `POST /v1/completion` just take a raw string and complete it. Using this means working around the model's own chat template.

### Fastapi

`poetry run fastapi dev`

## DATA :

GameAssets are taken from [welevel/GameAssets](https://github.com/welevel/GameAssets).
