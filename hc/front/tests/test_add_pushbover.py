
from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddPushoverTestCase(BaseTestCase):
    def test_it_adds_channel(self):
       self.client.login(username="alice@example.org", password="password")

       session = self.client.session
       session["po_nonce"] = "n"
       session.save()

       params = "pushover_user_key=a&nonce=n&prio=0"
       r = self.client.get("/integrations/add_pushover/?%s" % params)
       assert r.status_code == 302

       channels = list(Channel.objects.all())
       assert len(channels) == 1
       assert channels[0].value == "a|0" 

    def test_it_adds_channel(self):
       self.client.login(username="alice@example.org", password="password")

       session = self.client.session
       session["po_nonce"] = "n"
       session.save()

       params = "pushover_user_key=a&nonce=n&prio=0"
       r = self.client.get("/integrations/add_pushover/?%s" % params)
       assert r.status_code == 302

       channels = list(Channel.objects.all())
       assert len(channels) == 1
       assert channels[0].value == "a|0"

    @override_settings(PUSHOVER_API_TOKEN=None)
    def test_it_requires_api_token(self):
       self.client.login(username="alice@example.org", password="password")
       r = self.client.get("/integrations/add_pushover/")
       self.assertEqual(r.status_code, 404)


    @override_settings(PUSHOVER_API_TOKEN=None)
    def test_it_requires_api_token(self):
       self.client.login(username="alice@example.org", password="password")
       r = self.client.get("/integrations/add_pushover/")
       self.assertEqual(r.status_code, 404)

    def test_it_validates_nonce(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=INVALID&prio=0"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        assert r.status_code == 403

    ### Test that pushover validates priority
    def test_it_validates_priority(self):
        ''' -2 = generate no notification/alert, 
            -1 = always send as a quiet notification, 
             1 = display as high-priority and bypass the user's quiet hours,
             2 =  also require confirmation from the user
        '''
        self.client.login(username="alice@example.org", password="password")
        session = self.client.session
        session["po_nonce"] = "n"
        session.save()
        priority = 100
        good_list = ['-2','-1','0','1','2']
        params = "pushover_user_key=a&nonce=n&prio=%s" % priority
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        if priority in good_list:
            self.assertEqual(r.status_code , 302)
        else:
            self.assertEqual(r.status_code , 400)