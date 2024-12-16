import pymongo

from pymongo import MongoClient

from bson.objectid import ObjectId

client=MongoClient("mongodb+srv://Don:Don_password@doncluster.lxtai.mongodb.net/")
db=client.Pymongo

usersCollection=db.users
users={"nome":"Marco","cognome":"Verdi"}
result=usersCollection.insert_one(users)
print(result.inserted_id)
users2={"nome":"Marco","cognome":"Verdi"}
usersCollection.insert_one(users2)

users=[{"id":1,"first_name":"Dorree","last_name":"Jaynes","email":"djaynes0@unc.edu","gender":"Female","ip_address":"7.192.224.101"},
{"id":2,"first_name":"Dannie","last_name":"Iozefovich","email":"diozefovich1@privacy.gov.au","gender":"Male","ip_address":"235.12.110.174"},
{"id":3,"first_name":"Gusti","last_name":"Drakes","email":"gdrakes2@jalbum.net","gender":"Genderfluid","ip_address":"230.41.249.98"},
{"id":4,"first_name":"Ade","last_name":"Brockington","email":"abrockington3@tumblr.com","gender":"Male","ip_address":"127.110.110.186"},
{"id":5,"first_name":"Ernst","last_name":"Sheeres","email":"esheeres4@surveymonkey.com","gender":"Male","ip_address":"235.114.186.190"},
{"id":6,"first_name":"Bianka","last_name":"Wilbore","email":"bwilbore5@themeforest.net","gender":"Female","ip_address":"161.38.210.61"},
{"id":7,"first_name":"Hynda","last_name":"Gravy","email":"hgravy6@wikimedia.org","gender":"Female","ip_address":"234.89.61.37"},
{"id":8,"first_name":"Serge","last_name":"Janecki","email":"sjanecki7@hexun.com","gender":"Male","ip_address":"77.100.177.182"},
{"id":9,"first_name":"Byrle","last_name":"Duncan","email":"bduncan8@edublogs.org","gender":"Male","ip_address":"237.0.97.81"},
{"id":10,"first_name":"Nikolas","last_name":"Luck","email":"nluck9@ftc.gov","gender":"Male","ip_address":"227.92.65.178"}]

usersCollection.insert_many(users)

usersage=[{"first_name":"Joyan","last_name":"Hellen","email":"jhellen0@dropbox.com","gender":"Female","age":46},
{"first_name":"Jillayne","last_name":"Doogue","email":"jdoogue1@meetup.com","gender":"Female","age":4},
{"first_name":"Kati","last_name":"Athridge","email":"kathridge2@parallels.com","gender":"Female","age":35},
{"first_name":"Errol","last_name":"Deerness","email":"edeerness3@globo.com","gender":"Non-binary","age":12},
{"first_name":"Elke","last_name":"Readings","email":"ereadings4@1und1.de","gender":"Female","age":94},
{"first_name":"Issie","last_name":"Longea","email":"ilongea5@seattletimes.com","gender":"Female","age":41},
{"first_name":"Karlene","last_name":"Quarton","email":"kquarton6@dedecms.com","gender":"Female","age":65},
{"first_name":"Herb","last_name":"McCalum","email":"hmccalum7@pcworld.com","gender":"Male","age":34},
{"first_name":"Jasper","last_name":"Siemons","email":"jsiemons8@tinyurl.com","gender":"Male","age":1},
{"first_name":"Esme","last_name":"Gantz","email":"egantz9@networkadvertising.org","gender":"Non-binary","age":16}]

#usersCollection.insert_many(usersage)

query={'age':35}

query2={"age":{"$gt":25}}           #gte greater or equal then  lt, lte, eq->equal, ne->not equal, $in per gli array, $regex per le regex

#sintassi per le regex: {campo:{$regex:"pattern",$options: "i"}}  al posto di "i" ci puoi mettere anche "x" ,"i" significa che ignori la capitalizzazione, "x" che ignori li spazi

#pattern: inizia con la lettera g -> {"nome":{"$regex":"^G"}}       ^ significa inizia con

#finisce con "ino" -> {"nome":{"$regex":"ino$"}}        $ finisce con

#che all'interno ci sia LL -> {"nome":{"$regex":"ll"}}

