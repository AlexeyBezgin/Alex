<<<<<<< HEAD
def pick_rooms():
    references = uidoc.Selection.PickObjects(
        Selection.ObjectType.Element, RoomSelectionFilter(),
        'Выделите помещения')
    return [doc.GetElement(reference)
for reference in references]
=======
>>>>>>> parent of 8642c3e (Добавил наполнение тестовому модулю)
