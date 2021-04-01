from io import StringIO, BytesIO
from typing import Tuple

from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from pathlib import Path
from enum import Enum

from xhtml2pdf import pisa
from xhtml2pdf.context import pisaContext

url = getattr(settings, 'FRONT_URL', '')
pdf_directory = getattr(settings, 'TEMPLATES')[0]['DIRS'][1]


class PdfType(Enum):
    Show_groups = 0


def get_pdf(pdf_type: PdfType, data, pdf_id=0):
    if pdf_type is PdfType.Show_groups:
        pdf = 'show_groups'
    else:
        return None

    path = f'{pdf_id}/{pdf}'
    if not Path(f'{pdf_directory}/{path}.html').exists():
        path = f'default/{pdf}'

    context = {'pagesize': 'A4', "groups": data}

    html_rendered = render_to_string(f'{path}.html', context=context)
    return html_rendered


def generate_groups_pdf(groups) -> Tuple[pisaContext, BytesIO]:
    html_rendered = get_pdf(PdfType.Show_groups, groups)

    result = BytesIO()
    pdf = pisa.pisaDocument(StringIO(html_rendered), dest=result)
    return pdf, result
