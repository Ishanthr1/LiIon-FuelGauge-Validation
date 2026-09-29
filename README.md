# Li-Ion Fuel Gauge Validation

This project reads measurements from a MAX17262H battery fuel gauge over I2C and saves them to a CSV file. It is intended for collecting data while testing a lithium-ion battery and fuel-gauge setup.

`fuelGauge.py` contains the register reads and conversions for voltage, current, capacity, state of charge, and fuel-gauge status. `main.py` samples those values at a regular interval and writes each sample with a UTC timestamp.

## Requirements

- A MAX17262H connected to an I2C bus
- A supported board with the CircuitPython Blinka libraries available
- Python packages listed in `requirements.txt`

The gauge address defaults to `0x36`.

## Setup

Install the dependencies in your Python environment:

```sh
python -m pip install -r requirements.txt
```

## Run

Start logging with the default settings (one sample every 10 seconds, written to `fg_log.csv`):

```sh
python main.py
```

Choose a different output file or sampling interval with `--output` and `--interval`:

```sh
python main.py --output test_run.csv --interval 2
```

The interval is in seconds. Press Ctrl+C to stop. The CSV file is opened in write mode, so an existing file at the selected path is replaced when logging starts.

## CSV fields

Each row contains:

| Field | Description |
| --- | --- |
| `timestamp` | Sample time in UTC, in ISO 8601 format |
| `voltage_mv` | Cell voltage in millivolts |
| `current_ma` | Current in milliamps |
| `average_current_ma` | Average current in milliamps |
| `remaining_capacity_mah` | Remaining capacity in milliamp-hours |
| `full_capacity_mah` | Reported full capacity in milliamp-hours |
| `state_of_charge` | Reported state of charge, scaled from the gauge register |
| `vfsoc` | Voltage-fuel-gauge state of charge, scaled from the gauge register |
| `vfstatus` | Raw fuel-gauge status register value |
