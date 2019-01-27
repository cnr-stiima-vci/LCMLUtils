import datetime

from django.utils import timezone
from django.test import TestCase

from .models import LCCS3Class, LCCS3Legend


class SimilarityTests(TestCase):
    
    def test1(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        print("test1 ongoing...")
        print(LCCS3Legend.objects.count())
        self.assertEqual(True,True)
