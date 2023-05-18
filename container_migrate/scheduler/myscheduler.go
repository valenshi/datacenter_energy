package main

import (
	"fmt"

	"k8s.io/apimachinery/pkg/labels"
	schedulerapi "k8s.io/kubernetes/pkg/scheduler/framework/v1alpha1"
)

// 定义 MyScheduler 结构体
type MyScheduler struct {
	// 插件的配置
	pluginArgs schedulerapi.PluginArgs
}

// 实现 scheduler.Interface 接口中的 Methods：
// 1. 绑定 Pod 到 Node 上
// 2. 取得初始化的状态信息
// 3. 发生新的调度事件，更新调度状态
func (s *MyScheduler) Schedule(pod *schedulerapi.Pod, nodeLister schedulerapi.NodeLister) (selectedNode *schedulerapi.Node, boundPod *schedulerapi.BoundPod, err error) {
	status := schedulerapi.SchedulerStatus{}
	status.ExtenderStates = make([]schedulerapi.ExtenderState, 1)
	status.ExtenderStates[0].ObjectName = pod.Name
	return nil, nil, &schedulerapi.NoSuitableNodeError{Status: status}
}

func (s *MyScheduler) QueueSort(queue schedulerapi.PodQueue) bool {
	return true
}

func (s *MyScheduler) Sync() error {
	return nil
}

// 实现 scheduler.FitPredicate 接口中的 Methods：
// 返回该节点是否能够满足 Pod 的资源需求
func (s *MyScheduler) Fit(pod *schedulerapi.Pod, node *schedulerapi.Node) (bool, error) {
	for _, container := range pod.Spec.Containers {
		// 将 Pod 需要的资源进行计算
		cpuRequest := container.Resources.Requests.Cpu().MilliValue()
		cpuLimit := container.Resources.Limits.Cpu().MilliValue()

		// 判断节点的资源是否满足 Pod 的需求
		if cpuRequest > node.Status.Allocatable.Cpu().MilliValue() || cpuLimit > node.Status.Allocatable.Cpu().MilliValue() {
			return false, nil
		}
	}
	return true, nil
}

// 实现 scheduler.PerfectPredicate 接口中的 Methods：
// 为 Pod 选定合适的 Node，并绑定到该节点
func (s *MyScheduler) Select(m schedulerapi.NodeLister, pod *schedulerapi.Pod, nodes []*schedulerapi.Node) (selected *schedulerapi.Node, err error) {
	for _, node := range nodes {
		if ok, _ := s.Fit(pod, node); ok {
			return node, nil
		}
	}
	return nil, fmt.Errorf("Failed to allocate pod due to insufficient memory or CPU resources")
}

// 定义 scorecalculator 结构体
type scorecalculator struct {
}

// 实现 Fit 接口中的 Score() 方法
func (sc *scorecalculator) Score(pod *schedulerapi.Pod, nodeName string) (int64, *schedulerapi.Status) {
	score := int64(0)

	// 在此处添加评分逻辑，评估当前节点是否适合放置 Pod

	return score, nil
}

// 定义 nodeselector 结构体
type nodeselector struct {
}

// 实现 PerfectPredicate 接口中的 Select() 方法
func (ns *nodeselector) SelectNodes(pods []*schedulerapi.Pod, nodeLister schedulerapi.NodeLister) ([]*schedulerapi.Node, error) {
	var nodes []*schedulerapi.Node
	for _, pod := range pods {
		selector, err := labels.Parse(pod.Spec.NodeSelector)
		if err != nil {
			continue
		}
		nodeList, err := nodeLister.List()
		if err != nil {
			return nil, err
		}
		for _, node := range nodeList.Items {
			labels := node.Labels
			if selector.Matches(labels) {
				nodes = append(nodes, &node)
			}
		}
	}
	return nodes, nil
}

// 实现 schedulerapi.Extender 接口
func (e *myExtender) Filter(pods *schedulerapi.PodList, nodes *schedulerapi.NodeList, nodeNames *schedulerapi.NodeNames) (*schedulerapi.ExtenderFilterResult, error) {
	result := schedulerapi.ExtenderFilterResult{}
	result.FailedNodes = map[string]string{}

	// 在这里添加过滤 Node 的逻辑

	result.FilteredNodes = make(map[string]string)
	for _, pod := range pods.Items {
		filterNodes, err := e.NodeSelector.SelectNodes([]*schedulerapi.Pod{&pod}, schedulerapi.NodeLister(nodes))
		if err != nil {
			return nil, err
		}
		if len(filterNodes) == 0 {
			result.FailedNodes[pod.Name] = ""
		} else {
			statuses := make([]schedulerapi.ExtenderFilterResultStatus, 0, len(filterNodes))
			for _, node := range filterNodes {
				// 计算一个 Node 的 Score 并将其加入到 statuses 列表中
				score, _ := e.ScoreCalculator.Score(&pod, node.Name)
				statuses = append(statuses, schedulerapi.ExtenderFilterResultStatus{
					Name:   node.Name,
					Score:  score,
					Msg:    "",
					Reason: "",
				})
			}
			result.FilteredNodes[pod.Name] = "Pass"
			result.NodeScores = append(result.NodeScores, schedulerapi.ExtenderScore{
				Name:   pod.Name,
				Scores: statuses,
			})
		}
	}

	return &result, nil
}

func (e *myExtender) Prioritize(pods *schedulerapi.HostPriorityList, nodes *schedulerapi.NodeList) (*schedulerapi.HostPriorityList, error) {
	return pods, nil
}

// 定义 main() 函数
func main() {
	// 创建 MyScheduler 和 Extender 实例
	ms := &MyScheduler{}
	me := &myExtender{}

	// 运行调度器
	schedulerapi.Run(ms, me, "0.0.0.0:10251")
}

// 定义 myExtender 结构体
type myExtender struct {
	ScoreCalculator *scorecalculator
	NodeSelector    *nodeselector
}
