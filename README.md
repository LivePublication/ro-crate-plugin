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
    

## Testing
The following commands explain how to run tests, and how to add them.

## Additional Context
The RO-Crate Plugin utilises a lot of wonderful and helpful OpenSource work, here are some links to their corresponding OpenSource GitHubs (along with why we have decided to use it)

## Notes
# Stencila Plugin
This repository was initially created using the starting point for writing a Stencila plugin in Python. It contains a standard python setup, including:
- [Poetry](https://python-poetry.org) for package management.
- The required dependencies from Stencila ([types](https://pypi.org/project/stencila_types/) and [plugin](https://pypi.org/project/stencila_plugin/))
- Implementation of the Kernel API that simply echoes the input.
- A set of tests that can be run using `pytest`.

If you'd like to work on this repository any future, use this template to continue working on it but ideally fork your own repository and create related branches. Notes:
- `src` includes all informtion relating to the RO-Crate Plugins functionality
- `pyproject.toml` includes the package name, description, and author.
- `tests/conftest.py` includes the location of the plugin script.

## Other Helpful links

1. [https://github.com/crs4/rocrate-validator/]
2. [https://github.com/ResearchObject/ro-crate-py]
