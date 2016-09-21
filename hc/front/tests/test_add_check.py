from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1
   
    ### Test that team access works
    def test_team_access_works(self):
        '''test if team  member can add checks'''
        url = "/checks/add/"
        for email in ["alice@example.org", "bob@example.org",
                                   "charlie@example.org", "migwi@andela.com"]:
            self.client.login(username=email, password="password")
            r = self.client.post(url)
            print (r)
            self.assertRedirects(r, "/checks/")
        # assert Check.objects.count() == 2
        print (Check.objects.count())