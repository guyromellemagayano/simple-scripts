"""
Finding the Median [v1.0]

To find the median number:
1. Put all the numbers in numerical order.
2. If there is an odd number of results, the median is the middle number.
3. If there is an even number of results, the median will be the mean of the two central numbers.
"""

def median(list_num):
    a = sorted(list_num)
    b = len(a) / 2
    
    if len(a) % 2 == 0: 
        return (a[b] + a[b-1]) / 2.0
    else:
        return a[b]