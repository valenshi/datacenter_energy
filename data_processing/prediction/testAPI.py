import unittest
from xmlrpc.client import ServerProxy
from my_tool import MySQLTool, get_host_ip

class TestAPI(unittest.TestCase):
    def setUp(self):
        # 在测试之前连接数据库，并向表中插入一些测试数据
        # self.db = MySQLTool(host='node1',username='ecm',password='123456',database='ecm')
        # self.db.execute("INSERT INTO nodedata (node_name, power) VALUES ('node1', 100)")
        # self.db.execute("INSERT INTO nodedata (node_name, power) VALUES ('node2', 200)")

        # 启动 XML-RPC 服务器
        self.server = ServerProxy(f"http://{get_host_ip()}:9926")

    def test_ping(self):
        response = self.server.ping()
        self.assertEqual(response, "200")

    def test_hostPower(self):
        response = self.server.hostPower("node1")
        print(response)
        # self.assertEqual(response, "100")

if __name__ == '__main__':
    unittest.main()