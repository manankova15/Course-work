from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from scripts.LTIToStepik import call_converter_to_stepik
from scripts.LTIToYandex import call_converter_to_yandex
from scripts.LTIToLMS import call_converter_to_lms
from scripts.YandexToLTI import call_converter_from_yandex
from scripts.StepikToLTI import call_converter_from_stepic
from scripts.LMSToLTI import call_converter_from_lms


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

            # Возвращаем результат в формате JSON
            return JsonResponse(result_json, safe=False)
        else:
            return HttpResponse("Only POST method is supported for this endpoint.", status=405)
    except Exception as e:
        # Если произошла ошибка, возвращаем сообщение об ошибке
        return JsonResponse({'error': 'Error during conversion'}, status=500)


