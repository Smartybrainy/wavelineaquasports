from .forms import ContactEnquiriesForm
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.forms.models import model_to_dict


class HomeView(View):

    def get(self, *args, **kwargs):
        template_name = 'main/index.html'
        contact_form = ContactEnquiriesForm()
        return render(self.request, template_name, {
            'contact_form': contact_form
        })

    def post(self, *args, **kwargs):
        form = ContactEnquiriesForm(self.request.POST or None)
        if form.is_valid():
            contact_form = form.save()
            return JsonResponse({'contact': model_to_dict(contact_form)}, status=200)


class AboutUs(View):
    def get(self, *args, **kwargs):
        template_name = "main/about.html"
        contact_form = ContactEnquiriesForm()
        return render(self.request, template_name, {'contact_form': contact_form})

    def post(self, *args, **kwargs):
        form = ContactEnquiriesForm(self.request.POST or None)
        if form.is_valid():
            contact_form = form.save()
            return JsonResponse({'contact': model_to_dict(contact_form)}, status=200)


class Programs(TemplateView):
    template_name = "main/programs.html"
