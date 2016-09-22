from hc.api.models import Check
from hc.test import BaseTestCase


class PauseTestCase(BaseTestCase):

    def test_it_works(self):
        check = Check(user=self.alice, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        ### Assert the expected status code and check's status
        self.assertEqual(r.status_code, 200)
        #* Post request to pause url changes status to pause
        self.assertEqual(r.json()['status'], 'paused', msg=r.json())

    def test_it_validates_ownership(self):
        check = Check(user=self.bob, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        self.assertEqual(r.status_code, 400)

    def test_accepts_post_requests_only(self):
        ### Test that it only allows post requests
        check = Check(user=self.bob, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r2 = self.client.get(url, HTTP_X_API_KEY='abc')
        self.assertEqual(r2.status_code, 405, msg=r2)
    
    