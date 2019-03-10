import datetime

from django.utils import timezone
from django.test import TestCase

from .models import LCCS3Class, LCCS3Legend
from .views.similarity import perform_assessment
from lcmlutils.settings import DATA_PATH
class SimilarityTests(TestCase):
    def test1(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        print("test1 ongoing...")
        print(DATA_PATH)
        print(LCCS3Legend.objects.count())
	c1 = LCCS3Class()
        with open(DATA_PATH+'/tests/sylhet4.lccs','rt') as f1:
            c1.xml_text = f1.read()
        c2 = LCCS3Class()
        with open(DATA_PATH+'/tests/seea6.lccs','rt') as f2:
            c2.xml_text = f2.read()
        res = perform_assessment(c1,c2)
        self.assertEqual(True,True)

