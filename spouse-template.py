import ravendb

server_url = ["http://192.168.1.131:8080"]
database_name = "familybook"

# Initialize the RavenDB session
store = ravendb.DocumentStore(urls=server_url, database=database_name)
store.initialize()

# Define Head of household template
# All ids will take the form: {family name} + generation + "-" seq 
spouse_template = {
    "@type": "spouseTemplate",
    "familyName": "",
    "id": "",
    "fName": "",
    "mName": "",
    "lName": "",
    "maidenName": "",
    "gender": "",
    "DOB": "",
    "occupation": "",
    "children": [ 
        {
            "name": "",
            "gender": "",
            "DOB": "",
            "generation": "",
            "id": ""
        }
    ]
}

with store.open_session() as session:
    session.store(spouse_template, "templates/family")
    session.save_changes()
    
print("Template saved")