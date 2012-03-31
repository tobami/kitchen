from django.test import TestCase
from mock import patch

from kitchen.dashboard import chef


class TestData(TestCase):

    def test_good_repo(self):
        """Should return true when a valid repository is found"""
        self.assertTrue(chef._check_kitchen())

    @patch('kitchen.dashboard.chef.KITCHEN_DIR', '/badrepopath/')
    def test_bad_repo(self):
        """Should raise RepoError when kitchen is not found"""
        self.assertRaises(chef.RepoError, chef._check_kitchen)

    def test_load_data_nodes(self):
        """Should return nodes when the given argument is 'nodes'"""
        data = chef._load_data('nodes')
        self.assertTrue(len(data), 3)
        self.assertEqual(data[1]['name'], "testnode2")

    def test_load_data_roles(self):
        """Should return roles when the given argument is 'roles'"""
        data = chef._load_data('roles')
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['name'], "dbserver")

    def test_load_data_unsupported(self):
        """Should return an empty dict when an invalid arg is given"""
        data = chef._load_data('rolezzzz')
        self.assertEqual(len(data), 0)


class TestViews(TestCase):

    def test_list(self):
        """Should display the node list page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("<title>Kitchen</title>" in response.content)
        self.assertTrue("Environment" in response.content)
        self.assertTrue("Roles" in response.content)

    @patch('kitchen.dashboard.chef.KITCHEN_DIR', '/badrepopath/')
    def test_list_no_repo(self):
        """Should display a RepoError message when repo dir doesn't exist"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("<title>Kitchen</title>" in response.content)
        expected = "Repo dir doesn&#39;t exist at &#39;/badrepopath/&#39;"
        self.assertTrue(expected in response.content)

    def test_graph_no_env(self):
        """Should not generate a graph when no environment is selected"""
        response = self.client.get("/graph/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("<title>Kitchen</title>" in response.content)
        self.assertTrue("Environment" in response.content)
        self.assertTrue("Please select an environment" in response.content)
