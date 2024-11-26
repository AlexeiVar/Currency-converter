from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import API


# Проверка, что нажата цифра при вводе в сумму валюты для переведения
def number_validation(pressed):
    if pressed:
        try:
            int(pressed)
            return True
        except ValueError:
            return False


# Получаю лист всех поддерживаемых кодов
code_list = API.get_codes()
# Проверяю что коды есть, если их нет то показываю пользователю ошибку
if code_list:
    pass
else:
    messagebox.showerror('API error', 'API недоступен по той или иной причине')
# Делаю лист только для кодов валюты
code_values = []
for thing in code_list:
    code_values.append(thing[0])


# Фрейм для "головы", содержит в себе немного текста и основную валюту
class HeadFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Код основной валюты, выбирается из списка поддерживаемой валюты
        self.main_currency = ttk.Combobox(self, state='readonly', width=10, values=code_values)
        self.main_currency.grid(row=0, column=2, sticky='e')
        # Здесь будет храниться имя выбранной основной валюты
        self.main_currency_name = ttk.Entry(self, state='readonly', width=27)
        self.main_currency_name.grid(row=0, column=3, sticky='e')
        # Привязываю код главной валюты к изменению её имени
        self.main_currency.bind('<<ComboboxSelected>>', self.change_name)
        # Надпись для объяснения основной валюты
        self.flavour_text = ttk.Label(self, text='Валюта, в которую переводить')
        self.flavour_text.grid(row=0, column=0, sticky='w')
        # Надпись для объяснения листа переводимой валюты
        self.other_currency_clarification = ttk.Label(self, text='Переводимая валюта')
        self.other_currency_clarification.grid(row=1, column=1, sticky='w')
        # Надпись для объяснения итога перевода валюты
        self.total_clarification = ttk.Label(self, text='Итог перевода', width=17)
        self.total_clarification.grid(row=1, column=3, sticky='e', padx=(0, 0))

    # Для изменения имени валюты, после выбора кода валюты
    def change_name(self, _event):
        self.main_currency_name.configure(state='normal')

        self.main_currency_name.delete(0, tk.END)
        for combo in code_list:
            if combo[0] == self.main_currency.get():
                self.main_currency_name.insert(0, combo[1])
                self.main_currency_name.configure(state='readonly')
                return 1
        self.main_currency_name.insert(0, 'не найдено')

        self.main_currency_name.configure(state='readonly')
        return 0


# Фрейм для "тела", содержит все переводимые валюты и результаты перевода
class BodyFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        # Создаю лист для сохранения созданных полей валют
        self.entry_list = []
        # Кнопки для добавления/удаления валюты
        self.add_button = ttk.Button(self, text='Добавить валюту', command=lambda: self.add())
        self.delete_button = ttk.Button(self, text='Удалить валюту', command=lambda: self.remove())
        # Сразу вызываю создание первой валюты
        self.add()

        self.delete_button.grid(row=5, column=1, sticky='ew')
        self.add_button.grid(row=5, column=0, sticky='ew')

    def add(self):
        number_validate = (self.register(number_validation), '%S')
        # Поле для количества валюты
        numb_entry = ttk.Entry(self, validate="key", validatecommand=number_validate)
        numb_entry.insert(0, '0')
        numb_entry.grid(row=len(self.entry_list), column=0)
        # Поле для кода валюты, является списком со всеми доступными валютами
        code_entry = ttk.Combobox(self, state='readonly', width=10, values=code_values)
        code_entry.grid(row=len(self.entry_list), column=1)
        # Имя валюты
        currency_name = ttk.Entry(self, state='readonly', width=27)
        currency_name.grid(row=len(self.entry_list), column=2)
        # Делаю что при изменении кода валюты будет меняться и имя
        code_entry.bind('<<ComboboxSelected>>', lambda _event: self.change_name(code_entry, currency_name))
        # Просто знак равно для улучшения интерфейса
        flavour_text = ttk.Label(self, text='=')
        flavour_text.grid(row=len(self.entry_list), column=3)
        # Поле для результата перевода
        result = ttk.Entry(self)
        result.insert(0, '0')
        result.configure(state='readonly')
        result.grid(row=len(self.entry_list), column=4)
        # Лист для удаления/изменения всех значений. 0=изначальная валюта 1=код валюты 2=имя валюты 3=равно 4=результат
        self.entry_list.append((numb_entry, code_entry, currency_name, flavour_text, result))
        if len(self.entry_list) == 5:
            self.add_button.grid_forget()

    def remove(self):
        if self.entry_list:
            # Получаю последнею созданную валюту и убираю её из списка
            entry = self.entry_list.pop()
            # Удаляю все поля из нижней валюты
            for thing in entry:
                thing.grid_forget()
            # Если мы удалили до 4 валюты, то добавляю кнопку добавления валюты
            if len(self.entry_list) == 4:
                self.add_button.grid(row=5, column=0)

    # Метод похожий на тот что у головы, но является статиком и принимает два значения:
    # сам combobox и то где хранится имя
    @staticmethod
    def change_name(combobox, name):
        name.configure(state='normal')

        name.delete(0, tk.END)
        for combo in code_list:
            if combo[0] == combobox.get():
                name.insert(0, combo[1])
                name.configure(state='readonly')
                return 1
        name.insert(0, 'не найдено')

        name.configure(state='readonly')
        return 0
