from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase
#our imports
from django.contrib.auth.models import User
from hc.accounts.models import Member, Profile


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    ### Test that the team access works
    def test_team_access_works(self):
        # create user japtheth and add him to a team
        self.client.login(username="japheth@example.org", password="pass123")
        form = {"invite_team_member": "1", "email": "migwi@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        member_emails = set()
        for member in self.japheth.profile.member_set.all():
            member_emails.add(member.user.email)
        ### Assert the existence of the member emails as from the invite
        self.assertTrue("migwi@example.org" in member_emails)

        # create user b_ and add him to the same team
        # if user a_ create a cron job user b_ should be able to check the cron job
        pass

    ### Test that bad kinds don't work
    ### This test confirms that a bad kind actually raises a http error 404 
    def test_bad_kinds_dont_work(self):
        self.client.login(username="migwi@example.org", password="pass")
        bad_kind = "andela"
        url = "/integrations/add_%s/" % bad_kind
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404)

    def test_team_access_works(self):
        self.brian = User(username='brian', email='brian@example.org')
        self.brian.set_password('pass123')
        self.brian.save()

        self.profile = Profile(user=self.brian, api_key='abc')
        self.profile.team_access_allowed = True
        self.profile.save()

        #arnold your

        self.arnold = User(username='arnold', email='arnold@example.org')
        self.arnold.set_password("pass124")
        self.arnold.save()

        self.arnolds_profile = Profile(user=self.arnold)
        self.arnolds_profile.current_team = self.profile
        self.arnolds_profile.save()


