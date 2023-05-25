import subprocess
import topologies
from mininet.net import Mininet
from mininet.node import Node, RemoteController
from mininet.cli import CLI


topo = topologies.eBPF_Topo()
net = Mininet(topo=topo,controller=RemoteController)	#define which topologie to implement
net.start()

p1 = subprocess.Popen(['python3', '/home/user/bcc/our_project/ebpf_drop_functions.py', 's1-eth1', 'pyramid_func','0','10000','2000'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p2 = subprocess.Popen(['python3', '/home/user/bcc/our_project/ebpf_drop_functions.py', 's2-eth2', 'step_func','0','50000','10'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

CLI(net)

net.stop()
