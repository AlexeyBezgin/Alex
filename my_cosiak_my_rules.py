<<<<<<< HEAD
import clr
clr.AddReference('RevitAPI')
import Autodesk.Revit.DB as DB

import System
clr.AddReference('System.Core')
clr.ImportExtensions(System.Linq)

uiapp = __revit__  # type:ignore
doc = uiapp.ActiveUIDocument.Document

# ===============================================================
def family_get_familyInstances(family, document=doc):  # noqa
    '''return List DB.FamilyInstance'''
    filter_FamilyInstance = DB.ElementClassFilter(DB.FamilyInstance)
    familyInstance_ids = family.GetDependentElements(filter_FamilyInstance)
    familyInstances = [document.GetElement(Id) for Id in familyInstance_ids]

    return familyInstances

def family_get_familySymbol(family):  # noqa
    '''return List[Autodesk.Revit.DB.ElementId] '''
    filter_familySymbol = DB.ElementClassFilter(DB.FamilySymbol)
    dbIds = family.GetDependentElements(filter_familySymbol)

    return dbIds


def familyHasInstanceBool(family, document=doc):  # noqa
    if len(family_get_familyInstances(family)):
        return True


def family_get_dependet_instances(family):
    return

# ===============================================================

familyHasInstances = list(
    DB.FilteredElementCollector(doc)
    .OfClass(DB.Family)
    .Where(familyHasInstanceBool))

result = 0

for family in familyHasInstances:
    if family.Id.IntegerValue > 100000:
        result += sum([db_id.IntegerValue for db_id in family_get_familySymbol(family)])
    else:
        result += sum([instance.Id.IntegerValue for instance in family_get_dependet_instances(family)])

print ("{} {}".format("Решение result =", result))
=======
def pick_rooms():
    references = uidoc.Selection.PickObjects(
        Selection.ObjectType.Element, RoomSelectionFilter(),
        'Выделите помещения')
    return [doc.GetElement(reference)
for reference in references]
>>>>>>> c3ec813 (Сделал другую функцию в тестовом модуле)
