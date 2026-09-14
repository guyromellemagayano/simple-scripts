#!/usr/bin/env python3
i = 1
print("-" * 50)
while i < 11:
	n = 1
	while n <= 10:
		print(f"{i * n:d}", end=' ')
		n += 1
	print()
	i += 1
print("-" * 50)
