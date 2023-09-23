## Overview

An interactive story generator built using ChatGPT on the backend. How to use:

- Decide a cast of characters first, with short paragraphs describing who they are and their personalities. (This is hardcoded currently, so you'll have to change this in the code)
- The story will progress one response at a time according to your prompt and your chosen character perspective.
- The generator will involve your characters, and make the story progress in a way that maintains continuity with the story so far.
- The characters will maintain their respective personalities in their dialog and actions according to your given (hardcoded) personalities.

## Demo



https://github.com/nfvdat/story-generator/assets/139157490/95790446-1aaa-4e30-a92f-80e1987109a6



## How to Run

First set up dependencies in a virtual environment:

```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then set the variable `OPENAI_API_KEY` in the `.env` file. If you don't have a key, make an OpenAI account and generate one there. Finally, run:

```
flask run
```
