"""
Pseudonym Manager Module
========================

pseudodnym : a dictitious name;
pseudonym : a unique identifier for an artifact that is generated automatically by the plugin.


- The plugin shall automatically generate short, unique pseudonyms for each artifact upon detection.
- The plugin shall ensure that each pseudonym is unique within the context of the current RO-Crate.
- The plugin shall maintain a mapping between artifacts original names and their pseudonyms.
- The plugin shall provide a user-friendly interface for users to view and search for artifacts using pseudonyms.

This module manages pseudonym generation and mapping, ensuring uniqueness and providing user-friendly interfaces for viewing and searching artifacts using pseudonyms.
interfaces for viewing and searching artifacts by pseduonym.

CHECK

========================
"""
# TODO : Implement the pseudonym manager module
from artifact import ROCrate


def generate_pseudonym(artifact):
    '''Generates a pseudonym for the given artifact.'''
    
    pass

def get_pseudonym(artifact):
    '''Returns the pseudonym for the given artifact.'''
    pass

def get_artifact(pseudonym):
    '''Returns the artifact for the given pseudonym.'''
    pass

def get_all_pseudonyms():
    '''Returns all pseudonyms and their corresponding artifacts.'''
    pass

def search_pseudonyms(query):
    '''Searches for pseudonyms that match the given query.'''
    pass