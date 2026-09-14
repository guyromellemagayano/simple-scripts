#!/usr/bin/env python3
fahrenheit = 0.0
print("Fahrenheight | Celsius")
while fahrenheit <= 250:
	celsius = (fahrenheit - 32.0) / 1.8
	print(f"{fahrenheit:5.1f}  | {celsius:7.2f}")
	fahrenheit = fahrenheit + 25
