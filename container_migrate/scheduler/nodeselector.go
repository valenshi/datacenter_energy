package main

import (
    "fmt"
    "k8s.io/apimachinery/pkg/api/resource"
    "k8s.io/apimachinery/pkg/labels"
    schedulerapi "k8s.io/kubernetes/pkg/scheduler/api"
)

//定义 nodeSelector 结构体
type NodeSelector struct {}

// 实现 PerfectPredicate 接口
func (s *NodeSelector) SelectNodes(pods []*schedulerapi.Pod, nodeLister schedulerapi.NodeLister) ([]*schedulerapi.Node, error) {
    //查找符合 Pod NodeSelector 的 Node，返回 Node 数组
    nodes := make([]*schedulerapi.Node, 0)

    for _, pod := range pods {
        selector, err := labels.Parse(pod.Spec.NodeSelector)
        if err != nil {
            return nil, fmt.Errorf("failed to parse nodeSelector of Pod %s: %w", pod.Name, err)
        }

        nodeList, err := nodeLister.List()
        if err != nil {
            return nil, fmt.Errorf("unable to get current nodes: %w", err)
        }

        for _, node := range nodeList.Items {
            // 检查 Node 的标签和 Pod 的 NodeSelector 是否匹配
            labels := node.Labels
            if selector.Matches(labels) {
                nodes = append(nodes, &node)
            }
        }
    }

    if len(nodes) == 0 {
        return nil, fmt.Errorf("no node found for Pod")
    }

    return nodes, nil
}