# -*- coding: utf-8 -*-

import re

from django.db.models import Q
from iSM.models import Consorcio, Consorcista
from iSM.pdf_controller import PDFController


class InvalidDocumentException(Exception):
    pass


def _format_date(date_str):
    match = re.match(r'(\d{,2})/(\d{4})', date_str)
    if match:
        groups = match.groups()
        return '%d-%.2d-01' % (int(groups[1]), int(groups[0]))
    raise InvalidDocumentException, 'Invalid date'

def _check_email(email):
    email_re = re.compile(
        r"^([-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
        r'|"^([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
        r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?)$'
        r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$', re.IGNORECASE)
    return re.match(email_re, email)

def process_document(document):
    pdf_controller = PDFController(document)
    pdf_controller.parse()
    if not pdf_controller.layout:
        return
    layout_list = list(pdf_controller.layout)
    consorcio_name = pdf_controller.lookup_term('-1-')
    consorcio_name_extra = pdf_controller.lookup_term('-2-')

    if not consorcio_name or not consorcio_name_extra:
        raise InvalidDocumentException, 'Invalid building'

    consorcio_name = re.search('-1-(.+)', layout_list[consorcio_name[0]].get_text())
    consorcio_name_extra = re.search('-2-(.+)', layout_list[consorcio_name_extra[0]].get_text())
    if not consorcio_name or not consorcio_name_extra:
        raise InvalidDocumentException, 'Invalid building'
    else:
        consorcio_name_full = consorcio_name.groups()[0] + consorcio_name_extra.groups()[0]
        consorcio_name_full = consorcio_name_full.strip().replace('\n', ' - ').replace('"', '')

    titular = pdf_controller.lookup_term('titular')

    if not titular:
        raise InvalidDocumentException, 'Invalid holder'

    titular = re.search('-Titular-(.+)', layout_list[titular[0]].get_text())
    if not titular:
        raise InvalidDocumentException, 'Invalid holder'
    consorcista_name = titular.groups()[0].strip().replace('\n', '')

    emails = pdf_controller.lookup_term('-email-')
    if not emails:
        raise InvalidDocumentException, 'Invalid emails'
    emails = re.search('-email-(.+)', layout_list[emails[0]].get_text())

    if not emails:
        raise InvalidDocumentException, 'Invalid emails'

    emails = [ email.strip()
               for email in emails.groups()[0].strip().replace('\n', '').split('/')
               if _check_email(email.strip()) ]

    if not emails:
        raise InvalidDocumentException, 'Invalid emails'

    unidad = pdf_controller.lookup_term('-unidad-')
    if not unidad:
        raise InvalidDocumentException, 'Invalid block'

    unidad = re.search('-Unidad-(.+)', layout_list[unidad[0]].get_text())

    if not unidad:
        raise InvalidDocumentException, 'Invalid block'

    unidad = unidad.groups()[0].strip().replace('\n', '')
    belongs_to = pdf_controller.lookup_term('expensas mes:')

    if not belongs_to:
        raise InvalidDocumentException, 'Invalid date'

    belongs_to = re.search('EXPENSAS MES: (.+)', layout_list[belongs_to[0]].get_text())

    if not belongs_to:
        raise InvalidDocumentException, 'Invalid date'

    belongs_to = belongs_to.groups()[0].strip()

    consorcio = Consorcio.objects.get_or_create(name=consorcio_name_full)[0]

    consorcista = Consorcista.objects.get_or_create(unidad=unidad, name=consorcista_name, consorcio=consorcio)[0]
    consorcista.emails = '/'.join(emails)
    consorcista.save()

    return consorcista, _format_date(belongs_to)
