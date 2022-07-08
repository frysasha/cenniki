from cennik_settings import CENNIK_WIDTH, CENNIK_WIDTH_COUNT, TITLE_HEIGHT
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.barcode import code39, code93, code128
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing


def get_cennik_base_table(cennik):
    title_table = Table([
        [cennik.title]
    ], CENNIK_WIDTH, TITLE_HEIGHT)

    code_table = Table([
        ['Код: ', cennik.code]
    ])

    article_table = Table([
        ['Артикул: ', cennik.article]
    ])

    country_table = Table([
        ['Страна: ', cennik.country]
    ])

    brand_table = Table([
        ['Производитель: ', cennik.brand]
    ])

    code_article_country_brand_table = Table([
        [[code_table], [article_table]],
        [[country_table], [brand_table]]
    ], [60])

    price_table = Table([[cennik.price, r'₽/шт.']])

    old_price_table = Table([[cennik.old_price]])
    stock_date_table = Table([[cennik.discount_date]])
    discount_text_table = Table([[cennik.discount_text]])

    price_and_text_table = Table([
        [[old_price_table], [price_table]],
        [[stock_date_table], [discount_text_table]],
    ])

    barcode_table = Table([[code128.Code128(cennik.barcode, barWidth=0.65, barHeight=0.6 * cm, quiet=False)]])

    date_table = Table([[cennik.date]], [60])

    barcode_date_table = Table([
        [[barcode_table],
         [date_table]]
    ], [3 * cm])

    ipro_text_table = Table([
        ['Покупай в IPRO']
    ])

    qrcode = QrCodeWidget(cennik.qrcode)
    b = qrcode.getBounds()
    qrcode.barWidth = 2.5 * cm
    qrcode.barHeight = 2.5 * cm
    qrcode_url_draw = Drawing(50, 50)
    qrcode_url_draw.add(qrcode)

    qr_code_table = Table([[qrcode_url_draw]])

    ipro_text_qr_code_table = Table([
        [ipro_text_table],
        [qr_code_table],
    ])

    cennik_table = Table([
        [title_table],
        [code_article_country_brand_table],
        [price_and_text_table],
        [barcode_date_table],
        [ipro_text_qr_code_table],
    ], CENNIK_WIDTH, rowHeights=(0.65 * cm, 0.95 * cm, 0.60 * cm, 0.75 * cm, 0.05 * cm))  # расположение по очереди

    title_table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('FONTNAME', (0, 0), (-1, -1), 'Roboto-Medium'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])
    title_table.setStyle(title_table_style)

    code_table_style = TableStyle([
        ('FONTSIZE', (0, 0), (0, 0), 6),
        ('FONTSIZE', (1, 0), (1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, 0), 'Roboto-Regular'),
        ('FONTNAME', (1, 0), (1, 0), 'Roboto-Medium'),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('FONTSIZE', (1, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
    ])
    code_table.setStyle(code_table_style)

    country_table_style = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('FONTNAME', (0, 0), (0, 0), 'Roboto-Regular'),
        ('FONTNAME', (-1, -1), (-1, -1), 'Roboto-Medium'),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
    ])
    country_table.setStyle(country_table_style)

    article_table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Roboto-Regular'),
        ('FONTNAME', (-1, -1), (-1, -1), 'Roboto-Medium'),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
    ])
    article_table.setStyle(article_table_style)

    brand_table_style = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('FONTNAME', (0, 0), (0, 0), 'Roboto-Regular'),
        ('FONTNAME', (-1, -1), (-1, -1), 'Roboto-Medium'),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
    ])
    brand_table.setStyle(brand_table_style)

    code_article_country_brand_table_style = TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])
    code_article_country_brand_table.setStyle(code_article_country_brand_table_style)

    price_and_text_table_style = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 7),
        ('BOTTOMPADDING', (-1, -1), (-1, -1), 0),
        ('VALIGN', (1, 0), (1, 0), 'BOTTOM'),
        ('FONTNAME', (0, 0), (0, 0), 'Roboto-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 15),
        ('FONTSIZE', (-1, -1), (-1, -1), 8),
        ('FONTNAME', (-1, -1), (-1, -1), 'Roboto-Regular'),
    ])
    price_and_text_table.setStyle(price_and_text_table_style)

    barcode_table_style = TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ])
    barcode_table.setStyle(barcode_table_style)

    date_table_style = TableStyle([
        # ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), -6),
        ('FONTNAME', (-1, -1), (-1, -1), 'Roboto-Regular'),
        ('FONTSIZE', (0, 0), (-1, -1), 4),
        # ('BOX', (0, 0), (-1, -1), .5, colors.red),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ])
    date_table.setStyle(date_table_style)

    barcode_date_table_style = TableStyle([

        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        # ('BOX', (0, 0), (-1, -1), .5, colors.red),
        # ('INNERGRID', (0, 0), (-1, -1), .5, colors.red),
    ])
    barcode_date_table.setStyle(barcode_date_table_style)

    ipro_text_table_style = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 13.3),
        ('FONTNAME', (0, 0), (0, 0), 'Roboto-Regular'),
        ('FONTSIZE', (0, 0), (0, 0), 4),
    ])
    ipro_text_table.setStyle(ipro_text_table_style)

    ipro_text_qr_code_table_style = TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 4.45 * cm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), -8),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        # ('BOX', (0, 0), (-1, -1), .5, colors.red),
        # ('INNERGRID', (0, 0), (-1, -1), .5, colors.red),
    ])
    ipro_text_qr_code_table.setStyle(ipro_text_qr_code_table_style)

    cennik_table_style = TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('LINEABOVE', (0, 1), (0, 1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])
    cennik_table.setStyle(cennik_table_style)

    return cennik_table