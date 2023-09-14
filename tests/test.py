from owlready2 import default_world
import os

dir_path = 'ontologies'
def try_load():
    for file_path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file_path)):
            try:
                default_world.get_ontology(os.path.join(dir_path, file_path)).load()
            except:
                raise ValueError("Unable to load " + os.path.join(dir_path, file_path))

try_load()