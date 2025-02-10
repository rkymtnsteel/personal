import ravendb

server_url = ["http://192.168.1.131:8080"]
database_name = "familybook"

# Initialize the RavenDB session
store = ravendb.DocumentStore(urls=server_url, database=database_name)
store.initialize()

def create_head_of_household(family_name, first_name, last_name, generation, dob, occupation, spouse_id):
    hoh_document = {
        "@type": "headOfHousehold",
        "familyName": family_name,
        "id": f"{family_name.lower()}_{generation}",       # Unique ID based on family name & generation
        "fName": first_name,
        "lName": last_name,
        "generation": generation,
        "DOB": dob,
        "occupation": occupation,
        "spouse": {"id": spouse_id}
    }

    return hoh_document

# Sample document using the template
new_hoh = create_head_of_household(
    family_name="Geary",
    first_name="Dean",
    last_name="Geary",
    generation="Gen1",
    dob="1955-10-31",
    occupation="Software Engineer",
    spouse_id="spouse_001"
)

# Save document to RavenDB
with store.open_session() as session:
    session.store(new_hoh, f"hoh/{new_hoh['id']}")  # Store under collection "hoh"
    session.save_changes()

print("New Head of Household document added successfully!")
