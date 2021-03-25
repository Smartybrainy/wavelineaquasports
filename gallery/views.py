from django.shortcuts import render
from django.views.generic import TemplateView


class GalleryView(TemplateView):
    template_name = 'gallery/gallery.html'
