from planner.models import Vegetable, COWithDate, COWithOffset


def import_vegetables_to_garden(garden_id, vegetables_selected):
    from vegetables_library.models import Vegetable as library_vegetable
    for v in vegetables_selected:
        current_vegetable = library_vegetable.objects.get(pk=v)
        copy_vegetable(garden_id, current_vegetable)


def copy_vegetable(garden_id, vegetable_from_library):
    """ Copy a vegetable coming from the library to the garden's own library (with id garden_id)"""
    from vegetables_library.models import CulturalOperation as library_operation
    from vegetables_library.models import COWithOffset as library_co_with_offset
    from vegetables_library.models import COWithDate as library_co_with_date
    # If the vegetable is already existing in the garden, we return without copying it again
    if not len(Vegetable.objects.filter(garden_id=garden_id, extern_id=vegetable_from_library.id)):
        copied_vegetable = Vegetable.objects.create(garden_id=garden_id, name=vegetable_from_library.name,
                                                    extern_id=vegetable_from_library.id)
        operations_to_copy = library_operation.objects.select_subclasses().filter(vegetable_id=vegetable_from_library.id)
        for op in operations_to_copy:
            if type(op) is library_co_with_date:
                co = COWithDate.objects.create(vegetable_id=copied_vegetable.id, name=op.name, duration=op.duration,
                                               absoluteDate=op.absoluteDate)
                co_with_offset_to_copy = library_co_with_offset.objects.filter(vegetable=vegetable_from_library,
                                                                               previous_operation=op)
                copy_with_recursion_co_with_offset(copied_vegetable.id, co_with_offset_to_copy, op, co)


def copy_with_recursion_co_with_offset(vegetable_concerned_id, operations_from_library_to_copy, library_parent_co,
                                       garden_parent_co):
    """ Copy a cultural operation with offset and all the cultural operation with offset depending on this one"""
    if not operations_from_library_to_copy:
        return None  # End of recursion
    for co_offset in operations_from_library_to_copy:
        new_garden_parent = copy_co_with_offset(vegetable_concerned_id, co_offset, garden_parent_co)
        from vegetables_library.models import COWithOffset as library_co_with_offset
        child_operations = library_co_with_offset.objects.filter(vegetable=library_parent_co.vegetable,
                                                                 previous_operation=co_offset)
        copy_with_recursion_co_with_offset(vegetable_concerned_id, child_operations, co_offset, new_garden_parent)


def copy_co_with_offset(vegetable_concerned_id, operation_to_copy, parent_co):
    """ Copy a cultural operation with offset from the library to a vegetable belonging to the garden"""
    return COWithOffset.objects.create(vegetable_id=vegetable_concerned_id, name=operation_to_copy.name,
                                       duration=operation_to_copy.duration, previous_operation=parent_co,
                                       offset_in_days=operation_to_copy.offset_in_days)
