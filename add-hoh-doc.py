import ravendb

server_url = ["http://192.168.1.131:8080"]
database_name = "familybook"

# Initialize the RavenDB session
store = ravendb.DocumentStore(urls=server_url, database=database_name)
store.initialize()

def generate_id(first_name, middle_name, last_name, generation):
    first_initial = first_name[0].upper() if first_name else ""
    middle_initial = middle_name[0].upper() if middle_name else "X"  # Use "X" if no middle name
    last_part = last_name[:3].upper() if last_name else "XXX"  # First 3 letters of last name
    return f"{first_initial}{middle_initial}{last_part}_{generation}"

# Function to create a Head of Household document
def create_head_of_household(first_name, middle_name, last_name, generation, dob, occupation):
    hoh_id = generate_id(first_name, middle_name, last_name, generation)  # Generate custom ID
    spouse_id = hoh_id + "_spouse"  # Spouse ID is HOH ID + "spouse"


    return {
        "@metadata": {"@collection": "hoh"},
        "@type": "headOfHousehold",
        "familyName": last_name,
        "id": hoh_id,
        "fName": first_name,
        "mName": middle_name,
        "lName": last_name,
        "generation": generation,
        "DOB": dob,
        "occupation": occupation,
        "spouse": {"id": spouse_id}
    }

    return hoh_document

# Sample document using the template
new_hoh = create_head_of_household(
    first_name="Dean",
    middle_name="A",
    last_name="Geary",
    generation="Gen1",
    dob="1955-10-31",
    occupation="Software Engineer"
)

# Save document to RavenDB
with store.open_session() as session:
    metadata = session.advanced.get_metadata_for(new_hoh)
    metadata["@collection"] = "hoh"  # Set collection name explicitly
    session.store(new_hoh, f"hoh/{new_hoh['id']}")  # Store under collection "hoh"
    session.save_changes()

print(f"New Head of Household document added with ID: {new_hoh['id']}")
print(f"Spouse ID: {new_hoh['spouse']['id']}")