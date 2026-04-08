from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# MAC learning table
mac_to_port = {}

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet.parsed:
        return

    dpid = event.connection.dpid

    # Initialize switch table
    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    # Learn source MAC
    mac_to_port[dpid][packet.src] = event.port

    # -------- ALLOW ARP --------
    if packet.type == 0x0806:
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        return

    # -------- FIREWALL RULE --------
    ip = packet.find('ipv4')
    if ip and packet.find('icmp'):
        icmp = packet.find('icmp')

        # Block ICMP from h1 -> h2 only
        if str(ip.srcip) == "10.0.0.1" and str(ip.dstip) == "10.0.0.2":
            if icmp.type == 8:  # echo request
                log.info("BLOCKED ICMP: %s -> %s", ip.srcip, ip.dstip)

                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet)
                msg.idle_timeout = 10
                event.connection.send(msg)
                return

    # -------- LEARNING SWITCH --------
    if packet.dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][packet.dst]

        log.info("Forward %s -> %s via port %s",
                 packet.src, packet.dst, out_port)

        # Install flow rule
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 60
        msg.actions.append(of.ofp_action_output(port=out_port))

        # Send current packet
        msg.data = event.ofp
        event.connection.send(msg)

    else:
        # Flood unknown destination
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)


def launch():
    log.info("Custom SDN Learning Switch + Firewall Started")
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
