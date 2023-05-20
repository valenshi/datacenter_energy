package plugins

import (
	"context"
	"fmt"

	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/klog"
	framework "k8s.io/kubernetes/pkg/scheduler/framework/v1alpha1"
)

// plugin name
const Name = "sample-plugin"

type Args struct {
	FavoriteColor  string `json:"favorite_color,omitempty"`
	FavoriteNumber int    `json:"favorite_number,omitempty"`
	ThanksTo       string `json:"thanks_to,omitempty"`
}

type Sample struct {
	args   *Args
	handle framework.FrameworkHandle
}

func (s *Sample) Name() string {
	return Name
}

var _ framework.ScorePlugin = &Sample{}

//type PluginFactory = func(configuration *runtime.Unknown, f FrameworkHandle) (Plugin, error)
func New(configuration *runtime.Unknown, f framework.FrameworkHandle) (framework.Plugin, error) {
	args := &Args{}
	if err := framework.DecodeInto(configuration, args); err != nil {
		return nil, err
	}
	klog.V(3).Infof("get plugin config args: %+v", args)
	return &Sample{
		args:   args,
		handle: f,
	}, nil
}

func (s *Sample) Score(ctx context.Context, state *framework.CycleState, p *v1.Pod, nodeName string) (int64, *framework.Status) {
	klog.V(3).Infof("enter Score()!!!")
	node, err := s.handle.SnapshotSharedLister().NodeInfos().Get(nodeName)
	if err != nil {
		// 节点没有准备好
		klog.Errorf("Node %q not found in cycle state: %v", nodeName, err)
		return 0, framework.NewStatus(framework.Error, fmt.Sprintf("Node not found in cycle state: %v", nodeName))
	}
	klog.V(3).Infof("node: %v", node)

	// 计算ECM指标的得分
	ecmScore := gethostPower(nodeName)
	klog.V(3).Infof(nodeName+" power is :%v", ecmScore)
	klog.V(3).Infof("exit Score()!!!")
	return ecmScore, framework.NewStatus(framework.Success, "")
}

// 计算资源占用率
// func calculateUtilizationPercentage(current, request, allocatable int64) int64 {
// 	value := int64(0)
// 	if allocatable > 0 {
// 		value = ((current + request) * 100) / allocatable
// 	}
// 	return value
// }

func gethostPower(name string) int64 {
	// var out bytes.Buffer
	// var stderr bytes.Buffer

	// cmd := exec.Command("python", "getpower.py", name)
	// cmd.Stdout = &out
	// cmd.Stderr = &stderr

	// err := cmd.Run()
	// if err != nil {
	// 	return -1
	// }
	// // fmt.Println("%q", out.String())
	// num, err := strconv.ParseInt(strings.TrimSpace(out.String()), 10, 64)
	// if err != nil {
	// 	fmt.Println(err)
	// 	return -1
	// }
	if name == "node1" {
		return 3
	} else if name == "node2" {
		return 2
	}
	return 1
}

func (s *Sample) ScoreExtensions() framework.ScoreExtensions {
	return nil
}

// func (cs *Sample) PreFilter(ctx context.Context, state *framework.CycleState, pod *v1.Pod) *framework.Status {
// 	klog.V(3).Infof("prefilter pod: %v", pod.Name)
// 	return framework.NewStatus(framework.Success, "")
// }

// func (s *Sample) PreFilterExtensions() framework.PreFilterExtensions {
// 	return nil
// }

// func (s *Sample) Filter(ctx context.Context, state *framework.CycleState, pod *v1.Pod, nodeInfo *nodeinfo.NodeInfo) *framework.Status {
// 	klog.V(3).Infof("filter pod: %v, node: %v", pod.Name, nodeInfo)
// 	return framework.NewStatus(framework.Success, "")
// }

// func (s *Sample) PreBind(ctx context.Context, state *framework.CycleState, p *v1.Pod, nodeName string) *framework.Status {
// 	// 从调度器的状态中获取节点的信息
// 	nodeInfo, error := s.handle.SnapshotSharedLister().NodeInfos().Get(nodeName)
// 	if error != nil {
// 		// 获取节点信息失败
// 		return framework.NewStatus(framework.Error, fmt.Sprintf("prebind get node info error: %+v", nodeName))
// 	} else {
// 		klog.V(3).Infof("prebind node info: %+v", nodeInfo.Node()) // 使用 klog 生成日志
// 		return framework.NewStatus(framework.Success, "")          // 成功绑定
// 	}
// }
