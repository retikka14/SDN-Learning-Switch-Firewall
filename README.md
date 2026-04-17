# SDN Mininet-Based Simulation Project – Learning Switch + Firewall

## 📌 Problem Statement
This project implements an SDN-based network using Mininet and POX controller to demonstrate:
- Controller–switch interaction
- Flow rule design (match–action)
- Network behavior observation

We implement:
- Learning Switch (MAC learning + forwarding)
- Firewall (block ICMP from h1 → h2)

---

## 🛠️ Requirements
- Ubuntu (or VM)
- Mininet
- POX Controller
- Open vSwitch

---

## ⚙️ Setup & Execution Steps

### 1. Clean Environment
```bash
sudo mn -c
sudo killall pox.py
```

---

### 2. Go to POX Directory
```bash
cd ~/pox
```

---

### 3. Create Controller Code
```bash
nano forwarding/my_switch.py
```

👉 Paste the code below:

```python
from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()
mac_to_port = {}

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet.parsed:
        return

    dpid = event.connection.dpid

    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    # Learn MAC
    mac_to_port[dpid][packet.src] = event.port

    # Allow ARP
    if packet.type == 0x0806:
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        return

    ip = packet.find('ipv4')
    icmp = packet.find('icmp')

    # Firewall: Block ICMP from h1 -> h2
    if ip and icmp:
        if str(ip.srcip) == "10.0.0.1" and str(ip.dstip) == "10.0.0.2":
            log.info("BLOCKED ICMP: %s -> %s", ip.srcip, ip.dstip)
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.idle_timeout = 10
            msg.priority = 100
            event.connection.send(msg)
            return

    # Learning switch
    if packet.dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][packet.dst]

        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.idle_timeout = 30
        msg.priority = 10
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.data = event.ofp
        event.connection.send(msg)
    else:
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)

def launch():
    log.info("Learning Switch + Firewall Started")
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
```

Save:
```
CTRL + X → Y → ENTER
```

---

### 4. Run Controller (Terminal 1)
```bash
./pox.py openflow.of_01 forwarding.my_switch
```

---

### 5. Run Mininet (Terminal 2)
```bash
sudo mn --controller=remote,ip=127.0.0.1,port=6633
```

---

## 🧪 Testing & Validation

### Test 1: Connectivity
```bash
pingall
```

Expected Output:
```
h1 -> X
h2 -> h1
*** Results: 50% dropped
```

---

### Test 2: Manual Ping
```bash
h1 ping -c 2 h2
h2 ping -c 2 h1
```

Result:
- h1 → h2 ❌ blocked
- h2 → h1 ✅ allowed

---

### Test 3: Flow Table
```bash
sh ovs-ofctl dump-flows s1
```

---

### Test 4: Throughput
```bash
iperf h1 h2
```

---

## 📊 Observations

- Controller installs flow rules dynamically
- MAC learning reduces flooding
- Firewall blocks specific ICMP traffic
- Flow table updates based on traffic
- Throughput measured using iperf

---


