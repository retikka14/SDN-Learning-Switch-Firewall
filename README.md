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

### Test 5: Packet Capture (Optional)
```bash
h1 tcpdump -i h1-eth0 -w capture.pcap &
h1 ping -c 3 h2
```

---

## 📊 Observations

- Controller installs flow rules dynamically
- MAC learning reduces flooding
- Firewall blocks specific ICMP traffic
- Flow table updates based on traffic
- Throughput measured using iperf
