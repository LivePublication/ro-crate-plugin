# Welcome to the RO-Crate Plugin!
Welcome to the **RO-Crate Plugin**! This repository contains tools to help you manage RO-Crates efficiently. It’s designed to be extensible and will integrate with **Stencila** in a future release.

---

## Getting Started
Follow these steps to set up the RO-Crate Plugin on your local machine, whether you're using Windows, Linux, or macOS.

### Dependencies
Before starting, ensure you have the following installed:
- [Git](https://git-scm.com)
- [PDM](https://pdm-project.org/en/latest/) for dependency management
- Python (version 3.8 or higher)

### Installation Steps
1. **Clone the repository**
   Open a terminal and run:
   ```bash
   git clone https://github.com/LivePublication/ro-crate-plugin
   ```
2. Navigate to the project directory
   ```bash
   cd ro-crate-plugin
   ```
3. Ensure that the repository is up-to-date including the submodule(s):
   ```bash
   git pull
   git submodule init
   git submodule update
   ```
4. Install dependencies
   ```bash
   pdm install
   ```
5. Activate the virtual environment
   ```bash
   source .venv/bin/activate
   ```
7. Run the RO-Crate Plugin
   For now, run the plugin manually:
   - Navigate to the file `rocrate_manager.py` and run main().
_Note: Integration with the Stencila VS Code extension is under development and will replace step 7._

---

## Testing
We’ve included comprehensive tests to ensure the plugin functions correctly. Here’s how you can run and add tests:

### Running Tests
1. Navigate to the `tests` directory:
   ```bash
   cd tests
   ```
2. Execute the tests using `pytest`:
   ```bash
   pytest 
   ```
   A detailed test trace will display the results.

### Adding Tests
To add new tests, navigate to the /tests directory. You can organize your tests under the following subdirectories:
- `/tests/crates`: Tests for valid and invalid RO-Crate examples.
- `/tests/plugin`: Tests related to the Stencila Plugin component.
- `/tests/unit`: Unit tests for the core logic of the RO-Crate Plugin.

## Additional Information
### What is this Plugin?
This repository is based on the Stencila Plugin Template. Learn more about it [here](https://github.com/stencila/plugin-python-template).

The plugin depends on the following tools and libraries: 
- [Poetry](https://python-poetry.org) for package management. 
- Stencila dependencies: ([types](https://pypi.org/project/stencila_types/) and [plugin](https://pypi.org/project/stencila_plugin/))
- `pytest` for testing.

### Project Structure
- `/src`: contains the core logic for the RO-Crate Plugin.
- `pyproject.toml`: defines the package metadata (e.g., name, description, and author).
- `tests/conftest.py`: specifies the location of the plugin script.

### Open Source Libraries
The RO-Crate Plugin leverages the excellent work of the following open-source projects:
1. [crs4/rocrate-validator](https://github.com/crs4/rocrate-validator/)
   Used to validate all RO-Crate objects in this plugin. (Currently integrated as a Git submodule but will switch to a pip installation in the future.)
2. [ResearchObject/ro-crate-py](https://github.com/ResearchObject/ro-crate-py)
   A library for creating and consuming RO-Crate objects.

## Contributing 
If you’d like to contribute, please:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with detailed descriptions of your changes.

## Future Development
We are actively working on integrating this plugin with Stencila’s VS Code extension. Stay tuned for updates!
