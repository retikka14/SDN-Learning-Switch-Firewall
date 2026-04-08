# SDN Learning Switch with Firewall (POX + Mininet)

## 📌 Problem Statement
This project implements a Software Defined Networking (SDN) solution using Mininet and POX controller.  
It demonstrates:
- Learning switch behavior
- Flow rule installation (match-action)
- Firewall rule (blocking ICMP traffic selectively)

---

## 🧠 Objective
- Understand controller–switch interaction  
- Implement packet_in handling  
- Design flow rules using OpenFlow  
- Observe network behavior  

---

## 🏗️ Topology

h1 ---- s1 ---- h2

- h1: 10.0.0.1  
- h2: 10.0.0.2  
- s1: Open vSwitch  

---

## ⚙️ Setup & Execution

### Step 1: Clean Environment
```bash
sudo mn -c
sudo killall pox.py
```

### Step 2: Run POX Controller
```bash
cd ~/pox
./pox.py forwarding.my_switch
```

### Step 3: Run Mininet
```bash
sudo mn --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow10
```

---

## 🧪 Testing

### 1. Check Connectivity
```bash
pingall
```

### 2. Firewall Behavior
```bash
h1 ping -c 2 h2   # BLOCKED ❌
h2 ping -c 2 h1   # ALLOWED ✅
```

### 3. Latency Test
```bash
h2 ping -c 5 h1
```

### 4. Throughput Test
```bash
iperf h2 h1
```

### 5. Flow Table Inspection
```bash
sh ovs-ofctl dump-flows s1
```

---

## 🔥 Functionality

### ✔ Learning Switch
- Learns MAC → port mapping  
- Installs flow rules dynamically  
- Reduces controller load after learning  

### ✔ Firewall Rule
- Blocks ICMP traffic from:
  10.0.0.1 → 10.0.0.2  

- Allows reverse traffic:
  10.0.0.2 → 10.0.0.1  

---

## 📊 Observations

- Latency: Low (milliseconds range)  
- Throughput: High (Gbps range in Mininet)  
- Flow rules dynamically installed  
- Firewall successfully blocks one direction only  

---

## 📸 Proof of Execution

Include screenshots of:
- pingall results  
- h1 blocked and h2 allowed  
- Controller logs showing BLOCKED IP  
- Flow table output  
- iperf results  

---
