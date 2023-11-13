# Subnet Calculator

This program takes an IP V4 address and a number of reserved bits for subnets.

Then divides the available ip address into the available number of subnets using those params.

# Notes

## How to use

### Subnet Module

```bash
python3 Subnet.py 10.0.0.0 10
```

or if you want to export the result into a file for further reading.

```bash
python3 Subnet.py 10.0.0.0 10 -o dumps/Subnets.txt
```

### VLSM Module

Being every int value after the ip address, the size of each of the subnet required (they don't have to be sorted).

```bash
python3 VLSM.py 192.168.254.0 95 70 2 2
```

or if you want to export the result into a file for further reading.

```bash
python3 VLSM.py 192.168.254.0 95 70 2 2 -o dumps/VLSM.txt
```

## Environment

While I provide a requirements.txt file, we don't need to install any libraries in order for this program to work.

Using vanilla Python is ok.
