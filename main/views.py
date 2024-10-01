from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpRequest, HttpResponse
from main.models import VTUResult


class IndexView(View):


    def get(self, request:HttpRequest)->HttpResponse:
        return render(request, "main/index.html")
    
class AboutView(TemplateView):
    template_name = "main/about.html"

class UploadView(View):

    def get(self, request:HttpRequest)->HttpResponse:
        results = VTUResult.objects.all()
        return render(request, "main/upload.html", {
            "results":results
        })