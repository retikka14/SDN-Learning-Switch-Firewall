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
Simple topology:

h1 ---- s1 ---- h2

- h1: 10.0.0.1  
- h2: 10.0.0.2  
- s1: Open vSwitch  

---

## ⚙️ Setup & Execution

### Step 1: Clean environment
```bash
sudo mn -c
sudo killall pox.py
