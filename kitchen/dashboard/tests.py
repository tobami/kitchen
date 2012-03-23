from django.test import TestCase


class TestViews(TestCase):
    def test_main(self):
        """Should display the main page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("<title>Kitchen</title>" in response.content)
        self.assertTrue("Environment" in response.content)
        self.assertTrue("Roles" in response.content)

    def test_graph_no_env(self):
        """Should not generate a graph when no environment is selected"""
        response = self.client.get("/graph/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("<title>Kitchen</title>" in response.content)
        self.assertTrue("Environment" in response.content)
        self.assertTrue("Please select an environment" in response.content)
