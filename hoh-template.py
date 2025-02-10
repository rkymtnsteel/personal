import ravendb

server_url = ["http://192.168.1.131:8080"]
database_name = "familybook"

# Initialize the RavenDB session
store = ravendb.DocumentStore(urls=server_url, database=database_name)
store.initialize()

# Define Head of household template
# All ids will take the form: {family name} + generation + "-" seq 
hoh_template = {
    "@type": "headOfHouseholdTemplate",
    "familyName": "",
    "id": "",
    "fName": "",
    "mName": "",
    "lName": "",
    "generation": "",
    "DOB": "",
    "occupation": "",
    "spouse": 
        {
            "id": "",
        }
}

with store.open_session() as session:
    session.store(hoh_template, "templates/hoh")
    session.save_changes()
    
print("Template saved")