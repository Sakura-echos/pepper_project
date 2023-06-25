from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'pepper/home.html')

def data_plotter(request):
    return render(request, 'pepper/data_plotter.html')

def download_data(request):
    return render(request, 'pepper/download_data.html')

def upload_new_data(request):
    return render(request, 'pepper/upload_new_data.html')

def polydispersivity_tool(request):
    return render(request, 'pepper/polydispersivity_tool.html')

def literature_finder(request):
    return render(request, 'pepper/literature_finder.html')