#L qualsiasi lettera e poi O -> {"nome":{"$regex":"L.O"}}

#che contenga uno di questi caratteri (ABC) -> {"nome":{"$regex":"[ABC]"}}

 #qualsiasi lettera compresa tra A e F -> {"nome":{"$regex":"[A-F]"}}

 #printa se trovi almeno un carattere al di fuori di ABC -> {"nome":{"$regex":"[^ABC]"}}

 #printa se trovi una A e un numero indistinto di B(anche 0) {"nome":{"$regex":"AB*"}}

#printa se trovi una A e almeno una B {"nome":{"$regex":"AB+"}}

#printa se trovi esattamente 3 A consecutive {"nome":{"$regex":"A{3}"}}

#printa se trovi esattamente un numero consecutivo di A tra 2 e 4 {"nome":{"$regex":"A{2-4}"}}

#printa se trovi la stringa ABC e prima e dopo un numero indistinto di caratteri prima e dopo {"nome":{"$regex":".*ABC.*"}}

result=usersCollection.find(query2).sort("age",1).skip(1).limit(3)
for user in result:    
    print(user)

#result=usersCollection.find(query2).sort("age",-1)  ordine decrescente, ordine crescente : 1

#result=usersCollection.find(query2).sort("age",1).skip(1).limit(3) printa la 2 3 e 4 linea

query={"first_name":"Herb"}
value={"$set":{"first_name":"Ferb"}}        #cambiamo il nome di Herb in Ferb

usersCollection.update_many(query,value)

result=usersCollection.find({'first_name':"Ferb"})
for user in result:    
    print(user)

#query={"first_name":"Herb"}
#value={"$set":{"first_name":"Ferb","age":55}}      cambi nome ed età

#{} query vuota = tutti i documenti

result=usersCollection.find({})
for user in result:                 #mostra tutti gli argomenti
    print(user)

usersCollection=db.users_test

users_test1=[{"nome":"Lino","cognome":"Billo","eta":23},
{"nome":"Pino","cognome":"Ballo","eta":18},
{"nome":"Gino","cognome":"Bello","eta":21},
{"nome":"Dino","cognome":"Bollo","eta":35},
{"nome":"Addolorato","cognome":"Bullo","eta":27}]

#usersCollection.insert_many(users_test1)

#trovare tutte le persone il cui cognome contenga la stringa llo

print("NEW DATAFRAME")

print("#trovare tutte le persone il cui cognome contenga la stringa llo")
result=usersCollection.find({"cognome":{"$regex":"llo"}})
for user in result:
    print(user)

#età compresa tra 20 e 30

print("trovare tutte le persone il cui cognome contenga la stringa llo")
result=usersCollection.find({"eta": {"$gte":20,"$lte":30}})
for user in result:
    print(user)

print("trovare tutte le persone il cui cognome inizi per B")
result=usersCollection.find({"cognome":{"$regex":"^B"}})
for user in result:
    print(user)

print("trovare la persona più giovane")
result=usersCollection.find().sort("eta",1).limit(1)
for user in result:
    print(user)

print("aggiungere una nuova persona nino ballo di 29 anni")
#usersCollection.insert_one({"name":"Nino","cognome":"Ballo","eta":29})
result=usersCollection.find({})
for user in result:
    print(user)

query={"first_name":"Herb"}
value={"$set":{"first_name":"Ferb"}}

print("addolorato aggiornato a 30 anni")
usersCollection.update_one({"nome":"Addolorato"},{"$set":{"eta":30}})
result=usersCollection.find({})
for user in result:
    print(user)

#operatore and:
query={"$and":[
    {"cognome":{"$regex":"ll"}},
    {"nome":{"$in":["Pino","Addolorato"]}},
    {"eta":{"$ne":27}}
]}

print("tutte le persone contenenti 2l consecutive il cui nome è o pino o addolorato che non hanno 27 anni")
result=usersCollection.find(query)
for user in result:
    print(user)

#operatore and: (puoi anche non metterlo)

print("tutte le persone che non hanno un eta maggiore di 30 anni e il nome non inizi per G")
query={"eta":{"$not":{"$gt":30}},
       "nome":{"$not":{"$regex":"^G"}}}
result=usersCollection.find(query)
for user in result:
    print(user)


