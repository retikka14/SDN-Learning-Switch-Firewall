## 🚀 Execution Steps (Clean + Complete)

### 1. Clean Previous Mininet & Controller
```bash
sudo mn -c
sudo killall pox.py
sudo lsof -i :6633
```

If any PID is shown:
```bash
sudo kill -9 <PID>
```

---

### 2. Navigate to POX Directory
```bash
cd ~/pox
```

---

### 3. Edit/Create Controller Code
```bash
cd ~/pox/pox/forwarding
nano my_switch.py
```

Paste your final controller code and save:
```
CTRL + X → Y → ENTER
```

---

### 4. Start POX Controller
```bash
cd ~/pox
./pox.py openflow.of_01 forwarding.my_switch
```

Expected output:
```
Learning Switch + Firewall Started
[00-00-00-00-00-01] connected
```

---

### 5. Start Mininet Topology (New Terminal)
```bash
sudo mn --controller=remote,ip=127.0.0.1,port=6633
```

---

## 🧪 Testing Commands

### 6. Verify Topology
```bash
nodes
net
```

---

### 7. Check Host IP Configuration
```bash
h1 ifconfig
h2 ifconfig
```

---

### 8. Test Connectivity (Ping)

#### Blocked Case:
```bash
h1 ping -c 3 h2
```
Expected: ❌ 100% packet loss (Blocked)

#### Allowed Case:
```bash
h2 ping -c 3 h1
```
Expected: ✅ Successful ping

---

### 9. Test Latency
```bash
h2 ping -c 5 h1
```

---

### 10. Test Throughput (iperf)
```bash
iperf h1 h2
```

Expected:
```
High bandwidth (e.g., Gbits/sec)
```

---

### 11. View Flow Table
```bash
sh ovs-ofctl dump-flows s1
```

Filter packet counts:
```bash
sh ovs-ofctl dump-flows s1 | grep n_packets
```

---


---

## ✅ Expected Results Summary

| Test Case | Result |
|----------|--------|
| h1 → h2 ping | ❌ Blocked |
| h2 → h1 ping | ✅ Allowed |
| iperf | ✅ Works |
| Flow table | ✅ Rules installed |
| tcpdump | ✅ Packets captured |

---

## 🧹 Cleanup After Execution
```bash
exit
sudo mn -c
sudo killall pox.py
```
