import couchdb
couch = couchdb.Server('http://localhost:5984/')
couch.resource.credentials = ('whisk_admin','some_passw0rd')
couchdb = 'whisk_local_activations'
db = couch[couchdb]
for id in db:
	doc = {}
	if "_design" not in id:
		#print(db[id].rev)
		just_id = id.split('/')
		doc['_id'] = just_id[1]
		if db[id].rev is list:
			doc['_rev'] = db[id].rev
		else:
			doc['_rev'] = db[id].rev
		print(doc)
		db.delete(db[id])
		#print(id)
		db.purge([doc])
db.compact()
