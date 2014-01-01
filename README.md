# huebrew

A Phillips Hue to Spacebrew bridge.

It automatically enumerates all of the Hue lights attached to your bridge and sets up spacebrew publishers and subscribers for brightness for each bulb.

# Usage

```
huebrew.py [-h] [-s SERVER] [-p PORT] [-b BRIDGE]
```

## Options

 * `-s` or `--server`: Specify the Spacebrew server to connect to. Defaults to the sandbox server at sandbox.spacebrew.cc.

 * `-p` or `--port`: Specify the Spacebrew server port to connect to. Defaults to port 9000.

 * `-b` or `--bridge`: Specify the Hue bridge to connect to. Defaults to trying to auto-detect the bridge.
