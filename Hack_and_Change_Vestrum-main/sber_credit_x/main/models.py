from django.db import models

# Модель клиента
class Client(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    birth_date = models.DateField("Дата рождения")
    passport_data = models.TextField("Паспортные данные")
    registration_address = models.CharField("Адрес регистрации", max_length=255)
    residence_address = models.CharField("Адрес проживания", max_length=255)
    marital_status = models.CharField("Семейное положение", max_length=50)
    children = models.BooleanField("Наличие детей")
    place_of_work = models.CharField("Место работы", max_length=255)
    work_experience = models.CharField("Стаж работы", max_length=50)
    position = models.CharField("Должность", max_length=100)
    confirmed_income = models.DecimalField("Ежемесячный подтвержденный доход", max_digits=10, decimal_places=2)
    savings_in_bank = models.BooleanField("Наличие сбережений на счетах в Банке")

    def __str__(self):
        return self.full_name

# Модель заявки
class Application(models.Model):
    client = models.ForeignKey(Client, related_name='applications', on_delete=models.CASCADE)
    status = models.CharField("Статус заявки", max_length=50, default='new')
    application_date = models.DateTimeField("Дата подачи заявки", auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} - {self.status}"

# Модель шагов проверки заявки
class ApplicationStep(models.Model):
    application = models.ForeignKey(Application, related_name='steps', on_delete=models.CASCADE)
    step_number = models.PositiveSmallIntegerField("Номер шага")
    description = models.TextField("Описание шага")
    is_completed = models.BooleanField("Шаг завершен", default=False)
    date_completed = models.DateTimeField("Дата завершения шага", null=True, blank=True)
    notes = models.TextField("Заметки", blank=True)

    def __str__(self):
        return f"Шаг {self.step_number} для заявки {self.application.id}"
