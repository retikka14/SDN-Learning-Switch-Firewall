from pox.core import core  # Import POX core system (event loop, logging, modules)
import pox.openflow.libopenflow_01 as of  # Import OpenFlow 1.0 protocol helpers

log = core.getLogger()  # Create logger for debugging/info output
mac_to_port = {}  # Dictionary: {switch_dpid: {mac_address: port_number}}

def _handle_PacketIn(event):  # Function triggered whenever a packet arrives at the controller
    packet = event.parsed  # Parsed packet object
    if not packet.parsed:  # If packet parsing failed
        return  # Ignore and exit

    dpid = event.connection.dpid  # Datapath ID of the switch that sent the packet

    if dpid not in mac_to_port:  # If this switch is not yet in MAC table
        mac_to_port[dpid] = {}  # Create a new MAC table for this switch

    # Learn MAC address location
    mac_to_port[dpid][packet.src] = event.port  # Map source MAC to incoming port

    # Allow ARP packets to be flooded (needed for network discovery)
    if packet.type == 0x0806:  # Ethernet type 0x0806 = ARP
        msg = of.ofp_packet_out()  # Create packet-out message
        msg.data = event.ofp  # Attach original packet data
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  # Flood to all ports
        event.connection.send(msg)  # Send message to switch
        return  # Stop further processing

    ip = packet.find('ipv4')  # Try to extract IPv4 layer
    icmp = packet.find('icmp')  # Try to extract ICMP layer

    # FIXED FIREWALL RULE SECTION
    if ip and icmp:  # Only proceed if packet has both IP and ICMP
        if str(ip.srcip) == "10.0.0.1" and str(ip.dstip) == "10.0.0.2":  # Specific blocked flow
            if icmp.type == 8:  # ICMP type 8 = Echo Request (ping request)
                log.info("BLOCKED ICMP REQUEST: %s -> %s", ip.srcip, ip.dstip)  # Log blocking event

                msg = of.ofp_flow_mod()  # Create flow rule to install in switch
                msg.match = of.ofp_match.from_packet(packet, event.port)  # Match this traffic pattern
                msg.idle_timeout = 10  # Remove rule after 10 seconds of inactivity
                msg.priority = 100  # High priority rule (firewall override)

                event.connection.send(msg)  # Send flow rule to switch
                return  # Stop processing this packet

    # Learning switch logic (MAC learning + forwarding)
    if packet.dst in mac_to_port[dpid]:  # If destination MAC is known
        out_port = mac_to_port[dpid][packet.dst]  # Get output port for destination MAC

        msg = of.ofp_flow_mod()  # Create flow rule
        msg.match = of.ofp_match.from_packet(packet, event.port)  # Match incoming traffic
        msg.idle_timeout = 30  # Remove flow if idle for 30 seconds
        msg.priority = 10  # Normal priority (lower than firewall)
        msg.actions.append(of.ofp_action_output(port=out_port))  # Forward to correct port
        msg.data = event.ofp  # Include original packet

        event.connection.send(msg)  # Install rule on switch

    else:  # If destination MAC is unknown
        msg = of.ofp_packet_out()  # Create packet-out message
        msg.data = event.ofp  # Attach original packet
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  # Flood to discover destination
        event.connection.send(msg)  # Send packet-out to switch


def launch():  # Entry point when POX module starts
    log.info("Learning Switch + Firewall Started")  # Log startup message
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)  # Register PacketIn handler
