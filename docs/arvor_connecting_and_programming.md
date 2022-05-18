# NKE ARVOR Float: Connecting, Programming, and Troubleshooting via Bluetooth

Author: Christopher Gordon, DFO, (chris.gordon@dfo-mpo.gc.ca)[mailto:chris.gordon@dfo-mpo.gc.ca]

This document to guide a user on how to connect to an NKE ARVOR float,
hopefully simplifying the documentation in the float manual. A simple version
of the process is that you connect your laptop to the float via bluetooth,
just as you would headphones, a mouse, etc. Once connected, you will be able to
use a terminal emulator (I use (Tera Term)[https://ttssh2.osdn.jp/index.html.en])
to query or program the float.

## Steps

1. Open bluetooth settings, select "Add Bluetooth or other device", then select
"Bluetooth"

2. Move the magnet on the float from the "On/Off" position on the float (midway
up the body of the flaot) to the "Bluetooth" position (just under the white
"head" of the float)

[pic of each position]

3. Pair to the float. The name of the float will (annoyingly) not be any of the
other number associated with the float like serial number, IMEI, or WMO, but
something totally different. It is typically a mix of numbers and letters and
dashes, for example "C210216-0138-AC", so look for that general structure and
press "pair". If you picked the right thing, they usually pair quite quickly.

Note: if the float is already armed, you can still pair to it but you will have
a limited time window (roughly a minute) to get paired to it. Once you are
successfully paired the float will realize it is not being deployed and stop
the launching sequence.

4. Connect a terminal emulator.