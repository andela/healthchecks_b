from django.test import Client, TestCase

from hc.api.models import Check, Ping


class PingTestCase(TestCase):

    def setUp(self):
        super(PingTestCase, self).setUp()
        self.check = Check.objects.create()

    def test_it_works(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        assert r.status_code == 200

        self.check.refresh_from_db()
        assert self.check.status == "up"

        ping = Ping.objects.latest("id")
        assert ping.scheme == "http"

    def test_it_handles_bad_uuid(self):
        r = self.client.get("/ping/not-uuid/")
        assert r.status_code == 400

    def test_it_handles_120_char_ua(self):
        ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/44.0.2403.89 Safari/537.36")

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)
        assert r.status_code == 200

        ping = Ping.objects.latest("id")
        assert ping.ua == ua

    def test_it_truncates_long_ua(self):
        ua = "01234567890" * 30

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)
        assert r.status_code == 200

        ping = Ping.objects.latest("id")
        assert len(ping.ua) == 200
        assert ua.startswith(ping.ua)

    def test_it_reads_forwarded_ip(self):
        ip = "1.1.1.1"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip)
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's remote address
<<<<<<< HEAD
        self.assertEqual(r.status_code, 200)
=======
        self.assertEqual(r.status_code, 200) 
>>>>>>> e79625ae6d99b40fcc672cd64a06e77e1e79ecaa
        self.assertEqual(ping.remote_addr, ip)

        ip = "1.1.1.1, 2.2.2.2"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip, REMOTE_ADDR="3.3.3.3")
        ping = Ping.objects.latest("id")
        assert r.status_code == 200
        assert ping.remote_addr == "1.1.1.1"

    def test_it_reads_forwarded_protocol(self):
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_PROTO="https")
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's scheme
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ping.scheme, 'https')

    def test_it_never_caches(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        assert "no-cache" in r.get("Cache-Control")

    ### Test that when a ping is made a check with a paused status changes status
    def test_check_status_change(self):
        self.check.status = 'paused'
        self.check.save()
        r = self.client.get("/ping/%s/" % self.check.code)
        self.assertTrue(r.status_code == 200, msg=r.status_code)


    ### Test that a post to a ping works
    def test_post_to_ping_works(self):
        url="/ping/"+str(self.check.code)+"/"
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")
        self.assertEqual(r.status_code, 200, msg=r)

    ### Test that the csrf_client head works
    def test_csrf_client_head(self):
        url="/ping/"+str(self.check.code)+"/"
        csrf = Client(enforce_csrf_checks=True)
        response = csrf.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")
        self.assertEqual(response.status_code, 200, msg=response)
