from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")


    ### Login and test it redirects already logged in
    def test_it_redirects_logged_in(self):

        form = {"email": "alice@example.org"}
        self.profile.refresh_from_db()
        token = self.profile.token

        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertEqual(r.status_code, 302 )

        self.assertRedirects(r, "/checks/")

    ### Login with a bad token and check that it redirects
    def test_it_redirects_after_bad_token(self):
        form = {"email": "alice@example.org"}

       #  self.profile.refresh_from_db()
        token = 'shah205-jeow@##-rmsqn2i'

        r = self.client.post("/accounts/check_token/alice/token/")
        self.assertEqual(r.status_code, 302)

        self.assertRedirects(r, '/accounts/login/')

    ### Any other tests?
