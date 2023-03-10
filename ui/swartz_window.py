import PySimpleGUI as sg
from logic import ref_downloader as rd
from model import result_popo as rp
from logic import html_generator as hg


class SwartzWindow:
    def __init__(self):
        # Define the window's contents
        layout = [[sg.Text("Copy and past article links. One article url per line.",
                           font="20")],
                  [sg.Multiline(key='-INPUT-', size=(400, 8), font="20")],
                  [sg.Text(size=(40, 1), key='-OUTPUT-', font="20")],
                  [sg.Button('Generate', pad=(10, 10)), sg.Button('Quit')]]

        # Create the window
        window = sg.Window('Swartz', layout, size=(470, 250), resizable=True)

        bulk_ref = rd.BulkReferencer()

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break
            # bulk_ref.extract_data()
            user_inp: str = values['-INPUT-']
            is_multiline = user_inp.__contains__("\n")
            if is_multiline:
                links = user_inp.split("\n")
            else:
                links = [user_inp]
            try:
                extracted_data = bulk_ref.extract_data(links)
                results = []
                for ref_result in extracted_data:
                    for result in ref_result['results']:
                        result_popo = rp.Result(result)
                        results.append(result_popo)
                hg.HtmlGenerator(results)
                if len(extracted_data) == len(links):
                    window['-OUTPUT-'].update('Reference generated successfully. Click here')
            except Exception as e:
                print(e)
                window['-OUTPUT-'].update('Error {}'.format(e.__str__()))

        # Finish up by removing from the screen
        window.close()
