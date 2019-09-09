import os
import sys

fifo = open("./dataframes", "r")
for line in fifo:
	print "Received: " + line
fifo.close()
