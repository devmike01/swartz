import PySimpleGUI as sg
from src.model import result_popo as rp
from src.logic import html_generator as hg, ref_downloader as rd
from threading import Thread


class SwartzWindow:

    def __init__(self):
        # Define the window's contents
        progress_value = 50
        layout = [[sg.Text("Copy and past article links. One article url per line.",
                           font="20")],
                  [sg.Multiline(key='-INPUT-', size=(400, 8), font="20")],
                  [sg.ProgressBar(progress_value, orientation='h', size=(100, 2),
                                  border_width=1, key='-PROGRESS_BAR-',
                                  bar_color=("Blue", "Yellow"), )],
                  [sg.Text(size=(40, 1), key='-OUTPUT-', font="20")],
                  [sg.Button('Generate', pad=(10, 10), key='-GENERATE-'), sg.Button('Quit')]]

        # Create the window
        window = sg.Window('Swartz', layout, size=(500, 280), resizable=False)

        bulk_ref = rd.BulkReferencer()

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break

            self.progress(window, 0)

            thread = Thread(target=self.generate, args=[values, bulk_ref, window],
                            daemon=True)
            thread.start()

        # Finish up by removing from the screen
        window.close()

    def progress(self, window, counter):
        if counter > 100:
            window['-PROGRESS_BAR-'].update(100)
            return
        self.progress(window, counter + 1,)
        window['-PROGRESS_BAR-'].update(counter)

    @staticmethod
    def set_text(window, text: str):
        window['-OUTPUT-'].update(text)

    @staticmethod
    def enable_generate_btn(window, enable: bool):
        window['-GENERATE-'].update(disabled=not enable)

    def generate(self, values, bulk_ref, window):
        self.set_text(window, 'Fetching Reference(s)...')
        self.enable_generate_btn(window, False)
        user_inp: str = values['-INPUT-']
        is_multiline = user_inp.__contains__("\n")
        if is_multiline:
            links = user_inp.split("\n")
        else:
            links = [user_inp]
        extracted_data = bulk_ref.extract_data(links)
        results = []

        try:
            for ref_result in extracted_data:
                for result in ref_result['results']:
                    result_popo = rp.Result(result)
                    results.append(result_popo)
            is_done = hg.HtmlGenerator(results)
            if is_done:
                self.set_text(window, 'Reference generated successfully.')
            self.enable_generate_btn(window, True)
        except Exception as e:
            self.enable_generate_btn(window, True)
            self.set_text(window, 'Error' + e.__str__())
