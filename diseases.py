import re

import wikipedia
from elasticsearch import Elasticsearch

client = Elasticsearch()  # elasticsearch client used to communicate with the database
indexName = "medical"  # the index name
# client.indices.delete(index=indexName) #delete an index
client.indices.create(index=indexName)  # create an index

diseaseMapping = {
    'properties': {
        'name': {'type': 'string'},
        'title': {'type': 'string'},
        'fulltext': {'type': 'string'}
    }
}
# client.indices.delete_mapping(index=indexName,doc_type='diseases')
client.indices.put_mapping(index=indexName, doc_type='diseases', body=diseaseMapping)

dl = wikipedia.page("Lists_of_diseases")

diseaseListArray = []
check = re.compile("List of diseases*")
for link in dl.links:
    if check.match(link):
        try:
            diseaseListArray.append(wikipedia.page(link))
        except Exception as e:
            print(str(e))

checkList = [["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], ["A"], ["B"], ["C"], ["D"], ["E"], ["F"], ["G"], ["H"],
             ["I"], ["J"], ["K"], ["L"], ["M"], ["N"], ["O"], ["P"], ["Q"], ["R"], ["S"], ["T"], ["U"], ["V"], ["W"],
             ["X"], ["Y"], ["Z"]]
docType = 'diseases'  # document type we will index
for diseaselistNumber, diseaselist in enumerate(diseaseListArray):  # loop through disease lists
    for disease in diseaselist.links:  # loop through lists of links for every disease list
        try:
            if disease[0] in checkList[diseaselistNumber] and disease[0:3] != "List":
                currentPage = wikipedia.page(disease)
                client.index(index=indexName, doc_type=docType, id=disease,
                             body={"name": disease, "title": currentPage.title, "fulltext": currentPage.content})
        except Exception as e:
            pass
