#!/usr/bin/env python3
import subprocess
import sys
import telnetlib
import time


if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <out filename>")
    sys.exit(1)

output_file = sys.argv[1]
print(f"Writing output to stdout and {output_file}")

PORT = 42477

# Open JLinkExe connection
jlink_cmd = "JLinkExe -device nrf52840_xxaa -if swd -speed 4000 -RTTTelnetPort {} -AutoConnect 1".format(
    PORT
)
proc = subprocess.Popen(
    jlink_cmd.split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

# Wait until it is ready
input("hit enter after selecting the device in JLink. If you have just one device connected, press enter right away.")

try:
    # Open Telnet to RTT port and start printing data
    telnet = telnetlib.Telnet(host="localhost", port=PORT, timeout=1)

    with open(output_file, "w") as fd:
        while True:
            rx_data = telnet.read_very_eager()
            if rx_data:
                tmp = "\t".join([str(time.time()), rx_data.strip().decode()])
                print(tmp)
                fd.write(tmp + "\n")

except KeyboardInterrupt:
    print("bye bye")
except Exception as e:
    print(e)
finally:
    proc.kill()
