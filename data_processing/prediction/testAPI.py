import unittest
from my_tool import MySQLTool, get_host_ip
import xmlrpc.client

class TestAPI(unittest.TestCase):
   def testhostPower(self):
    ip = "192.168.1.201"
    hostname = "node1"
    try:
        print('collectHost', ip, hostname)
        server_url = "http://" + ip + ":9926/"
        proxy = xmlrpc.client.ServerProxy(server_url)
        result = proxy.hostPower(hostname)
        print(result)
    except Exception as e:
        print(e)
        return

if __name__ == '__main__':
    unittest.main()