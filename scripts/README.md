## Setup

Create virtual environment and install dependencies:

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt
```

## Usage

First flash the central and client firmware onto two Nordic boards. Have the central connected to your computer, and the client powered by battery or USB.

To collect data run the following script. I suggest naming using a naming convention such as `PHY-DISTANCE-NUMBER.txt`. (For example, `1M-50M-1.txt` stands for 1M PHY at 50 meters, run number 1)

```
./rtt_print.py <output filename>
```

To analyze data, run the following script. It takes `rtt_print.py`'s output as input. It will calculate throughput, plot and save the plots to the same filename (with extension `.png`). If parsing failed, it's probably because you didn't collect enough data or the connection failed (lots of "connected" and "disconnected" messages and not a lot of useful results). However, there is still a good chance that it's buggy :)

```
./analyze.py <output filename>
```
