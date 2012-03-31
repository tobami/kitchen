from django.test import TestCase
from mock import patch

from kitchen.dashboard import chef


class TestData(TestCase):
    nodes = chef.load_extended_node_data()

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
        self.assertEqual(len(data), 5)
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

    def test_filter_nodes_all(self):
        """Should return all nodes when empty filters are are given"""
        data = chef.filter_nodes(self.nodes, '', '')
        self.assertEqual(len(data), 5)

    def test_filter_nodes_env(self):
        """Should filter nodes belonging to a given environment"""
        data = chef.filter_nodes(self.nodes, 'production')
        self.assertEqual(len(data), 3)

        data = chef.filter_nodes(self.nodes, 'staging')
        self.assertEqual(len(data), 2)

        data = chef.filter_nodes(self.nodes, 'non_existing_env')
        self.assertEqual(len(data), 0)

    def test_filter_nodes_roles(self):
        """Should filter nodes acording to their virt value"""
        data = chef.filter_nodes(self.nodes, roles='dbserver')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "testnode3.mydomain.com")

        data = chef.filter_nodes(self.nodes, roles='loadbalancer')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "testnode1")

        data = chef.filter_nodes(self.nodes, roles='webserver')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "testnode2")

        data = chef.filter_nodes(self.nodes, roles='webserver, dbserver')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[1]['name'], "testnode4")

    def test_filter_nodes_virt(self):
        """Should filter nodes acording to their virt value"""
        data = chef.filter_nodes(self.nodes, virt_roles='guest')
        self.assertEqual(len(data), 4)

        data = chef.filter_nodes(self.nodes, virt_roles='host')
        self.assertEqual(len(data), 1)

        data = chef.filter_nodes(self.nodes, virt_roles='host,guest')
        self.assertEqual(len(data), 5)

    def test_filter_nodes_bomined(self):
        """Should filter nodes acording to their virt value"""
        data = chef.filter_nodes(self.nodes,
            env='production', roles='loadbalancer,webserver', virt_roles='guest')
        self.assertEqual(len(data), 2)

        data = chef.filter_nodes(self.nodes,
            env='staging', roles='webserver', virt_roles='guest')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "testnode4")


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
        response = self.client.get("/graph/?env=")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("<title>Kitchen</title>" in response.content)
        self.assertTrue("Environment" in response.content)
        self.assertTrue("Please select an environment" in response.content)
