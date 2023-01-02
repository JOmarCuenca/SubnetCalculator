# Subnet Calculator

This program takes an IP V4 address and a number of reserved bits for subnets.

Then divides the available ip address into the available number of subnets using those params.

# Notes

## How to use

```bash 
python3 Subnet.py 10.0.0.0 10
```

or if you want to export the result into a file for further reading.

```bash 
python3 Subnet.py 10.0.0.0 10 -o dumps/Subnets.txt
```

## Environment

While I provide a requirements.txt file, we don't need to install any libraries in order for this program to work.

Using vanilla Python is ok.