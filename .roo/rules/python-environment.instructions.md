# Python Environment rules

Use uv.

- Create a new project: `uv init --app`
- Activate the environment: `. .venv/bin/activate`
- Deactivate the environment: `deactivate`
- Check installed packages: `uv pip list`
- Add a dependency: `uv add <package_name>`
- Add a development dependency: `uv add --dev <package_name>`
- Add an optional dependency: `uv add --optional <package_name>`
- Remove a dependency: `uv remove <package_name>`
- Synchronize the virtual environment to the latest state (install packages based on pyproject.toml): `uv sync`
- Explicitly update the lock file: `uv lock`
- Upgrade all packages to the latest version: `uv lock --upgrade`
- Run a script: `uv run <script_name>`

In this workspace, the Python environment uses `uv`.
Follow the Python project structure generated by `uv init`.

Refer to the following Do's and Don'ts:
## Do
`uv add fuzzywuzzy python-Levenshtein`
## Don't
`pip install fuzzywuzzy python-Levenshtein`
