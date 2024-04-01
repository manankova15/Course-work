from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import xml.dom.minidom
import xml.etree.ElementTree as ET
from scripts.LTIToStepik import call_converter_to_stepik
from scripts.LTIToYandex import call_converter_to_yandex
from scripts.LTIToLMS import call_converter_to_lms
from scripts.CrossConvertion import *

def home(request):
    return render(request, 'home.html')

def new_task(request):
    return render(request, 'newTask.html')

def convert(request):
    try:
        if request.method == 'POST':
            option = request.POST.get('conversion_option')

            uploaded_file = request.FILES.get('file')

            # Проверяем, загружен ли файл
            if not uploaded_file:
                return JsonResponse({'error': 'Please, upload file'}, status=400)

            if option == '1':
                result_json = call_converter_from_yandex(uploaded_file)
            elif option == '2':
                result_json = call_converter_from_stepic(uploaded_file)
            elif option == '3':
                result_json = call_converter_from_lms(uploaded_file)
            elif option == '4':
                result_json = call_converter_to_yandex(uploaded_file)
            elif option == '5':
                result_json = call_converter_to_stepik(uploaded_file)
            elif option == '6':
                result_json = call_converter_to_lms(uploaded_file)
            elif option == '7':
                result_json = convert_yandex_to_stepik(uploaded_file)
            elif option == '8':
                result_json = convert_yandex_to_smartlms(uploaded_file)
            elif option == '9':
                result_json = convert_stepik_to_yandex(uploaded_file)
            elif option == '10':
                result_json = convert_stepik_to_smartlms(uploaded_file)
            elif option == '11':
                result_json = convert_smartlms_to_yandex(uploaded_file)
            elif option == '12':
                result_json = convert_smartlms_to_stepik(uploaded_file)

            if option == '6' or option == '8' or option == '10':
                xml_string = xml.dom.minidom.parseString(ET.tostring(result_json)).toprettyxml()
                response = HttpResponse(xml_string, content_type='application/xml')
            else:
                response = JsonResponse(result_json, safe=False)

            return response
        else:
            return HttpResponse("Only POST method is supported for this endpoint.", status=405)
    except Exception as e:
        print("!!!!!")
        print(e)
        return JsonResponse({'error': f'Error during conversion'}, status=500)


def get_languages(request):
    programming_languages = ["Java", "Python", "JavaScript", "C", "C++", "C#", "Ruby", "Go", "Swift", "Kotlin", "Rust",
                             "PHP", "TypeScript", "Perl"]

    return render(request, 'my_template.html', {'programming_languages': programming_languages})
