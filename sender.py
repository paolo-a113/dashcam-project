import os

fifo = open("./dataframes", "w")
fifo.write("Message from the sender!\n")
fifo.close()
