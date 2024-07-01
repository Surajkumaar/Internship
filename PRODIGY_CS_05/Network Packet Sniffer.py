import tkinter as tk
from tkinter import ttk
from scapy.all import sniff, IP, TCP, UDP, Raw
import threading
import binascii

class PacketSnifferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Packet Sniffer")
        self.root.configure(bg='black')

        self.start_button = tk.Button(root, text="Start Sniffing", command=self.start_sniffing, bg='green', fg='white')
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Sniffing", command=self.stop_sniffing, state=tk.DISABLED, bg='red', fg='white')
        self.stop_button.pack(pady=5)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black", font=('Arial', 10))
        style.configure("Treeview.Heading", background="black", foreground="white", font=('Arial', 10, 'bold'))

        self.tree = ttk.Treeview(root, columns=("Source IP", "Destination IP", "Protocol", "Payload"), show="headings", style="Treeview")
        self.tree.heading("Source IP", text="Source IP")
        self.tree.heading("Destination IP", text="Destination IP")
        self.tree.heading("Protocol", text="Protocol")
        self.tree.heading("Payload", text="Payload")
        self.tree.column("Source IP", width=150)
        self.tree.column("Destination IP", width=150)
        self.tree.column("Protocol", width=80)
        self.tree.column("Payload", width=400)
        self.tree.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        self.sniffing = False
        self.sniff_thread = None

    def start_sniffing(self):
        self.sniffing = True
        self.start_button.config(state=tk.DISABLED, bg='gray')
        self.stop_button.config(state=tk.NORMAL, bg='red')
        self.sniff_thread = threading.Thread(target=self.sniff_packets)
        self.sniff_thread.start()

    def stop_sniffing(self):
        self.sniffing = False
        self.start_button.config(state=tk.NORMAL, bg='green')
        self.stop_button.config(state=tk.DISABLED, bg='gray')

    def sniff_packets(self):
        sniff(prn=self.packet_callback, store=0, stop_filter=lambda x: not self.sniffing)

    def packet_callback(self, packet):
        if IP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            protocol = packet[IP].proto

            # Determine the protocol type
            if protocol == 6:  # TCP
                protocol_type = "TCP"
            elif protocol == 17:  # UDP
                protocol_type = "UDP"
            else:
                protocol_type = "Other"

            # Display payload data if present
            payload_data = ""
            if Raw in packet:
                payload_data = binascii.hexlify(packet[Raw].load).decode('utf-8')

            # Insert the packet information into the treeview
            self.tree.insert("", tk.END, values=(ip_src, ip_dst, protocol_type, payload_data))

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSnifferApp(root)
    root.mainloop()
