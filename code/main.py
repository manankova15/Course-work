from scripts.YandexToLTI import call_converter_from_yandex
from scripts.StepikToLTI import call_converter_from_stepic
from scripts.LTIToYandex import call_converter_to_yandex
from scripts.LTIToStepik import call_converter_to_stepik
import sys

if __name__ == '__main__':
    try:
        # call_converter_from_yandex()
        # print("\n+++++++++++++++++++++++++\n")
        # call_converter_from_stepic()
        # call_converter_to_yandex()
        call_converter_to_stepik()
    except AttributeError as er:
        print("Невозможно обработать файл из-за отсутствия какого-то из атрибутов, ", er)
    except:
        print("При обработке файла произошла ошибка, ", sys.exc_info())


