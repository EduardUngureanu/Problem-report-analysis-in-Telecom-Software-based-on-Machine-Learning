import pprint
from pymongo import MongoClient

def grp_in_charge_occurance(client: MongoClient):
    document_count = client['test-database']['test-collection'].count_documents({})
    grp_dict = {}
    grp_list = client['test-database']['test-collection'].distinct('groupInCharge')
    for grp in grp_list:
        grp_dict[grp] = client['test-database']['test-collection'].count_documents({'groupInCharge' : grp}) / document_count * 100
    pprint.pprint(sorted(grp_dict.items(), key=lambda x: x[1]))

def feature_list(client: MongoClient):
    feature_list = client['test-database']['test-collection'].distinct('feature')
    pprint.pprint(feature_list)

def cnn_percent(client: MongoClient):
    val = client['test-database']['test-collection'].count_documents({'state' : 'Correction Not Needed'}) / client['test-database']['test-collection'].count_documents({}) * 100
    print("Percentage of corrections not needed: {:.4f}%".format(val))

def nr_of_atachments(client:MongoClient):
    lista = client['test-database']['test-collection'].find({})
    newlist = sorted(lista, key=lambda d: len(d['attachedPRs']))
    for dict in newlist:
        print("problemReportId:{}, nubmer of attachements {}".format(dict['problemReportId'], len(dict['attachedPRs'])))

client = MongoClient('localhost', 27017)
db = client['test-database']
collection = db['test-collection']

# grp_in_charge_occurance(client)
# feature_list(client)
# cnn_percent(client)
nr_of_atachments(client)

client.close()