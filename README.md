# streamlit-botgen

BotGen is a small Streamlit app for building and editing a chatbot's training set by hand. You add prompt/response pairs through a web form, review them, edit them by index, and delete them. Everything is stored as a flat JSON list in `data/prompts.json`. The checked-in data file holds behavioral interview questions and STAR-format answers, which is what the app was originally used for.

One thing to be clear about: the "Train Your Chatbot" button does not train anything. It runs a progress bar for about five seconds and prints a success message. There is no model, no API call, and no inference code in this repo. The app is a CRUD editor for the training data, not a chatbot.

## Features

- Add a prompt/response pair through a form
- View the whole dataset as JSON in the app
- Update a pair by its list index
- Delete a pair by its list index
- Data persisted to a single JSON file on disk
- A standalone `JSONFileCRUD` class in `logic/jsoncrud.py` that does the same create/read/update/delete against any JSON file
- Makefile and GitHub Actions workflow for formatting and linting

## Requirements

- Python 3
- `streamlit`

There is no `requirements.txt` in the repo, so Streamlit has to be installed directly. The Makefile and CI workflow both check for a `requirements.txt` and skip the install step when it is missing.

No API keys and no environment variables are used anywhere in the code.

## Installation

```bash
git clone https://github.com/espin086/streamlit-botgen.git
cd streamlit-botgen
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit
```

Dev tooling, if you want the lint and format targets:

```bash
make setup
```

That installs `flake8`, `pytest`, `pylint`, `black`, and `isort`.

## Usage

Run the app from the repo root, since the JSON path is relative:

```bash
streamlit run botgen.py
```

Streamlit opens the app at http://localhost:8501. The page has four expanders:

- **Train Your Bot** — type a new prompt and response, click Create, and the pair is appended to `data/prompts.json`
- **Your Questions and Answers** — dumps the current file contents as JSON
- **Update Your Answers** — pick an index, type the replacement prompt and response, click Update
- **Delete Any Answers** — pick an index, click Delete

Below the expanders, "Train Your Chatbot" runs the fake progress bar described above.

Using the CRUD class on its own:

```python
from logic.jsoncrud import JSONFileCRUD

file = JSONFileCRUD("url.json")
file.create({"test": 3})
file.update(0, {"test": 4})
file.read()
file.delete(0)
```

Note that `JSONFileCRUD.__init__` truncates the target file to an empty list, so constructing it against an existing file wipes that file.

Lint and format:

```bash
make isort
make black-it
make pylint
make pytest
```

There are no test files in the repo, so `make pytest` collects nothing.

## Project structure

```
botgen.py                              Streamlit app: the whole UI and its own read/write JSON helpers
logic/__init__.py                      Empty, makes logic an importable package
logic/jsoncrud.py                      JSONFileCRUD class, create/read/update/delete on a JSON file
data/prompts.json                      The dataset: a list of {"prompt", "response"} objects
Makefile                               setup, isort, black-it, pylint, pytest, and an all target
.github/workflows/python_application.yml  CI: installs tooling, runs black, pylint, pytest, isort
LICENSE                                MIT
```

## How it works

`botgen.py` is a single top-to-bottom Streamlit script. It defines its own `read_json` and `write_json` functions and rewrites the entire `data/prompts.json` file on every create, update, or delete. It does not import `logic.jsoncrud`, so the class in that module is currently unused by the app and duplicates the same logic.

Records are identified by their position in the list. Update and delete both take a numeric index bounded by `len(data) - 1`, which means an empty dataset gives the number inputs a negative maximum and the app errors out. There is also no confirmation step on delete.

The CI workflow triggers on pushes and pull requests to `master`, but the default branch is `main`, so it does not currently run.

## License

MIT. See [LICENSE](LICENSE).
