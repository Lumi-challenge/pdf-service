month_mapper = {
    'JAN': '01',
    'FEV': '02',
    'MAR': '03',
    'ABR': '04',
    'MAI': '05',
    'JUN': '06',
    'JUL': '07',
    'AGO': '08',
    'SET': '09',
    'OUT': '10',
    'NOV': '11',
    'DEZ': '12'
}

def handle_month_year(string):
    month = string.split("/")[0]
    year = string.split("/")[1]
    return month_mapper[month], year