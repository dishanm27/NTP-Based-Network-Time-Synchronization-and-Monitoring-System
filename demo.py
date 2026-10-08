import socket
import struct
import datetime
import time

print("=" * 40)
print("     NTP TIME SYNCHRONIZATION SYSTEM")
print("=" * 40)

# NTP server
NTP_SERVER = "pool.ntp.org"

# Create UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5)

# NTP packet
packet = b'\x1b' + 47 * b'\0'

try:
    # Record request time
    start_time = time.time()

    # Send request to NTP server
    client.sendto(packet, (NTP_SERVER, 123))

    # Receive response
    data, address = client.recvfrom(1024)

    # Record response time
    end_time = time.time()

    # Calculate network delay
    network_delay = (end_time - start_time) * 1000

    # Extract time from NTP response
    ntp_time = struct.unpack("!12I", data[:48])[10]

    # Convert NTP time to Unix time
    ntp_time -= 2208988800

    # Convert to readable date and time
    server_time = datetime.datetime.fromtimestamp(ntp_time)

    print("NTP Server      :", address[0])
    print("Server Time     :", server_time.strftime("%Y-%m-%d %H:%M:%S"))
    print("Network Delay   :", round(network_delay, 2), "ms")
    print("Status          : Time synchronized")

except Exception as e:
    print("Error:", e)

finally:
    client.close()

print("=" * 40)