from django.test import TestCase


class TestViews(TestCase):
    def test_main(self):
        """Should display the main page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("<title>Kitchen</title>" in response.content)
        self.assertTrue("Environments" in response.content)
        self.assertTrue("Roles" in response.content)
