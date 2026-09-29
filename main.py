import csv
import os
import sys
import argparse
import signal
import time
from datetime import datetime, timezone

import board
import busio

from fuelGauge import MAX17262H

cvsheader = ['timestamp', 'voltage_mv', 'current_ma', 'average_current_ma', 'remaining_capacity_mah', 'full_capacity_mah', 'state_of_charge', 'vfsoc', 'vfstatus']


def smaple(fg):
    now = datetime.now(timezone.utc)
    return [now.isoformat(timespec='seconds'), fg.voltage_mv(), fg.current_ma(), fg.average_current_ma(), fg.remaining_capacity_mah(), fg.full_capacity_mah(), fg.state_of_charge(), fg.vfsoc(), fg.vfstatus()]

_running = True
def _stop(signum, frame):
    global _running
    _running = False

def main():
    parser = argparse.ArgumentParser(description='MAX17262H Fuel Gauge Logger')
    parser.add_argument('--output', '-o', type=str, default='fg_log.csv', help='Output CSV file name')
    parser.add_argument('--interval', '-i', type=float, default=10.0, help='Sampling interval in seconds')
    args = parser.parse_args()


    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)


    # Initialize I2C bus and fuel gauge
    i2c = busio.I2C(board.SCL, board.SDA)
    fg = MAX17262H(i2c)

    # Open CSV file for writing
    with open(args.output, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(cvsheader)  # Write header

        print(f"Logging data to {args.output} every {args.interval} seconds. Press Ctrl+C to stop.")
        
        try:
            next_t = time.monotonic()
            while _running:
                data = smaple(fg)
                writer.writerow(data)
                csvfile.flush()  # Ensure data is written to disk
                os.fsync(csvfile.fileno())  # Force write to disk

                next_t = next_t + args.interval
                remaining = next_t - time.monotonic()
                if remaining < 0:
                    next_t = time.monotonic()
                    continue
                end  = time.monotonic() + remaining  # Get the end time of the sampling interval
                while _running and time.monotonic() < end:
                    time.sleep(min(0.25, end - time.monotonic()))  # Sleep in small increments to be responsive to signals
        except KeyboardInterrupt:
            print("\nLogging stopped by user.")

    print("Logging stopped.")


if __name__ == "__main__":
    main()