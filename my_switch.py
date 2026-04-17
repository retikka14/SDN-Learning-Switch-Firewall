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

    # ✅ FIXED FIREWALL
    if ip and icmp:
        if str(ip.srcip) == "10.0.0.1" and str(ip.dstip) == "10.0.0.2":
            if icmp.type == 8:  # ONLY request
                log.info("BLOCKED ICMP REQUEST: %s -> %s", ip.srcip, ip.dstip)

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
