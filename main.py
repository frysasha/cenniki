import datetime

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from templates.regular_table import get_cennik_base_table
import csv

CENNIK_WIDTH = 7 * cm
CENNIK_WIDTH_COUNT = 4
TITLE_HEIGHT = 0.65 * cm

fileName = 'cenniki.pdf'

pdf = SimpleDocTemplate(fileName, pagesize=landscape(A4), topMargin=0 * cm, bottommargin=0 * cm)

pdfmetrics.registerFont(TTFont('Roboto-Medium', 'fonts/Roboto-Medium.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Regular', 'fonts/Roboto-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Bold', 'fonts/Roboto-Bold.ttf'))


class Cennik:
    title = None
    code = None
    country = None
    article = None
    brand = None
    price = None
    qrcode = None
    barcode = None
    date = None
    old_price = None
    discount_text = None
    discount_date = None


def create_cennik(title, code, country, article, brand, price):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='cennik_title', wordWrap=True, fontName='Roboto-Medium', fontSize=7,
                              leading=9))  # стиль параграфа (автоматом переносит строку) leading = отступ между строками
    cennik = Cennik()
    cennik.title = [Paragraph(title, styles['cennik_title'])]
    cennik.code = code
    cennik.country = country
    cennik.article = article
    cennik.brand = brand
    cennik.date = datetime.datetime.now().strftime('%d.%m.%Y')
    cennik.qrcode = f'https://ipro.etm.ru/cat/nn/{code}'
    cennik.barcode = f'ETM{code}'
    cennik.price = price

    return cennik





def get_cennik_data_from_csv(filename):
    with open(filename) as csv_file:
        csvdata = csv.reader(csv_file, delimiter=';')
        cennik_list_data = []
        for row in csvdata:
            cennik_data = {}
            code = row[0]
            name = row[1]
            article = row[2]
            brand = row[8]
            price = row[4]
            cennik_data['code'] = code
            cennik_data['name'] = name
            cennik_data['article'] = article
            cennik_data['brand'] = brand
            cennik_data['price'] = price.strip()
            cennik_list_data.append(cennik_data)
        del cennik_list_data[0]
    return cennik_list_data


def get_cennik_rows(cennik_data):
    all_rows_table = []  # все ценники
    row_table = []  # по 4 ценника в строке

    for c in cennik_data:
        if len(row_table) >= 4:
            all_rows_table.append(row_table)
            row_table = []
            row_table.append(get_cennik_base_table(
                create_cennik(title=c['name'], code=c['code'], article=c['article'], brand=c['brand'],
                              country=c['brand'],
                              price=c['price'])))
        else:
            row_table.append(get_cennik_base_table(
                create_cennik(title=c['name'], code=c['code'], article=c['article'], brand=c['brand'],
                              country=c['brand'],
                              price=c['price'])))

    all_rows_table.append(row_table)

    return all_rows_table


def build_main_table(cennik_table):
    main_table = Table(cennik_table)
    main_table_style = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ])
    main_table.setStyle(main_table_style)
    pdf.build([main_table])


def build_pdf(csv_file):
    cennik_data = get_cennik_data_from_csv(csv_file)
    cennik_table = get_cennik_rows(cennik_data)
    build_main_table(cennik_table)


if __name__ == '__main__':
    build_pdf('cena12.csv')
