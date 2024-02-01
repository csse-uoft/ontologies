## IANA Media Types
IANA Media Types in `dct:MediaType` 

Source: https://www.iana.org/assignments/media-types/media-types.xhtml

### Properties:
Column `Name` -> `dct:title`<br>
Column `Template` -> URI, if the template is empty, generate the URI from the registry name and the media type `Name`

### [Download](https://csse-uoft.github.io/ontologies/iana-media-types.owl)

### Example

```xml
<?xml version="1.0"?>
<rdf:RDF xml:base="https://www.iana.org/assignments/media-types/"
         xmlns:term="http://purl.org/dc/terms/"
         xmlns="https://www.iana.org/assignments/media-types/">
         
<term:MediaType rdf:about="application/json">
  <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#NamedIndividual"/>
  <term:title rdf:datatype="http://www.w3.org/2001/XMLSchema#string">json</term:title>
</term:MediaType>
```
