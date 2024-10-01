"""
AC5: The plugin shall maintain a record of artifacts across iterations of RO-Crates, using unique identifiers
to track artifacts regardless of name changes. 

- The plugin shall create symbolic links for artifacts in new RO-Crate iterations, pointing to their corresponding artifacts in previous iterations.
- The plugin shall update the symbolic links whenever a new RO-Crate iteration is introduced, ensuring links point to the latest artifacts
- The plugin shall employ a matching algorithm to identify and link artifacts between iterations, even if their names have changed.
- The plugin shall provide a mechanism to handle conflicts when multiple artifacts could potentially match between iterations, allowing user intervention if necessary
- The plugin shall provided detailed error messages if the symbolic link creation or updating process fails

This module manages the links across iterations of the RO-Crate generation process. It manages artifact
tracking across iterations, creates symbolic links, and resolves any conflicts found between similar
artifacts.
"""
# TODO : Implement the linking module

