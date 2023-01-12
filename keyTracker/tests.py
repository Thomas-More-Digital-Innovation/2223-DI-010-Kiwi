from django.test import TestCase
from django.contrib.auth.models import User
from keyTracker import models
# Create your tests here.
# functions that need to run when 'manage.py test' is ran, have to start wih the word 'test'


class KeyTestCase(TestCase):
    def setUp(self):
        pass
        # key = models.Key(keyHolder=test_user, isReturned=False)

    def testTakeKey(self):
        test_user = User.objects.create_user(
            username="testUser", password="testPassword")

        key = models.Key(keyHolder=test_user, isReturned=False)
        key.save()
        self.assertEqual(key.isReturned, False)
        self.assertEqual(key.keyHolder, test_user)
