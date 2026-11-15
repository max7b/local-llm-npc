# Villager NPC LLM

Stack :
- llama.cpp for serving the model.


## HOW TO :

```bash
llama serve -hf ggml-org/Qwen3.5-4B-GGUF --no-mmproj -c 8192 --reasoning off -v
```

- ggml-org = official llama.cpp quantizer
- `-c` context size 8192 should be enough
- `--reasoning` off, let's try that for now and see speed/performance
- `--no-mmproj` text-only, no multimodal projection
- `-v` to debug fully

## DATA :

GameAssets are taken from [welevel/GameAssets](https://github.com/welevel/GameAssets).
