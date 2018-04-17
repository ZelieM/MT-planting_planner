from datetime import date

from django.test import TestCase

from planner.import_vegetables_helpers import import_vegetables_to_garden
from planner.models import Garden, Vegetable

OP1_NAME = "DateOperation"
V1_NAME = "LibraryVeggie"


class ImportVegetableTests(TestCase):

    def setUp(self):
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        from vegetables_library.models import Vegetable as library_vegetable
        self.library_veggie = library_vegetable.objects.create(name=V1_NAME, variety="MyVariety")
        self.second_veggie = library_vegetable.objects.create(name="SecondVeggie", variety="SameVariety")
        from vegetables_library.models import COWithOffset as library_co_with_offset
        from vegetables_library.models import COWithDate as library_co_with_date
        op1 = library_co_with_date.objects.create(name=OP1_NAME, vegetable=self.second_veggie,
                                                  absoluteDate=date(2018, 10, 3))
        op2 = library_co_with_offset.objects.create(name="OffsetOp", vegetable=self.second_veggie,
                                                    previous_operation=op1, offset_in_days=3)
        library_co_with_offset.objects.create(name="SecondOffsetOp", vegetable=self.second_veggie,
                                              previous_operation=op2, offset_in_days=3)

    def test_import_simple_veggie(self):
        self.assertEqual(len(self.garden.vegetable_set.all()), 0)  # Currently no vegetables in this garden
        vegetable = [self.library_veggie.id]
        import_vegetables_to_garden(self.garden.id, vegetable)
        self.assertEqual(len(self.garden.vegetable_set.all()), 1)
        self.assertEqual(Vegetable.objects.get(name=V1_NAME).extern_id,
                         self.library_veggie.id)  # Check if the id of the original vegetable has been copied properly
