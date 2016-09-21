from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1
   
   
    def test_team_access_works(self):
        print ('Object Count 1:',Check.objects.count())
        url = url = "/checks/add/"
        
        self.client.login(username="charlie@example.org", password="password")
        r = self.client.post(url)
        self.assertEqual(Check.objects.all()[0].user, 'charlie') # expected: charlies's check made

        # Add the first team check by alice
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertEqual(Check.objects.all()[1].user),'alice') # expected: alice's check made
        #second check should belong to alice since they are not group members


