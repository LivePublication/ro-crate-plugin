"""

The plugin shall parse the metadata of the `ro-crate-metadata.json` file to extract 
information about the RO-Crate instance.

- The plugin shall validate the type of the RO-Crate against a predefined list of
  expected types.
- The plugin shall validate the version of the RO-Crate against a predefiend list of
  expected types.
- The plugin shall notify the user if the RO-Crate type or version is not recognised

note: use the RO-Crate validator (slack)

This file holds the logic for metadata extractiong and validation of the RO-Crate type
and version. It will also notify the user of any discrepancies (e.g., unrecognized type
or invalid version)

"""
