package main

import (
	"fmt"
	"net/rpc"
)

type Args struct {
	NodeName string
}

func main() {
	client, err := rpc.Dial("tcp", "192.168.1.201:9926")
	if err != nil {
		fmt.Println("连接RPC服务器失败：", err)
	}

	var res float64
	err = client.Call("API.hostPower", Args{"node1"}, &res)
	if err != nil {
		fmt.Println("调用hostPower函数失败：", err)
	}
	fmt.Printf("节点1的功率值为: %v\n", res)
}
