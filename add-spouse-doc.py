import ravendb

server_url = ["http://192.168.1.131:8080"]
database_name = "familybook"

# Initialize the RavenDB session
store = ravendb.DocumentStore(urls=server_url, database=database_name)
store.initialize()

def generate_id(first_name, middle_name, last_name):
    first_initial = first_name[0].upper() if first_name else ""
    middle_initial = middle_name[0].upper() if middle_name else "X"  # Use "X" if no middle name
    last_part = last_name[:3].upper() if last_name else "XXX"  # First 3 letters of last name
    return f"{first_initial}{middle_initial}{last_part}"

# Function to create a Head of Household document
def create_hoh_spouse(hoh_id, first_name, middle_name, last_name, generation, dob, occupation, children):
    children=[{"name": "Child Name", "gender": "M/F", "DOB": "YYYY-MM-DD", "generation": "Gen2"}]
    hoh_id = generate_id("Dean", "A", "Geary") + "_Gen1"
    spouse_id = generate_id(first_name, middle_name, last_name)  # Generate custom ID
    spouse_id = hoh_id + "_" + spouse_id  # Spouse ID is HOH ID + "spouse"


    return {
        "@metadata": {"@collection": "family"},
        "@type": "spouse",
        "familyName": last_name,
        "id": spouse_id,
        "fName": first_name,
        "mName": middle_name,
        "lName": last_name,
        "generation": generation,
        "DOB": dob,
        "occupation": occupation,
        "children": children
    }

# Sample document using the template
new_spouse = create_hoh_spouse(
    first_name="Dean",
    middle_name="A",
    last_name="Geary",
    generation="Gen1",
    dob="1955-10-31",
    occupation="Software Engineer"
)

# Save document to RavenDB
with store.open_session() as session:
    session.store(new_hoh, f"family/{new_hoh['id']}")  # Store under collection "hoh"
    metadata = session.advanced.get_metadata_for(new_hoh)  # Retrieve metadata
    metadata["@collection"] = "hoh"  # Set the collection explicitly
    session.save_changes()

print(f"New Head of Household document added with ID: {new_hoh['id']}")
print(f"Spouse ID: {new_hoh['spouse']['id']}")