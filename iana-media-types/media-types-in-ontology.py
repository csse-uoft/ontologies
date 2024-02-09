from owlready2 import rdfs, default_world
import requests
import csv
import os
import json
from datetime import date

# Load mine-type to file extension mapping
# https://gist.github.com/pedropalhari/ad81feb4d49a3622dfd26e2d4d038140
with open(os.path.join(os.path.dirname(__file__), 'mime-types-to-file-extension.json')) as json_file:
    mine_type2file_exts = json.load(json_file)


# Taken from https://www.iana.org/assignments/media-types/media-types.xhtml
iana_uri_prefix = "https://www.iana.org/assignments/media-types/"
iana_media_type_csvs = {
    "application": "https://www.iana.org/assignments/media-types/application.csv",
    "audio": "https://www.iana.org/assignments/media-types/audio.csv",
    "font": "https://www.iana.org/assignments/media-types/font.csv",
    "image": "https://www.iana.org/assignments/media-types/image.csv",
    "message": "https://www.iana.org/assignments/media-types/message.csv",
    "model": "https://www.iana.org/assignments/media-types/model.csv",
    "multipart": "https://www.iana.org/assignments/media-types/multipart.csv",
    "text": "https://www.iana.org/assignments/media-types/text.csv",
    "video": "https://www.iana.org/assignments/media-types/video.csv",
}


def download_and_load_csv(registry_name: str, url: str): 
    download = requests.get(url)
    decoded_content = download.content.decode('utf-8')
    reader = csv.DictReader(decoded_content.splitlines())
    result = []
    for row in reader:
        # Name, Template, Reference
        # In some cases, the Template is empty, i.e. the uri will be 404, but we still create an uri for it based on the registry and name.
        result.append([row['Name'], iana_uri_prefix + (row['Template'] or f'{registry_name}/{row["Name"]}')])
    return result
        

dct_onto = default_world.get_ontology(location="https://csse-uoft.github.io/ontologies/dct.rdf", base_iri="http://purl.org/dc/terms/").load()
onto = default_world.get_ontology(iana_uri_prefix)
dct_onto.title[onto.metadata] = ['IANA Media Types']
dct_onto.modified[onto.metadata] = [date.today().strftime("%B %d, %Y")]

with onto:
    for registry_name, csv_url in iana_media_type_csvs.items():
        media_types = download_and_load_csv(registry_name, csv_url)
        for [name, uri] in media_types:
            if default_world.get(uri):
                print(f"\nWarning: duplicated {name} : {uri}, Skipped")
            else:
                media_type = dct_onto.MediaType(iri=uri)
                dct_onto.title[media_type] = [name]
                if mine_type2file_exts.get(f'{registry_name}/{name}'):
                    # use ext[1:] to remove the dot
                    file_extensions = [ext[:] for ext in mine_type2file_exts.get(f'{registry_name}/{name}')]
                    rdfs.label[media_type] = [f"{', '.join(file_extensions)} - {registry_name}/{name}"]
                else:
                    rdfs.label[media_type] = [f"{registry_name}/{name}"]
        
    
    # Save to onotolgies/iana-media-types.owl
    onto.save(os.path.join(os.path.dirname(__file__), '..', 'ontologies', 'iana-media-types.owl'))