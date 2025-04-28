# Rules for This Project

## Python Environment

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

## Design Policy

This project aims to be a single-purpose tool.
First, create it simply, and only consider extending it if expansion becomes absolutely necessary.

## Purpose of This Project

Read Japanese text from PNG screenshots saved under the img/ directory and output it in text format.
