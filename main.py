import datetime

from reportlab.graphics.shapes import Drawing
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.barcode import code39, code93, code128
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import csv

CENNIK_WIDTH = 7 * cm
CENNIK_WIDTH_COUNT = 4



class Cennik:
    title = ''
    code = ''
    country = ''
    article = ''
    brand = ''
    price = ''
    qrcode = ''
    barcode = ''
    date = ''


def getCennik(title, code, country, article, brand, price):
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


fileName = 'pdfTable.pdf'

pdf = SimpleDocTemplate(fileName, pagesize=landscape(A4), topMargin=1*cm, bottommargin=1*cm)

pdfmetrics.registerFont(TTFont('Roboto-Medium', 'fonts/Roboto-Medium.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Regular', 'fonts/Roboto-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Bold', 'fonts/Roboto-Bold.ttf'))


def getCennikTable(cennik):
    titleTable = Table([
        [cennik.title]
    ], CENNIK_WIDTH, 0.65 * cm)

    codeTable = Table([
        ['Код: ', cennik.code]
    ])

    articleTable = Table([
        ['Артикул: ', cennik.article]
    ])

    countryTable = Table([
        ['Страна: ', cennik.country]
    ])

    brandTable = Table([
        ['Производитель: ', cennik.brand]
    ])

    code_article_country_brand_table = Table([
        [[codeTable], [articleTable]],
        [[countryTable], [brandTable]]
    ], [60])

    price_table = Table([[cennik.price, r'₽/шт.']])

    barcode_table = Table([[code128.Code128(cennik.barcode, barWidth=0.8, barHeight=12, quiet=False)]])

    dateTable = Table([[cennik.date]], [60])


    barcode_date_table = Table([
        [[barcode_table],
         [dateTable]],

    ])

    qrcode = QrCodeWidget(cennik.qrcode)
    b = qrcode.getBounds()
    qrcode.barWidth = 2.5 * cm
    qrcode.barHeight = 2.5 * cm
    qrcode_url_draw = Drawing(50, 50)
    qrcode_url_draw.add(qrcode)

    qrTable = Table([[qrcode_url_draw]])

    cennikTable = Table([
        [titleTable],
        [code_article_country_brand_table],
        [price_table],
        [barcode_date_table],
        [qrTable],
    ], CENNIK_WIDTH, rowHeights=(0.65 * cm, 0.95 * cm, 0.65 * cm, 0.75 * cm, 0.05 * cm))  # расположение по очереди

    titleTableStyle = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('FONTNAME', (0, 0), (-1, -1), 'Roboto-Medium'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        # ('BOX', (0, 0), (0, 0), 1, colors.black),
    ])
    titleTable.setStyle(titleTableStyle)

    codeTableStyle = TableStyle([
        ('FONTSIZE', (0, 0), (0, 0), 6),
        ('FONTSIZE', (1, 0), (1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, 0),
         'Roboto-Regular'
         ),
        ('FONTNAME', (1, 0), (1, 0),
         'Roboto-Medium'
         ),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('FONTSIZE', (1, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
    ])
    codeTable.setStyle(codeTableStyle)

    countryTableStyle = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('FONTNAME', (0, 0), (0, 0),
         'Roboto-Regular'
         ),
        ('FONTNAME', (-1, -1), (-1, -1),
         'Roboto-Medium'
         ),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
    ])
    countryTable.setStyle(countryTableStyle)

    articleTableStyle = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0),
         'Roboto-Regular'
         ),
        ('FONTNAME', (-1, -1), (-1, -1),
         'Roboto-Medium'
         ),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
    ])
    articleTable.setStyle(articleTableStyle)

    brandTableStyle = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('FONTNAME', (0, 0), (0, 0),
         'Roboto-Regular'
         ),
        ('FONTNAME', (-1, -1), (-1, -1),
         'Roboto-Medium'
         ),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
    ])
    brandTable.setStyle(brandTableStyle)

    code_article_country_brand_table_style = TableStyle([

        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])

    code_article_country_brand_table.setStyle(code_article_country_brand_table_style)

    price_table_style = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 7),
        ('BOTTOMPADDING', (-1, -1), (-1, -1), 0),
        ('VALIGN', (1, 0), (1, 0), 'BOTTOM'),
        ('FONTNAME', (0, 0), (0, 0),
         'Roboto-Bold'
         ),
        ('FONTSIZE', (0, 0), (0, 0), 15),
        ('FONTSIZE', (-1, -1), (-1, -1), 8),
        ('FONTNAME', (-1, -1), (-1, -1),
         'Roboto-Regular'
         ),

    ])
    price_table.setStyle(price_table_style)

    barcode_table_style = TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ])
    barcode_table.setStyle(barcode_table_style)

    dateTableStyle = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        # ('BOX', (0, 0), (-1, -1), .5, colors.black),
        ('FONTNAME', (-1, -1), (-1, -1),
         'Roboto-Regular'
         ),
        ('FONTSIZE', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ])
    dateTable.setStyle(dateTableStyle)

    barcode_data_table_style = TableStyle([

        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        # ('INNERGRID', (0, 0), (-1, -1), .5, colors.red),
    ])

    barcode_date_table.setStyle(barcode_data_table_style)

    qrTableStyle = TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 4.7 * cm),
        ('BOTTOPPADDING', (0, 0), (-1, -1), 0),

    ])
    qrTable.setStyle(qrTableStyle)

    cennikTableStyle = TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('LINEABOVE', (0, 1), (0, 1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])
    cennikTable.setStyle(cennikTableStyle)

    return cennikTable


def open_csv(filename):
    with open(filename) as csv_file:
        csvdata = csv.reader(csv_file, delimiter=';')
        cennik_table_data = []
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
            cennik_table_data.append(cennik_data)
        del cennik_table_data[0]
    return cennik_table_data


c = open_csv('cena1.csv')[0]
c1 = getCennikTable(
    getCennik(title=c['name'], code=c['code'], article=c['article'], brand=c['brand'], country=c['brand'],
              price=c['price']))

all_rows_table = []  # все ценники

row_table = []  # по 4 ценника в строке
for c in open_csv('cena1.csv'):
    if len(row_table) >= 4:
        all_rows_table.append(row_table)
        row_table = []
        row_table.append(getCennikTable(
            getCennik(title=c['name'], code=c['code'], article=c['article'], brand=c['brand'], country=c['brand'],
                      price=c['price'])))
    else:
        row_table.append(getCennikTable(
            getCennik(title=c['name'], code=c['code'], article=c['article'], brand=c['brand'], country=c['brand'],
                      price=c['price'])))


all_rows_table.append(row_table)

mainTable = Table(all_rows_table)
print(len(open_csv('cena1.csv')))
print(len(row_table))
print(len(all_rows_table))

mainTableStyle = TableStyle([
    ('TOPPADDING', (0, 0), (-1, -1), 1),
    ('LEFTPADDING', (0, 0), (-1, -1), 1),
    ('RIGHTPADDING', (0, 0), (-1, -1), 1),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
])
mainTable.setStyle(mainTableStyle)

elems = []
elems.append(mainTable)
pdf.build(elems)

if __name__ == '__main__':
    pass
