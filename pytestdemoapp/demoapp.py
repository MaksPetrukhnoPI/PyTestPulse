import csv
import os
import tkinter

import customtkinter as ctk
from CTkTable import *

from pytestpulse import report_format, unit_tests_executor

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PyTestPulseDemoApp")
        self.resizable(False, False)
        self.geometry(f"{700}x{700}")
        self.report_format_frame()
        self.work_dir = os.getcwd()
        self.dir_picker_frame()
        execute_button = ctk.CTkButton(self, text="Execute", command=self.run_pytestpulse)
        execute_button.grid(row=1, column=0, padx=(10, 0), pady=(10, 10), sticky="nsew", columnspan=2)
        self.reports_text_box = ctk.CTkTextbox(self, height=400)
        self.reports_text_box.grid(row=2, column=0, padx=(10, 0), pady=(10, 10), sticky="nsew", columnspan=2)

    def run_pytestpulse(self):
        unit_tests_executor.execute(self.tests_dir_entry.get(), self.__get_report_format(), True)
        reports_file = self.__find_reports_file()
        with open(reports_file, 'r') as f:
            if reports_file.endswith('.csv'):
                self.__display_csv(f)
            else:
                self.__display_text(f)
        os.remove(reports_file)

    def dir_picker_frame(self):
        picker_frame = ctk.CTkFrame(self, border_width=1)
        picker_frame.grid(row=0, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")

        tests_dir_label = ctk.CTkLabel(master=picker_frame, text="Unit tests directory")
        tests_dir_label.grid(row=1, column=1, padx=10, pady=5, sticky='W')
        self.tests_dir_entry = ctk.CTkEntry(master=picker_frame, placeholder_text="Tests directory..",
                                            width=400)
        self.__set_tests_dir_text(os.getcwd().replace('pytestdemoapp', 'unit_tests'))
        self.tests_dir_entry.grid(row=2, column=1, padx=10, pady=(10, 10), sticky="n")

        choose_dir_button = ctk.CTkButton(master=picker_frame, text="Choose dir", width=50,
                                          command=lambda: self.__browse_dir(False))
        choose_dir_button.grid(row=2, column=3, padx=(5, 10), pady=(10, 10), sticky="n")


    def report_format_frame(self):
        radiobutton_frame = ctk.CTkFrame(self, border_width=1)
        radiobutton_frame.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.radio_var = tkinter.IntVar(value=0)
        label_radio_group = ctk.CTkLabel(master=radiobutton_frame, text="Tests Report Format:")
        label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=5, sticky="")

        radio_button_1 = ctk.CTkRadioButton(master=radiobutton_frame, variable=self.radio_var,
                                            value=0, text="Json")
        radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        radio_button_2 = ctk.CTkRadioButton(master=radiobutton_frame, variable=self.radio_var,
                                            value=1, text="Xml")
        radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        radio_button_3 = ctk.CTkRadioButton(master=radiobutton_frame, variable=self.radio_var,
                                            value=2, text="Csv")
        radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        radio_button_4 = ctk.CTkRadioButton(master=radiobutton_frame, variable=self.radio_var,
                                            value=3, text="Text")
        radio_button_4.grid(row=4, column=2, pady=10, padx=20, sticky="n")

    def __display_text(self, f):
        self.table_frame.grid_forget()
        self.reports_text_box.grid(row=2, column=0, padx=(10, 0), pady=(10, 10), sticky="nsew", columnspan=2)
        self.__set_reports_text(f.read())

    def __display_csv(self, f):
        self.reports_text_box.grid_forget()
        self.table_frame = ctk.CTkScrollableFrame(self, height=400, border_width=1)
        self.table_frame.grid(row=2, column=0, padx=(10, 0), pady=(10, 10), sticky="nsew", columnspan=2)
        reader = csv.reader(f, delimiter=';')
        data = list(reader)
        table = CTkTable(master=self.table_frame,
                         values=data,
                         corner_radius=8,
                         header_color=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"]),
                         wraplength=245
                         )
        table.grid(row=0, column=0, padx=0, pady=0, sticky="nsew", columnspan=2)

    def __find_reports_file(self):
        os.chdir(self.work_dir)
        for file in os.listdir():
            if file.startswith('pytestpulse'):
                return file

    def __get_report_format(self):
        match self.radio_var.get():
            case 0:
                return report_format.JsonFormat()
            case 1:
                return report_format.XmlFormat()
            case 2:
                return report_format.CsvFormat()
            case 3:
                return None

    def __browse_dir(self):
        directory = ctk.filedialog.askdirectory()
        self.__set_tests_dir_text(directory)

    def __set_tests_dir_text(self, text):
        self.tests_dir_entry.delete(0, ctk.END)
        self.tests_dir_entry.insert(0, text)

    def __set_reports_text(self, text):
        self.reports_text_box.delete("0.0", "end")
        self.reports_text_box.insert("0.0", text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
