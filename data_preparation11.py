from elasticsearch import Elasticsearch
from py2neo import Graph, Relationship

client = Elasticsearch()
indexName = "gastronomical"
docType = 'recipes'

graph_db = Graph("http://neo4j:neo4ja@localhost:7474/db/data/")

filename = 'C:/Users/Gebruiker/Downloads/ingredients.txt'
ingredients = []
with open(filename) as f:
    for line in f:
        ingredients.append(line.strip())

print(ingredients)

ingredientnumber = 0
grandtotal = 0
for ingredient in ingredients:
    try:
        IngredientNode = graph_db.merge_one("Ingredient", "Name", ingredient)
    except:
        continue

    ingredientnumber += 1
    searchbody = {
        "size": 99999999,
        "query": {
            "match_phrase":
                {
                    "ingredients": {
                        "query": ingredient,
                    }
                }
        }
    }

    result = client.search(index=indexName, doc_type=docType, body=searchbody)

    print(ingredient)
    print(ingredientnumber)
    print("total: " + str(result['hits']['total']))

    grandtotal = grandtotal + result['hits']['total']
    print("grand total: " + str(grandtotal))

    for recipe in result['hits']['hits']:

        try:
            RecipeNode = graph_db.merge_one("Recipe", "Name", recipe['_source']['name'])
            NodesRelationship = Relationship(RecipeNode, "Contains", IngredientNode)
            graph_db.create_unique(NodesRelationship)
            print("added: " + recipe['_source']['name'] + " contains " + ingredient)

        except:
            continue
