import PySimpleGUI as sg
from database_manager import DatabaseManager

db_manager = DatabaseManager()

layout = [
    [sg.Text('Select Entry Type'), sg.Combo(['headOfHousehold', 'spouse', 'child'], key='entry_type', readonly=True)],
    [sg.Text('First Name'), sg.InputText(key='first_name')],
    [sg.Text('Middle Name'), sg.InputText(key='middle_name')],
    [sg.Text('Last Name'), sg.InputText(key='last_name')],
    [sg.Text('Generation'), sg.InputText(key='generation')],
    [sg.Text('Date of Birth (YYYY-MM-DD)'), sg.InputText(key='dob')],
    [sg.Text('Occupation'), sg.InputText(key='occupation')],
    [sg.Button('Submit'), sg.Button('Cancel')]
]

window = sg.Window('Family Entry Form', layout)

while True:
    event, values = window.read()
    
    if event in (sg.WINDOW_CLOSED, 'Cancel'):
        break

    elif event == 'Submit':
        entry_type = values['entry_type']
        data = {
            "fName": values['first_name'],
            "mName": values['middle_name'],
            "lName": values['last_name'],
            "generation": values['generation'],
            "DOB": values['dob'],
            "occupation": values['occupation'],
        }

        new_entry = db_manager.create_from_template(entry_type, data)
        
        if new_entry:
            stored_id = db_manager.store_document(new_entry)
            sg.popup(f"Document saved with ID: {stored_id}")
        else:
            sg.popup("Error: Template not found!")

window.close()
