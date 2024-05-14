# -*- coding: utf-8 -*-
import clr

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit import DB

import sys
sys.path.append(r"C:\Program Files (x86)\IronPython 2.7\Lib")
sys.path.append(r"X:\01_Скрипты\05_BIM_Модули")
from ingp import doc, is_dynamo
from ingp_errors import CustomWarningError
from ingp_dialog import mbox2

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

import math
clr.AddReference("System.Windows.Forms")

import System
from System.Collections.Generic import List


def get_name_starts_with(type_name, starts_name):
    name_starts_with = type_name.startswith(starts_name)
    return name_starts_with


# Преобразование питоновского списка в шарповский List, наследник ICollection
def get_multicategoryfilter(built_in_categories):
    built_in_categories = List[DB.BuiltInCategory](built_in_categories)
    multicategoryfilter = DB.ElementMulticategoryFilter(built_in_categories)
    return multicategoryfilter


def get_family_name(element):
    famname = element.get_Parameter(DB.BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()
    return famname


def get_type_name(elements):
    names = []
    if not isinstance(elements, (list, tuple, List[object])):
        elements = [elements]
    
    for element in elements:
        if hasattr(element, 'GetTypeId'):
            element_type = doc.GetElement(element.GetTypeId())
            name = element_type.Parameter[DB.BuiltInParameter.SYMBOL_NAME_PARAM].AsString()
        else:
            name = ""
        names.append(name)
            
    return names


def elems_grouper():
    a = DB.BuiltInCategory
    multicategoryfilter = get_multicategoryfilter([a.OST_Walls, a.OST_StructuralFoundation, a.OST_StructuralColumns, a.OST_Floors, a.OST_StructuralFraming, a.OST_GenericModel])
    elements = DB.FilteredElementCollector(doc).WherePasses(multicategoryfilter).WhereElementIsNotElementType().ToElements()
    
    global badelements
    
    elements_ПС = []
    elements_Шпунт_Трубчатый = []
    elements_Сваи = []
    elements_ФП = []
    elements_ГИ = []
    elements_Стены = []
    elements_Плиты = []
    elements_Колонны_Прямоугольные = []
    elements_Колонны_Круглые = []
    elements_Балки = []
    elements_ЛМ_Монолит = []
    elements_ЛМ_Сборный = []
    elements_ЛП_Монолит = []
    elements_ЛП_Сборный = []
    elements_Рампы = []
    elements_ДШ = []
    elements_Парапеты = []
    elements_Термовкладыши = []
    elements_Отверстия = []
    elements_Панель_Стеновая = []
    elements_Панель_Перекрытия = []
    elements_Капители = []
    badelements = []
    elements_badelements = []
    
    for element in elements:
        type_name = " ".join(get_type_name(element))
        family_name = get_family_name(element)
        if get_name_starts_with(type_name, "ПС_"):
            elements_ПС.append(element)
        elif get_name_starts_with(type_name, "СВ_ЖБ_"):
            elements_Сваи.append(element)
        elif get_name_starts_with(type_name, "ФП_ЖБ_"):
            elements_ФП.append(element)
        elif get_name_starts_with(type_name, "ГИ_"):
            elements_ГИ.append(element)
        elif get_name_starts_with(type_name, "СТ_ЖБ_"):
            elements_Стены.append(element)
        elif get_name_starts_with(type_name, "П_ЖБ_"):
            elements_Плиты.append(element)
        elif get_name_starts_with(type_name, "К_ЖБ_") and "Круглая" in family_name:
            elements_Колонны_Круглые.append(element)
        elif get_name_starts_with(type_name, "К_ЖБ_"):
            elements_Колонны_Прямоугольные.append(element)
        elif get_name_starts_with(type_name, "Б_ЖБ_"):
            elements_Балки.append(element)
        elif get_name_starts_with(type_name, "ЛМ_ЖБ_"):
            elements_ЛМ_Монолит.append(element)
        elif get_name_starts_with(type_name, "ЛМ_СМ_"):
            elements_ЛМ_Сборный.append(element)
        elif get_name_starts_with(type_name, "ЛП_ЖБ_"):
            elements_ЛП_Монолит.append(element)
        elif get_name_starts_with(type_name, "ПП_ЛП_"):
            elements_ЛП_Сборный.append(element)
        elif get_name_starts_with(type_name, "РАМП_ЖБ_"):
            elements_Рампы.append(element)
        elif get_name_starts_with(type_name, "К_КМ_ТР_"):
            elements_Шпунт_Трубчатый.append(element)
        elif get_name_starts_with(type_name, "СП_"):
            elements_Панель_Стеновая.append(element)
        elif get_name_starts_with(type_name, "ВСП_"):
            elements_Панель_Стеновая.append(element)
        elif get_name_starts_with(type_name, "НСП_"):
            elements_Панель_Стеновая.append(element)
        elif get_name_starts_with(type_name, "ПП_"):
            elements_Панель_Перекрытия.append(element)
        elif get_name_starts_with(type_name, "КАП_ЖБ_"):
            elements_Капители.append(element)
        elif "ДШ" in type_name:
            elements_ДШ.append(element)
        elif get_name_starts_with(type_name, "ПАР_ЖБ_"):
            elements_Парапеты.append(element)
        elif type_name == '"Rockwool" ВЕНТИ БАТТС':
            elements_Термовкладыши.append(element)
        else:
            elements_badelements.append(element)
            if type_name not in badelements:
                badelements.append(type_name)
                
            
    elements_dict = {
        "Фундаментные плиты" : elements_ФП,
        "Колонны_Круглые" : elements_Колонны_Круглые,
        "Колонны_Прямоугольные" : elements_Колонны_Прямоугольные,
        "ЛМ_Монолит" : elements_ЛМ_Монолит,
        "ЛП_Монолит" : elements_ЛП_Монолит,
        "Шпунт_Трубчатый" : elements_Шпунт_Трубчатый,
        "Стены" : elements_Стены,
        "Парапеты" : elements_Парапеты,
        "Панель_Стеновая" : elements_Панель_Стеновая,
        "Панель_Перекрытия" : elements_Панель_Перекрытия,
        "Плиты" : elements_Плиты,
        "Балки" : elements_Балки,
        "Капители" : elements_Капители,
        "Рампы" : elements_Рампы,
        "ЛМ_Сборный" : elements_ЛМ_Сборный,
        "ЛП_Сборный" : elements_ЛП_Сборный,
        "Термовкладыши" : elements_Термовкладыши,
        "badelements" : elements_badelements,
    }
    
    return elements_dict