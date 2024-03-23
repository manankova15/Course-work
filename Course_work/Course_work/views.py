from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from scripts.LTIToStepik import call_converter_to_stepik
from scripts.LTIToYandex import call_converter_to_yandex
from scripts.LTIToLMS import call_converter_to_lms
from scripts.YandexToLTI import call_converter_from_yandex
from scripts.StepikToLTI import call_converter_from_stepic
from scripts.LMSToLTI import call_converter_from_lms
import xml.dom.minidom
import xml.etree.ElementTree as ET



def home(request):
    return render(request, 'home.html')

def convert(request):
    try:
        if request.method == 'POST':
            option = request.POST.get('conversion_option')

            # Получаем файл из запроса
            uploaded_file = request.FILES.get('file')

            # Проверяем, загружен ли файл
            if not uploaded_file:
                # Если файл не загружен, возвращаем сообщение об ошибке
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

            if option == '6':
                # Преобразование JSON в XML с помощью xml.dom.minidom
                # xml_string = (result_json).toprettyxml()
                # xml_string = xml.dom.minidom(result_json).toprettyxml()
                # xml_string = ET.tostring(result_json, encoding='utf-8').decode().preattyfy()
                # response = JsonResponse(xml_string, safe=False)

                xml_string = xml.dom.minidom.parseString(ET.tostring(result_json)).toprettyxml()
                response = HttpResponse(xml_string, content_type='application/xml')
            else:
                # Возвращаем результат в формате JSON
                response = JsonResponse(result_json, safe=False)

            # Если параметр format равен 'download', возвращаем файл в нужном формате
            if request.GET.get('format') == 'download':
                if option == '6':
                    filename = 'converted_file.xml'  # Имя файла для формата XML
                    response = HttpResponse(xml_string, content_type='application/xml')
                elif option == '5':
                    filename = 'converted_file.step'  # Имя файла для формата STEP
                    response = HttpResponse(result_json, content_type='application/step')
                else:
                    filename = 'converted_file.json'  # Имя файла по умолчанию
                    response = HttpResponse(result_json, content_type='application/json')

                # response = HttpResponse(result_json, content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response
        else:
            return HttpResponse("Only POST method is supported for this endpoint.", status=405)
    except Exception as e:
        # Если произошла ошибка, возвращаем сообщение об ошибке
        print("!!!!!")
        print(e)
        return JsonResponse({'error': f'Error during conversion'}, status=500)


