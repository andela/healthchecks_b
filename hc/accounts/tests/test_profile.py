from django.core import mail

from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check
from hc.accounts.models import Profile


class ProfileTestCase(BaseTestCase):

    def test_it_sends_set_password_link(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 302

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token

        self.assertNotEqual(token, None)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Set password on healthchecks.io')
        self.assertIn("Hello,\n\nHere's a link to set a password for your account", mail.outbox[0].body)

    def test_it_sends_report(self):
        check = Check(name="Test Check", user=self.alice)
        check.save()

        self.alice.profile.send_report()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Monthly Report')
        self.assertIn('This is a monthly report sent by healthchecks.io', mail.outbox[0].body)

    def test_it_sends_daily_report(self):
        check = Check(name="Sample Test", user=self.alice)
        check.save()

        self.alice.profile.send_daily_report()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Daily Report')
        self.assertIn('This is a daily report sent by', mail.outbox[0].body)

    def test_it_sends_weekly_report(self):
        check = Check(name="Weekly Sample", user = self.alice)
        check.save()

        self.alice.profile.send_weekly_report()

        self.assertEqual(mail.outbox[0].subject, 'Weekly Report')
        self.assertIn('This is a weekly report sent by', mail.outbox[0].body)

    def test_it_adds_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        self.assertIsNotNone(member_emails)
        self.assertTrue("frank@example.org" in member_emails)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'You have been invited to join alice@example.org on healthchecks.io')
        self.assertIn('You will be able to manage their existing monitoring checks and set up new', mail.outbox[0].body)

    def test_add_team_member_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_removes_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_switches_to_own_team(self):
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "foo.svg")
        self.assertContains(r, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(r, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(r, "bobs-tag.svg")

    def test_it_creates_api_key(self):
        self.client.login(username="alice@example.org", password="password")
        #send request to accounts/profile/create_api_key
        form = {"create_api_key": ""}
        r = self.client.post("/accounts/profile/", form)

        self.assertEqual(r.status_code, 200)
        self.alice.profile.refresh_from_db()
        #ensure that alice's api_key is not empty
        self.assertIsNotNone(self.alice.profile.api_key)

    def test_it_revokes_api_key(self):
        self.client.login(username="alice@example.org", password="password")
        #send request to accounts/profile/revoke_api_key
        form = {"revoke_api_key": ""}
        self.client.post("/accounts/profile/", form)

        self.alice.profile.refresh_from_db()
        #ensure that alice's api_key is empty
        self.assertEqual(self.alice.profile.api_key, "")

    def test_status_code_of_page(self):
        r = self.client.get("/accounts/profile/")
        self.assertEqual(r.status_code, 302)
