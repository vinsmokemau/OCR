"""."""
import xlrd
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
from django.urls import reverse_lazy
from scripts.ocr_funcion import OCR_extraccion


class ImageCreate(CreateView):
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


class ImageDetailView(DetailView):

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
        excel_names = [sheet.row_values(row)[2] for row in range(1, sheet.nrows)]
        related_names = []
        for excel_name in excel_names:
            if excel_name in names:
                related_names.append(excel_name)
        context['related_names'] = related_names
        return context
