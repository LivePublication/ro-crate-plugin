# Welcome to the RO-Crate Plugin!
This README.md will discuss ways to set up the RO-Crate Plugin and also educate you on how to run it with Stencila, with will be a later upcoming feature.


## Getting Started
This explains how to run the RO-Crate Plugin on your local machine (whether you've got a Windows, Linux, or MacOS). Please follow the following steps:

1. Open a terminal
2. Clone the RO-Crate Plugin repository with the following command:
    `git clone <https://github.com/LivePublication/ro-crate-plugin>`
3. Ensure that you are in the correct directory for the ro-crate-plugin with the following command:
    `cd ro-crate-plugin`
4. Please ensure that you currenctly have the most uptodate version of the ro-crate-plugin and it's dependencies through the following command:
    `git pull`
    `git submodule init`
    `git submodule update`
5. Install all other dependencies with the following command:
    `pdm install`
6. Initialise the project using one of the following commands:
    
7. To run the RO-Crate plugin, traverse to the file `rocrate_manager.py` and run the commands in main (this is how it currently works but will eventually be linked up to Stencila's VSCode extension)

## Testing
The following commands explain how to run tests, and how to add them.

Run the following commands in the terminal to run test:
1. `cd tests`
2. `pytest`
A trace should display the results of the test

To add tests traverse yourself to the `/tests` directory and and tests as such. Notes:
- `/tests/crates` includes valid and invalid RO-Crate examples to test against
- `/tests/plugin` includes all tests relating to the component that operates as a Stencila Plugin
- `/tests/unit` includes all unit tests that test the logic of the RO-Crate Plugin 

## Additional Context
The RO-Crate Plugin utilises a lot of wonderful and helpful OpenSource work, here are some links to their corresponding OpenSource GitHubs (along with why we have decided to use it)

## Notes
# This Plugin is a Stencila Plugin, what does that mean?
This repo has been created from Stencila's plugin template given [here](https://github.com/stencila/plugin-python-template). It therefore has the following dependencies:
- [Poetry](https://python-poetry.org) for package management. 
- Stencila dependencies: ([types](https://pypi.org/project/stencila_types/) and [plugin](https://pypi.org/project/stencila_plugin/))
- `pytest`

If you'd like to work on this repository the logic regarding the RO-Crate Plugin exsists within `/src/logic` where the Stencila plugin logic exists under `src/plugin_python_template. Ideally continue working on this using a fork of the repository and created branches as such. Please Note:
- `src` includes all information relating to the RO-Crate Plugin's functionality
- `pyproject.toml` includes the package name, description, and author.
- `tests/conftest.py` includes the location of the plugin script.

# Open Source Libraries
This project has utilised the lovely work of `crs4's` rocrate-validator to validate all of the plugins RO-Crate objects, here is the link to their repository https://github.com/crs4/rocrate-validator/. Please keep in mind that currently we are using a git submodule for the rocrate-validator - this will eventually be changed to use their pip installation. It also utilises the work of ResearchObject to create and consume RO-Crate objects here is the link to their repository: https://github.com/ResearchObject/ro-crate-py.
