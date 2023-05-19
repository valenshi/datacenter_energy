import my_tool
from jsonrpc import Server, jsonrpc_method

import argparse

class API:
    """
    API类实现了远程过程调用所需的方法
    """

    @jsonrpc_method(name='ping')
    def ping(self):
        """
        ping方法返回200字符串，用于测试RPC服务是否正在运行
        """
        return "200"

    @jsonrpc_method(name='hostPower')
    def hostPower(self, nodeName:str):
        """
        host_power方法接受一个节点名称并返回该节点的功率值。
        """
        db = my_tool.MySQLTool(host='node1', username='ecm', password='123456', database='ecm')
        result = db.select(table_name="nodedata", columns=["power"], where="node_name = '"+nodeName+"'", order_by="timestamp DESC", limit=1)
        return result[0]['power']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9926, help='port number for JSONRPC')
    args = parser.parse_args()

    #创建JSONRPC Server对象
    server = Server()
    server.register_instance(API())

    #启动JSONRPC服务
    server.serve('0.0.0.0', args.port)