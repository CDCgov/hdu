CDA2FHIR

Use the API like so.

    curl -X POST -F "cda_file=@good-ccda.xml" http://localhost:8000/cda2fhir/api/    

and a bad example is here:

    curl -X POST -F "cda_file=@bad-ccda.xml" http://localhost:8000/cda2fhir/api/