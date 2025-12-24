# SaleOrderAutomation_Python

Brief documentation for the SaleOrderAutomation_Python workspace.

## Description

This repository contains utilities and scripts to automate sales order processing (data extraction, transformation, upload to Merlin/DMS, and reporting). The code is split between a small demo/dummy area and the main project logic under the `project/` and `scripts/` folders.

## Quick start

1. Install Python (recommended 3.8+).
2. Create and activate a virtual environment:

   - Windows (PowerShell):

     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

   - Windows (cmd):

     ```cmd
     python -m venv .venv
     .\.venv\Scripts\activate.bat
     ```

3. Install dependencies (if a `requirements.txt` is added):

   ```bash
   pip install -r requirements.txt
   ```

4. Run the main entry (project):

   ```bash
   python project/main.py
   ```

## Project layout

- `project/` — core application modules (contains `main.py`, DB readers, config).
- `scripts/` — helper scripts (DB writer, DMS downloader, file handlers, logger, merlin API adapters).
- `dummy_dms/`, `dummy_merlin_portal/` — local dummy services and example pages for testing.
- `input/`, `output/`, `logs/` — runtime data directories.

## Common tasks

- Run unit or integration tests: (add tests and CI as needed).
- Add a `requirements.txt` or `pyproject.toml` to pin dependencies.

## Contributing

Feel free to open issues or submit PRs. Add a short description of changes and relevant reproduction steps.

## Notes

- This README is a minimal starter. Update with specific dependency versions, environment variables, and running instructions as the project evolves.

## License

Specify a license for the project (e.g., MIT) by adding a `LICENSE` file.
