import PySimpleGUI as sg
import ravendb

# Initialize the RavenDB session
server_url = ["http://192.168.1.131:8080"]
database_name = "familybook"
store = ravendb.DocumentStore(urls=server_url, database=database_name)
store.initialize()

def generate_id(first_name, middle_name, last_name, generation):
    first_initial = first_name[0].upper() if first_name else ""
    middle_initial = middle_name[0].upper() if middle_name else "X"
    last_part = last_name[:3].upper() if last_name else "XXX"
    return f"{first_initial}{middle_initial}{last_part}_{generation}"

def create_head_of_household(first_name, middle_name, last_name, generation, dob, occupation):
    hoh_id = generate_id(first_name, middle_name, last_name, generation)
    return {
        "@metadata": {"@collection": "HeadsOfHousehold"},
        "@type": "headOfHousehold",
        "id": hoh_id,
        "fName": first_name,
        "mName": middle_name,
        "lName": last_name,
        "generation": generation,
        "DOB": dob,
        "occupation": occupation,
        "spouse": None,
        "children": []
    }

def create_spouse(hoh_id, first_name, middle_name, last_name, generation, dob, occupation, children):
    spouse_id = f"{hoh_id}_spouse"
    return {
        "@metadata": {"@collection": "family"},
        "@type": "spouse",
        "id": spouse_id,
        "fName": first_name,
        "mName": middle_name,
        "lName": last_name,
        "generation": generation,
        "DOB": dob,
        "occupation": occupation,
        "children": children
    }

def create_child(first_name, middle_name, last_name, generation, dob, gender):
    child_id = generate_id(first_name, middle_name, last_name, generation)
    return {
        "@metadata": {"@collection": "Children"},
        "@type": "child",
        "id": child_id,
        "fName": first_name,
        "mName": middle_name,
        "lName": last_name,
        "generation": generation,
        "DOB": dob,
        "gender": gender
    }

# Initial layout
layout = [
    [sg.Text('Select Entry Type'), sg.Combo(['Head of Household', 'Spouse', 'Child'], key='entry_type', readonly=True)],
    [sg.Text('', size=(2, 1))],
    [sg.Text('First Name'), sg.InputText(key='first_name')],
    [sg.Text('Middle Name'), sg.InputText(key='middle_name')],
    [sg.Text('Last Name'), sg.InputText(key='last_name')],
    [sg.Text('Generation'), sg.InputText(key='generation')],
    [sg.Text('Date of Birth (YYYY-MM-DD)'), sg.InputText(key='dob')],
    [sg.Text('Occupation'), sg.InputText(key='occupation')],
    [sg.Text('Gender (M/F)'), sg.InputText(key='gender')],
    [sg.Text('Head of Household ID (for Spouse/Child)'), sg.InputText(key='hoh_id')],
    [sg.Text('Children')],
    [sg.Column([[]], key='children_column')],
    [sg.Button('Add Child'), sg.Button('Submit'), sg.Button('Cancel')]
]

window = sg.Window('Family Entry Form', layout)

child_count = 0

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Cancel'):
        break
    if event == 'Add Child':
        child_count += 1
        child_layout = [
            [sg.Text(f'Child {child_count} First Name'), sg.InputText(key=f'child_{child_count}_first_name')],
            [sg.Text(f'Child {child_count} Middle Name'), sg.InputText(key=f'child_{child_count}_middle_name')],
            [sg.Text(f'Child {child_count} Last Name'), sg.InputText(key=f'child_{child_count}_last_name')],
            [sg.Text(f'Child {child_count} Generation'), sg.InputText(key=f'child_{child_count}_generation')],
            [sg.Text(f'Child {child_count} Date of Birth (YYYY-MM-DD)'), sg.InputText(key=f'child_{child_count}_dob')],
            [sg.Text(f'Child {child_count} Gender (M/F)'), sg.InputText(key=f'child_{child_count}_gender')],
            [sg.HorizontalSeparator()]
        ]
        window.extend_layout(window['children_column'], child_layout)
    if event == 'Submit':
        entry_type = values['entry_type']
        first_name = values['first_name']
        middle_name = values['middle_name']
        last_name = values['last_name']
        generation = values['generation']
        dob = values['dob']
        occupation = values['occupation']
        gender = values['gender']
        hoh_id = values['hoh_id']

        if entry_type == 'Head of Household':
            new_entry = create_head_of_household(first_name, middle_name, last_name, generation, dob, occupation)
        elif entry_type == 'Spouse':
            children = []
            for i in range(1, child_count + 1):
                child = {
                    "fName": values[f'child_{i}_first_name'],
                    "mName": values[f'child_{i}_middle_name'],
                    "lName": values[f'child_{i}_last_name'],
                    "generation": values[f'child_{i}_generation'],
                    "DOB": values[f'child_{i}_dob'],
                    "gender": values[f'child_{i}_gender']
                }
                children.append(child)
            new_entry = create_spouse(hoh_id, first_name, middle_name, last_name, generation, dob, occupation, children)
        elif entry_type == 'Child':
            new_entry = create_child(first_name, middle_name, last_name, generation, dob, gender)
        else:
            sg.popup("Invalid entry type selected.")
            continue

    # Store the new entry in RavenDB
    with store.open_session() as session:
        session.store(new_entry, new_entry['id'])
        session.save_changes()

    sg.popup(f"New {entry_type} document added with ID: {new_entry['id']}")
# ::contentReference[oaicite:0]{index=0}