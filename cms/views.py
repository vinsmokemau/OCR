"""."""
import xlrd
import xlwt
from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView,
    FormView,
)
import cv2
import pytesseract
from .models import Image
from .forms import ImageForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from scripts.ocr_funcion import OCR_extraccion
from django.contrib.auth.mixins import LoginRequiredMixin


class ImageCreate(LoginRequiredMixin, CreateView):
    model = Image
    fields = [
        'image',
        'excel',
    ]
    template_name = 'home.html'

    def form_valid(self, form):
        self.image = form.cleaned_data['image']
        return super(ImageCreate, self).form_valid(form)

    def get_succes_url(self):
        return self.object.get_absolute_url()


class ImageDetailView(LoginRequiredMixin, DetailView):

    model = Image
    template_name = "image.html"
    pk_url_kwarg = 'image_id'
    context_object_name= 'image'

    def get_context_data(self, **kwargs):
        context = super(ImageDetailView, self).get_context_data(**kwargs)
        extraction = OCR_extraccion('media/' + str(self.object.image))
        names = [extraction[name_id] for name_id in extraction]
        context['names_found'] = names
        wb = xlrd.open_workbook('media/' + str(self.object.excel)) 
        sheet = wb.sheet_by_index(0)
        excel_names = [sheet.row_values(row) for row in range(1, sheet.nrows)]
        related_names = []
        for excel_name in excel_names:
            if excel_name[2] in names:
                related_names.append(excel_name)
        context['related_names'] = related_names
        return context


def export_results_xls(request, image_id):
    obj = get_object_or_404(Image, pk=image_id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="results.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Resultados')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        '#',
        'Registro SIP',
        'Nombre',
        'Genero',
        'Tipo De Investigacion',
        'Titulo del Poryecto',
        'Resumen',
        'Objetivo',
        'Adscrito',
        'Nivel',
        'Carrera',
        'Grado Academico',
        'Fecha de Captura',
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    extraction = OCR_extraccion('media/' + str(obj.image))
    names = [extraction[name_id] for name_id in extraction]

    wb_read = xlrd.open_workbook('media/' + str(obj.excel))
    sheet = wb_read.sheet_by_index(0)
    excel_names = [sheet.row_values(row)[2] for row in range(1, sheet.nrows)]
    related_names = []

    count = 1
    for excel_name in excel_names:
        if excel_name in names:
            row_num += 1
            row = sheet.row_values(count)
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        count += 1

    wb.save(response)
    return response
