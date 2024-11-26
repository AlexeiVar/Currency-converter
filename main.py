import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from frames import BodyFrame, HeadFrame
import API


def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Currency converter')
        self.geometry('550x225')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.head = HeadFrame(self)
        self.head.grid(row=0, column=0, sticky='ew', rowspan=2)

        self.body = BodyFrame(self)
        self.body.grid(row=2, column=0)
        # Кнопка для конвертации валюты
        button = ttk.Button(self, text='Конвертировать', command=lambda: self.convert())
        button.grid(row=3, column=0, sticky='E')

    def convert(self):
        # Получаю главную валюту
        main_currency = self.head.main_currency.get()
        # Если главной валюты нет, ничего не делаю
        if not main_currency:
            return 0
        # Получаю курсы для валют
        convert_rates = API.get_rates(main_currency)
        # Если курсы есть, то получаю результаты
        if convert_rates:
            for entry in self.body.entry_list:
                entry[4].configure(state='normal')

                entry[4].delete(0, tk.END)
                entry[4].insert(0, (round(float(entry[0].get())/convert_rates[entry[1].get()], 3)))

                entry[4].configure(state='readonly')
        # Если курсов нет, то показываю пользователю ошибку
        else:
            messagebox.showerror('API error', 'API недоступен по той или иной причине')


if __name__ == "__main__":
    main()
