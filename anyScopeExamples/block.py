#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
from __future__ import print_function
from picosdk.discover import find_unit
from picosdk.device import ChannelConfig, TimebaseOptions
import matplotlib.pyplot as plt
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bits', type=float, default=8)
    args = parser.parse_args()

    if args.bits < 8:
        raise ValueError("you need to specify bits to be at least 8.")

    with find_unit() as device:

        print("found PicoScope: %s" % (device.info,))

        channel_configs = [ChannelConfig(name='A', enabled=True, coupling='DC', range_peak=5.)]
        actual_interval = 1.e-6
        oversample = int(round(4 ** (args.bits - 8)))

        print("using oversample of", oversample)

        min_total_capture_time = 2.e-3

        # using oversample, we can pump up the effective resolution of the scope (while reducing the total available
        # sample memory).
        timebase_options = TimebaseOptions(max_time_interval=actual_interval,
                                           no_of_samples=None,
                                           min_collection_time=min_total_capture_time,
                                           oversample=oversample)

        times, voltages, overflow_warnings = device.capture_block(timebase_options, channel_configs)

        for channel, data in voltages.items():
            label = "Channel %s" % channel
            if channel in overflow_warnings:
                label += " (over range)"
            plt.plot(times, data, label=label)

        plt.xlabel('Time / s')
        plt.ylabel('Amplitude / V')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    main()

