# -*- coding:utf-8 -*-

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator


class PDFController(object):
    def __init__(self, fd=None, password=''):
        self.fd = fd
        self.password = password
        self.parsed = False
        self.document = PDFDocument()
        self.laparams = LAParams()
        self.rsrcmgr = PDFResourceManager()
        self.device = PDFPageAggregator(self.rsrcmgr, laparams=self.laparams)
        self.layout = []

        if fd:
            self.open(fd, password)

    def open(self, fd, password=''):
        self.password = password
        self.fd = fd if hasattr(fd, 'read') else open(fd)

    def close(self):
        if self.fd:
            self.fd.close()
            self.fd = None
        self.parsed = False

    def parse(self):
        parser = PDFParser(self.fd)
        parser.set_document(self.document)
        self.document.set_parser(parser)
        self.document.initialize(self.password)
        if not self.document.is_extractable:
            self.fd.close()
            raise PDFTextExtractionNotAllowed

        if not self.layout:
            self.layout = self._get_layout()

        self.parsed = True

    def _get_layout(self):
        layout = []
        interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)
        for page in self.document.get_pages():
            interpreter.process_page(page)
            layout = self.device.get_result()
        return layout

    def lookup_term(self, term, ignore_case=True):
        layout_list = list(self.layout)
        indexes = [ i for i, v in enumerate(layout_list)
                    if hasattr(v, 'get_text') and (term.lower() if ignore_case else term) in
                        (v.get_text().lower() if ignore_case else v.get_text()) ]
        return indexes

    def __del__(self):
        self.fd.close()

    def __repr__(self):
        return '<PDFController> %s, %s' % ('Open file "%s"' % self.fd.name if self.fd else 'No file opened',
                                             'not parsed' if not self.parsed else 'parsed')
