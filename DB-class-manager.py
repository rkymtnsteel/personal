import ravendb

import ravendb

class DatabaseManager:
    def __init__(self, server_url="http://192.168.1.131:8080", database_name="familybook"):
        """Initialize RavenDB connection"""
        self.store = ravendb.DocumentStore(urls=[server_url], database=database_name)
        self.store.initialize()

        # Define multiple templates
        self.templates = {
            "headOfHousehold": {
                "@metadata": {"@collection": "Templates"},
                "id": "hoh",
                "type": "headOfHousehold",
                "fName": "",
                "mName": "",
                "lName": "",
                "generation": "",
                "DOB": "",
                "occupation": "",
                "spouse": None,
                "children": []
            },
            "spouse": {
                "@metadata": {"@collection": "Templates"},
                "id": "spouse",
                "type": "spouse",
                "fName": "",
                "mName": "",
                "lName": "",
                "DOB": "",
                "occupation": "",
                "children": []
            },
            "child": {
                "@metadata": {"@collection": "Templates"},
                "id": "child",
                "type": "child",
                "fName": "",
                "mName": "",
                "lName": "",
                "DOB": "",
                "gender": ""
            }
        }

    def store_templates(self):
        """Store multiple templates in RavenDB"""
        with self.store.open_session() as session:
            for template_name, template_data in self.templates.items():
                session.store(template_data, template_data["id"])
                metadata = session.advanced.get_metadata_for(template_data)
                metadata["@collection"] = "Templates"  # Explicitly set collection
            session.save_changes()
        return "Templates stored successfully in RavenDB."

    def fetch_document(self, document_id):
        """Fetch any document by ID from RavenDB"""
        with self.store.open_session() as session:
            return session.load(document_id)

    def fetch_template(self, template_name):
        """Fetch a template from RavenDB; if missing, use default template"""
        template_id = f"template/{template_name}"
        template = self.fetch_document(template_id)
        return template if template else self.templates.get(template_name)

    def create_from_template(self, template_name, data):
        """Create a new document based on a stored template"""
        template = self.fetch_template(template_name)
        if template:
            new_doc = template.copy()
            new_doc.update(data)
            new_doc["id"] = self.generate_id(data.get("fName", ""), data.get("mName", ""), data.get("lName", ""), data.get("generation", ""))
            return new_doc
        return None

    def store_document(self, document):
        """Store a document in RavenDB"""
        with self.store.open_session() as session:
            session.store(document, document["id"])
            session.save_changes()
        return document["id"]

    def generate_id(self, first_name, middle_name, last_name, generation):
        """Generate a unique ID based on name and generation"""
        first_initial = first_name[0].upper() if first_name else ""
        middle_initial = middle_name[0].upper() if middle_name else "X"
        last_part = last_name[:3].upper() if last_name else "XXX"
        return f"{first_initial}{middle_initial}{last_part}_{generation}"

db_manager = DatabaseManager()
print(db_manager.store_templates())  # Stores all templates in RavenDB
