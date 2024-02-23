import os
import tkinter as tk
from PIL import ImageTk, Image
from full_realization import full_realization, download_data, moex
from time import time
from datetime import datetime, timedelta


class SQGui:

    value = 10000
    num_stocks = 50
    risk = 2

    def __init__(self):

        self.root = tk.Tk()

        self.root.geometry('600x780')
        self.root.title('Suggest Quantum')
        self.root.configure(bg='white')
        self.root.iconbitmap('images/logo_pic.ico')

        # functions

        def set_value(new_value):
            SQGui.value = new_value
            # print(SQGui.value)

        def set_num_stocks(new_num_stocks):
            SQGui.num_stocks = new_num_stocks
            # print(SQGui.num_stocks)
            if new_num_stocks == 50:
                self.label_time.config(text='Ожидаемое время вычисления ≈6 минут')
                self.label_time.update_idletasks()
            elif new_num_stocks == 100:
                self.label_time.config(text='Ожидаемое время вычисления ≈10 минут')
                self.label_time.update_idletasks()
            elif new_num_stocks == 150:
                self.label_time.config(text='Ожидаемое время вычисления ≈17 минут')
                self.label_time.update_idletasks()

        def set_risk(new_risk):
            SQGui.risk = new_risk
            # print(SQGui.risk)

        def photo_button(img_path):
            button_img = Image.open(img_path)
            return ImageTk.PhotoImage(button_img)

        def show_modal_plot(path):

            # print('value:', SQGui.value)
            # print('num_stocks:', SQGui.num_stocks)
            # print('risk:', SQGui.risk)

            global pop_plot
            pop_plot = tk.Toplevel(self.root)
            pop_plot.title('Portfolio value plot')
            pop_plot.geometry('500x375')
            pop_plot.config(bg='white')

            graph = Image.open(path)
            width, height = graph.size
            newsize = (500, int(height/(width/500)))
            graph = graph.resize(newsize)
            test = ImageTk.PhotoImage(graph)
            label = tk.Label(pop_plot, image=test)
            label.image = test
            label.pack()

        def show_modal_txt(path):

            global pop_txt
            pop_txt = tk.Toplevel(self.root)
            pop_txt.title('Portfolio information')
            pop_txt.geometry('300x600')
            pop_txt.config(bg='white')

            with open(path, 'r', encoding="utf-8") as f:
                label = tk.Label(pop_txt, text=f.read(), background='white', justify="left")
                label.pack()

        def compute():

            now = time()

            download_flg = False
            if os.path.exists('MOEX'):
                if os.listdir('MOEX'):
                    datediff = 0
                    for root, i, j in os.walk('MOEX'):
                        times = []
                        for k in j:
                            times.append(os.path.getmtime('MOEX\\' + k))
                        datediff = (datetime.today() - datetime.fromtimestamp(max(times))).days
                    if datediff > 0:
                        self.label.config(text='Загрузка цен акций')
                        self.label.update_idletasks()
                        download_data(moex)
                        download_flg = True
                else:
                    self.label.config(text='Загрузка цен акций')
                    self.label.update_idletasks()
                    download_data(moex)
                    download_flg = True
            else:
                self.label.config(text='Загрузка цен акций')
                self.label.update_idletasks()
                download_data(moex)
                download_flg = True

            if download_flg:
                self.label.config(text='Загрузка цен акций\nВычисление портфеля')
                self.label.update_idletasks()
            else:
                self.label.config(text='Вычисление портфеля')
                self.label.update_idletasks()

            my_portfolio, roi, risker, success_rate, names = full_realization(SQGui.value, SQGui.num_stocks, SQGui.risk)

            print('Суммарное время:', timedelta(seconds=(time() - now)))
            print(f'Исследовано {int(100/success_rate)} портфелей, чтобы найти лучший')
            print('Ожидаемая доходность:', int(roi), '%')
            print('Ожидаемый риск:', int(risker), '%')

            self.label.config(text='Готово!\n' +
                                   'Описание собранного портфеля и график можно найти в папке с приложением:\n' +
                                   f'{names[0]}\n{names[1]}\n\n' +
                                   f'Суммарное время: {str(timedelta(seconds=(time() - now))).split(".")[0]}\n' +
                                   f'Исследовано {int(100/success_rate)} портфелей, чтобы найти лучший\n' +
                                   f'Ожидаемая окупаемость: {int(roi)} %\n' +
                                   f'Ожидаемый риск: {int(risker)} %')

            self.label.update_idletasks()

            show_modal_plot(names[1])
            show_modal_txt(names[0])

        # logo

        self.logo = Image.open('images/Suggest Quantum.png')
        self.test = ImageTk.PhotoImage(self.logo)
        self.label_logo = tk.Label(image=self.test)
        self.label_logo.image = self.test
        self.label_logo.pack(pady=(90, 30))

        # support text

        self.label = tk.Label(self.root, bg='white', text='Набор акций подбирается из состава индекса MOEX', font='Segoe 12')
        self.label.pack(pady=(0, 20))

        # budget

        self.label = tk.Label(self.root, bg='white', text='Введите желаемый бюджет портфеля', font='Segoe 12')
        self.label.pack(pady=(0, 10))

        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0)

        photo_10k = photo_button('images/10k.png')
        photo_50k = photo_button('images/50k.png')
        photo_150k = photo_button('images/150k.png')
        photo_unlim = photo_button('images/unlimited.png')

        self.btn10k = tk.Button(self.buttonframe, command=lambda:set_value(10000), image=photo_10k, borderwidth=0)
        self.btn10k.grid(row=1, column=1)
        self.btn50k = tk.Button(self.buttonframe, command=lambda:set_value(50000), image=photo_50k, borderwidth=0)
        self.btn50k.grid(row=1, column=2)
        self.btn150k = tk.Button(self.buttonframe, command=lambda:set_value(150000), image=photo_150k, borderwidth=0)
        self.btn150k.grid(row=1, column=3)
        self.btn_unlim = tk.Button(self.buttonframe, command=lambda: set_value(10000000), image=photo_unlim, borderwidth=0)
        self.btn_unlim.grid(row=1, column=4)

        self.buttonframe.pack()

        # number of stocks

        self.label = tk.Label(self.root, bg='white', text='Введите желаемое количество акций', font='Segoe 12')
        self.label.pack(pady=(10, 10))

        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0)

        photo_50 = photo_button('images/50.png')
        photo_100 = photo_button('images/100.png')
        photo_150 = photo_button('images/150.png')

        self.btn50 = tk.Button(self.buttonframe, command=lambda: set_num_stocks(50) , image=photo_50, borderwidth=0)
        self.btn50.grid(row=1, column=1)
        self.btn100 = tk.Button(self.buttonframe, command=lambda: set_num_stocks(100), image=photo_100, borderwidth=0)
        self.btn100.grid(row=1, column=2)
        self.btn150 = tk.Button(self.buttonframe, command=lambda: set_num_stocks(150), image=photo_150, borderwidth=0)
        self.btn150.grid(row=1, column=3)
        self.buttonframe.pack()

        # risk level
        self.label = tk.Label(self.root, bg='white', text='Введите желаемый уровень риска', font='Segoe 12')
        self.label.pack(pady=(10, 10))

        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0)

        photo_risk_1 = photo_button('images/risk_1.png')
        photo_risk_2 = photo_button('images/risk_2.png')
        photo_risk_3 = photo_button('images/risk_3.png')

        self.btn_risk_1 = tk.Button(self.buttonframe, command=lambda: set_risk(3), image=photo_risk_1, borderwidth=0)
        self.btn_risk_1.grid(row=1, column=1)
        self.btn_risk_2 = tk.Button(self.buttonframe, command=lambda: set_risk(2), image=photo_risk_2, borderwidth=0)
        self.btn_risk_2.grid(row=1, column=2)
        self.btn_risk_3 = tk.Button(self.buttonframe, command=lambda: set_risk(1), image=photo_risk_3, borderwidth=0)
        self.btn_risk_3.grid(row=1, column=3)

        self.buttonframe.pack()

        # computation

        self.label_time = tk.Label(self.root, bg='white', text='Ожидаемое время вычисления ≈6 минут',
                                   font='Segoe 12')
        self.label_time.pack(pady=(20, 0))

        photo_compute = photo_button('images/compute.png')
        self.btn_compute = tk.Button(command=lambda: compute(), image=photo_compute, borderwidth=0)
        self.btn_compute.pack(pady=(14, 10))

        self.label = tk.Label(self.root, bg='white', text='', font='Segoe 9')
        self.label.pack()

        self.root.mainloop()


if __name__ == '__main__':

    SQGui()
