def pick_rooms():
    references = uidoc.Selection.PickObjects(
        Selection.ObjectType.Element, RoomSelectionFilter(),
        'Выделите помещения')
    return [doc.GetElement(reference)
for reference in references]