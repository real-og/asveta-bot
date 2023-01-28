import gspread

subjects = ['Русский',
            'Беларуская', 
            'Английский',
            'История',
            'Физика', 
            'Химия', 
            'География',]

classes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

time_periods = ['08:30 - 13:00',
                '13:00 - 18:00',
                '18:00 - 22:00',]

admin_ids = ['277961206',
             ]

class WorkSheet:
    def __init__(self):
        self.link = "https://docs.google.com/spreadsheets/d/1FPthYKyRTUvzdw-COO1zesDRgMyOl7HCCc8EeZywKlA/edit?usp=sharing"
        self.account = gspread.service_account(filename='key.json')
        self.sheet = self.account.open_by_url(self.link).sheet1

    def append_request(self, subject, class_num, time, email):
        self.sheet.append_row([subject, class_num, time, email])

