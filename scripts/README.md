Create virtual environment and install dependencies:

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt
```

Collect data:

```
./rtt_print.py <output filename>
```

Analyze data:

```
./analyze.py <output filename>
```
