import PySimpleGUI as sg
import ravendb

# Initialize RavenDB connection
server_url = ["http://192.168.1.131:8080"]
database_name = "familybook"
store = ravendb.DocumentStore(urls=server_url, database=database_name)
store.initialize()

sg.theme("LightBlue5")

layout = [
    [sg.Text('Enter Name:', text_color="black")],  # Change text color
    [sg.InputText(key="name", background_color="white", text_color="black")],  # Change input field color
    [sg.Button("Submit", button_color=("white", "green"))],  # Change button color
]

window = sg.Window("Custom Form Colors", layout)


# Function to fetch spouse data from RavenDB
def fetch_spouse(spouse_id):
    with store.open_session() as session:
        spouse = session.load(spouse_id)
        return spouse if spouse else None

# Function to update spouse data in RavenDB
def update_spouse(spouse_id, first_name, middle_name, last_name, dob, occupation, children):
    with store.open_session() as session:
        spouse = session.load(spouse_id)
        if spouse:
            spouse["fName"] = first_name
            spouse["mName"] = middle_name
            spouse["lName"] = last_name
            spouse["DOB"] = dob
            spouse["occupation"] = occupation
            spouse["children"] = children  # Updating children list
            session.save_changes()
            return True
    return False

# Function to create/update children dynamically
def add_child_form(child_num):
    return [
        [sg.Text(f'Child {child_num} First Name'), sg.InputText(key=f'child_{child_num}_first_name')],
        [sg.Text(f'Child {child_num} Middle Name'), sg.InputText(key=f'child_{child_num}_middle_name')],
        [sg.Text(f'Child {child_num} Last Name'), sg.InputText(key=f'child_{child_num}_last_name')],
        [sg.Text(f'Child {child_num} DOB (YYYY-MM-DD)'), sg.InputText(key=f'child_{child_num}_dob')],
        [sg.Text(f'Child {child_num} Gender (M/F)'), sg.InputText(key=f'child_{child_num}_gender')],
        [sg.HorizontalSeparator()]
    ]

# Define the update form layout
layout = [
    [sg.Text('Enter ID'), sg.InputText(key='spouse_id'), sg.Button('Load')],
    [sg.Text('First Name'), sg.InputText(key='spouse_first_name')],
    [sg.Text('Middle Name'), sg.InputText(key='spouse_middle_name')],
    [sg.Text('Last Name'), sg.InputText(key='spouse_last_name')],
    [sg.Text('DOB (YYYY-MM-DD)'), sg.InputText(key='spouse_dob')],
    [sg.Text('Occupation'), sg.InputText(key='spouse_occupation')],
    [sg.Text('Children')],
    [sg.Column([[]], key='children_column')],
    [sg.Button('Add Child'), sg.Button('Submit'), sg.Button('Cancel')]
]

window = sg.Window('Update Family Form', layout)

child_count = 0
loaded_spouse = None

while True:
    event, values = window.read()
    
    if event in (sg.WINDOW_CLOSED, 'Cancel'):
        break

    # Load Spouse Data
    elif event == 'Load':
        spouse_id = values['spouse_id']
        loaded_spouse = fetch_spouse(spouse_id)

        if loaded_spouse:
            window['spouse_first_name'].update(loaded_spouse.get("fName", ""))
            window['spouse_middle_name'].update(loaded_spouse.get("mName", ""))
            window['spouse_last_name'].update(loaded_spouse.get("lName", ""))
            window['spouse_dob'].update(loaded_spouse.get("DOB", ""))
            window['spouse_occupation'].update(loaded_spouse.get("occupation", ""))

            # Clear and reload children
            window['children_column'].update([[]])
            child_count = 0
            if "children" in loaded_spouse:
                for child in loaded_spouse["children"]:
                    child_count += 1
                    child_layout = add_child_form(child_count)
                    window.extend_layout(window['children_column'], child_layout)
                    
                    window[f'child_{child_count}_first_name'].update(child.get("fName", ""))
                    window[f'child_{child_count}_middle_name'].update(child.get("mName", ""))
                    window[f'child_{child_count}_last_name'].update(child.get("lName", ""))
                    window[f'child_{child_count}_dob'].update(child.get("DOB", ""))
                    window[f'child_{child_count}_gender'].update(child.get("gender", ""))

        else:
            sg.popup("Spouse not found!")

    # Add a New Child Dynamically
    elif event == 'Add Child':
        child_count += 1
        child_layout = add_child_form(child_count)
        window.extend_layout(window['children_column'], child_layout)

    # Submit the Updated Data
    elif event == 'Submit' and loaded_spouse:
        spouse_id = values['spouse_id']
        first_name = values['spouse_first_name']
        middle_name = values['spouse_middle_name']
        last_name = values['spouse_last_name']
        dob = values['spouse_dob']
        occupation = values['spouse_occupation']

        children = []
        for i in range(1, child_count + 1):
            child = {
                "fName": values.get(f'child_{i}_first_name', ''),
                "mName": values.get(f'child_{i}_middle_name', ''),
                "lName": values.get(f'child_{i}_last_name', ''),
                "DOB": values.get(f'child_{i}_dob', ''),
                "gender": values.get(f'child_{i}_gender', '')
            }
            children.append(child)

        updated = update_spouse(spouse_id, first_name, middle_name, last_name, dob, occupation, children)
        if updated:
            sg.popup("Spouse details updated successfully!")
        else:
            sg.popup("Failed to update spouse!")

window.close()
