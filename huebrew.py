#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import urllib
import sys

from time import sleep
import phue
from phue import Bridge
from pySpacebrew.spacebrew import Spacebrew


class HueBulb(object):
    def __init__(self, brew, name, light):
        self._brew = brew
        self._name = name
        self._light = light
        self._old_brightness = -1
        brew.addPublisher(name + " Brightness", "range")
        brew.addSubscriber(name + " Brightness", "range")
        brew.subscribe(name + " Brightness", self.brightness)

    def poll(self):
        """ Poll the HUE API for the current state of this bulb
        """
        b = self._light.brightness
        if b != self._old_brightness:
            print("%s brightness changed to %d"%(self._name, b))
            self._publish("Brightness", b * 4)
            self._old_brightness = b

    def brightness(self, value):
        b = int(value)/4 # scale 0-1023 to 0-255
        print("Set brightness of %s to %d"%(self._name, b))
        self._light.brightness = b
        self._publish("Brightness", b * 4)

    def _publish(self, name, value):
        self._brew.publish("%s %s"%(self._name, name), value)


def main():
    parser = argparse.ArgumentParser(description="Hue to Spacebrew bridge")
    parser.add_argument("-s", "--server", help="Spacebrew server",
            default="sandbox.spacebrew.cc")
    parser.add_argument("-p", "--port", help="Spacebrew port",
            type=int, default=9000)
    parser.add_argument("-b", "--bridge", help="Hue bridge")

    args = parser.parse_args()

    print("Connecting to Spacebrew server: %s port %d"%(args.server, args.port))

    brew = Spacebrew("Hue Bridge", server=args.server, port=args.port)

    if args.bridge is None:
        info = urllib.urlopen('http://www.meethue.com/api/nupnp').read()
        info = json.loads(info)
        if len(info) > 0:
            args.bridge = info[0][u'internalipaddress']
        else:
            print("ERROR: Could not auto-detect Hue bridge IP")
            print(" Please specify --bridge manually")
            sys.exit(1)

    print("Connecting to Hue bridge at: %s" % args.bridge)

    bridge = None
    while bridge == None:
        try:
            bridge = Bridge(args.bridge)
        except phue.PhueRegistrationException as e:
            print(str(e))
            sleep(5)


    lights = bridge.get_light_objects('name')

    brew_lights = []

    print("Lights:")
    for name in lights:
        print(" - %s"%(name))
        brew_lights.append(HueBulb(brew, name, lights[name]))

    print("Starting Spacebrew")
    brew.start()
    sleep(5)

    try:
        while True:
            for light in brew_lights:
                light.poll()
            # chill out man
            sleep(1)
    finally:
        brew.stop()


if __name__ == '__main__':
    main()
