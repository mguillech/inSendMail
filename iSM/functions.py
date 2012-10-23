# -*- coding: utf-8 -*-

import re

from django.db.models import Q
from iSM.models import Consorcio, Consorcista
from iSM.pdf_controller import PDFController


class InvalidDateException(Exception):
    pass


def _format_date(date_str):
    match = re.match(r'(\d{,2})/(\d{4})', date_str)
    if match:
        groups = match.groups()
        return '%d-%.2d-01' % (int(groups[1]), int(groups[0]))
    raise InvalidDateException, date_str

def process_document(document):
    pdf_controller = PDFController(document)
    pdf_controller.parse()
    if not pdf_controller.layout:
        return
    layout_list = list(pdf_controller.layout)
    consorcio_name = layout_list[0]

    if consorcio_name and hasattr(consorcio_name, 'get_text'):
        consorcio_name = consorcio_name.get_text().strip().replace('\n', ' - ').replace('"', '')
    titular = pdf_controller.lookup_term('titular')
    consorcista_name = layout_list[titular[0] + 1].get_text().strip().replace('\n', '')
    emails = pdf_controller.lookup_term('E_mail', False)
    emails = [ email.strip()
               for email in layout_list[emails[0] +1].get_text().strip().replace('\n', '').split('/') ]
    unidades = pdf_controller.lookup_term('unidad:')
    unidad = layout_list[unidades[0] + 1].get_text().strip().replace('\n', '')
    belongs_to = pdf_controller.lookup_term('expensas mes')
    belongs_to = layout_list[belongs_to[0]].get_text().split(':')[1].strip()

    consorcio = Consorcio.objects.get_or_create(name=consorcio_name)[0]

    consorcista = Consorcista.objects.filter(Q(emails__in=emails) | Q(emails='/'.join(emails)),
        name=consorcista_name)
    if not consorcista:
        consorcista = Consorcista.objects.create(unidad=unidad, name=consorcista_name,
            emails='/'.join(emails), consorcio=consorcio)
        consorcista.save()
    else:
        consorcista = consorcista.get()

    return consorcista, _format_date(belongs_to)
