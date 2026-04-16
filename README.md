# SDN Learning Switch Controller using POX & Mininet

## 📌 Project Overview
This project implements a Software Defined Networking (SDN) Learning Switch Controller using the POX controller and Mininet emulator. The controller dynamically learns MAC addresses and installs flow rules to enable efficient packet forwarding between hosts.

---

## 🎯 Objectives
- Implement MAC address learning logic  
- Dynamically install OpenFlow rules  
- Enable packet forwarding  
- Inspect and verify flow table entries  

---

## 🏗️ System Architecture
- Controller: POX (OpenFlow 1.0)  
- Emulator: Mininet  
- Switch: Open vSwitch (OVS)  
- Hosts: h1, h2  

---

## 🔌 Topology
```
h1 ---- s1 ---- h2
```

- 1 Switch (s1)  
- 2 Hosts (h1, h2)  

---

## ⚙️ Installation

### 1. Install Mininet
```bash
sudo apt update
sudo apt install mininet -y
```
### 2.1 Create File
```bash
cd ~/pox/pox/forwarding
nano my_switch.py
```
### 2.2 Clone POX
```bash
git clone https://github.com/noxrepo/pox.git
cd pox
```

---

## 🚀 Execution Steps

### Step 1: Clean environment
```bash
sudo mn -c
sudo killall pox.py
```

### Step 2: Run POX controller
```bash
cd ~/pox
./pox.py openflow.of_01 forwarding.my_switch
```

### Step 3: Run Mininet (new terminal)
```bash
sudo mn --controller=remote,ip=127.0.0.1,port=6633
```

---

## 🧠 Controller Logic
- Learns source MAC address and maps it to switch port  
- Floods packet if destination is unknown  
- Installs flow rules when destination is known  
- Reduces controller load after learning  

---

## 🧪 Testing

### Run:
```bash
pingall
```

### Expected Output:
```
*** Results: 0% dropped (2/2 received)
```

---

## 📊 Flow Table Inspection
```bash
sh ovs-ofctl dump-flows s1
```

### Observation:
- Flow rules are dynamically installed  
- Packets are forwarded without controller intervention after learning  

---

## 📈 Performance Evaluation
- Initial packets are flooded  
- Subsequent packets are directly forwarded  
- Reduced latency after rule installation  
- Efficient bandwidth utilization  

---

## ✅ Conclusion
The project successfully demonstrates an SDN-based learning switch using POX and Mininet. The controller dynamically learns MAC addresses and installs flow rules, improving network efficiency and reducing latency.

