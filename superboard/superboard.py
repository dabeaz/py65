#!/usr/bin/env python -u
# 
# Ohio Scientific Superboard II simulator
# Author: David Beazley (http://www.dabeaz.com)
# Copyright (C) 2011
#
# This simulator requires the use of the 'basic.bin' and 'rom.bin'
# binary files in this directory.    Once starting the simulator,
# you need to follow the following steps.
#
#  1. Launch a telnet session to localhost 12000
#  2. Put telnet in character mode
#  3. Type 'C' and press return twice for "MEMORY SIZE" and "TERMINAL WIDTH"
#  4. Start typing BASIC programs.
#
# Example:
#
# bash %  telnet localhost 12000
# Trying 127.0.0.1...
# Connected to localhost.
# Escape character is '^]'.
# ^]
# telnet> mode c
# C 
# MEMORY SIZE? 
# TERMINAL WIDTH? 
#
# 31999 BYTES FREE
#
# OSI 6502 BASIC VERSION 1.0 REV 3.2
# COPYRIGHT 1977 BY MICROSOFT CO.
# 
# OK
# 10 FOR X = 1 TO 10
# 20 PRINT X;
# 30 NEXT X
# RUN
#  1  2  3  4  5  6  7  8  9  10 
# OK
#
#
# Note: This simulator is based on actual ROM images dumped from my
# own OSI Superboard II system.  See Superboard II related blog posts at
# http://www.dabeaz.com/blog.html

import py65.monitor
import sys
import select
from socket import *
import threading

def video_output(address,value):
    row = (address - 0xd000) // 32
    column = address % 32
    sys.stdout.write(('\x1b[<%d>;<%d>H' % (row,column)) + chr(value))
    sys.stdout.flush()

# Keyboard mapping table
keymap = {
    b'\x00' : {254:254, 253:255, 251:255, 247:255, 239:255, 223:255, 191:255, 127:255}, 
    b'\x03' : {254:190, 251:191 },
    b'\x0f' : {254:190, 223:223 },
    b'\r' : {254:254, 223:247}, 
    b'\n' : {254:254, 223:247}, 
    b' ' : {254:254, 253:239}, 
    b'/' : {254:254, 253:247}, 
    b';' : {254:254, 253:251}, 
    b':' : {254:254, 191:239}, 
    b'-' : {254:254, 191:247}, 
    b'.' : {254:254, 223:127}, 
    b',' : {254:254, 251:253}, 
    b'A' : {254:254, 253:191}, 
    b'B' : {254:254, 251:239}, 
    b'C' : {254:254, 251:191}, 
    b'D' : {254:254, 247:191}, 
    b'E' : {254:254, 239:191}, 
    b'F' : {254:254, 247:223}, 
    b'G' : {254:254, 247:239}, 
    b'H' : {254:254, 247:247}, 
    b'I' : {254:254, 239:253}, 
    b'J' : {254:254, 247:251}, 
    b'K' : {254:254, 247:253}, 
    b'L' : {254:254, 223:191}, 
    b'M' : {254:254, 251:251}, 
    b'N' : {254:254, 251:247}, 
    b'O' : {254:254, 223:223}, 
    b'P' : {254:254, 253:253}, 
    b'Q' : {254:254, 253:127}, 
    b'R' : {254:254, 239:223}, 
    b'S' : {254:254, 247:127}, 
    b'T' : {254:254, 239:239}, 
    b'U' : {254:254, 239:251}, 
    b'V' : {254:254, 251:223}, 
    b'W' : {254:254, 239:127}, 
    b'X' : {254:254, 251:127}, 
    b'Y' : {254:254, 237:247}, 
    b'Z' : {254:254, 253:223}, 
    b'1' : {254:254, 127:127}, 
    b'2' : {254:254, 127:191}, 
    b'3' : {254:254, 127:223}, 
    b'4' : {254:254, 127:239}, 
    b'5' : {254:254, 127:247}, 
    b'6' : {254:254, 127:251}, 
    b'7' : {254:254, 127:253}, 
    b'8' : {254:254, 191:127}, 
    b'9' : {254:254, 191:191}, 
    b'0' : {254:254, 191:223}, 
    b'!' : {254:252, 127:127}, 
    b'"' : {254:252, 127:191}, 
    b'#' : {254:252, 127:223}, 
    b'$' : {254:252, 127:239}, 
    b'%' : {254:252, 127:247}, 
    b'&' : {254:252, 127:251}, 
    b"'" : {254:252, 127:254}, 
    b'(' : {254:252, 191:127}, 
    b')' : {254:252, 191:191}, 
    b'*' : {254:252, 191:239}, 
    b'=' : {254:252, 191:247}, 
    b'>' : {254:252, 223:127}, 
    b'<' : {254:252, 251:253}, 
    b'?' : {254:252, 253:247}, 
    b'+' : {254:252, 253:251}, 
}


# Raw file underlying stdin
raw_stdin = sys.stdin.buffer.raw

# State about what's being polled
kb_row = 0
kb_current = keymap[b'\x00']
kb_count = 0

# Read the row values for the polled row
def keyboard_read(address):
    global kb_count, kb_current
    if kb_count > 0:
        kb_count -= 1
        if kb_count < 20:
            kb_current = keymap[b'\x00']
#    else:
#        kb_current = keymap[b'\x00']
#        if kb_row == 254:
#            # Poll stdin to see any input
#            r,w,e = select.select([raw_stdin],[],[],0)
#            if r:
#                keyboard_press(raw_stdin.read(1))

    return kb_current.get(kb_row,255)

# Set the current keyboard poll row
def keyboard_write(address, val):
    global kb_row
    kb_row = val

# Initiate a keypress
def keyboard_press(ch):
    global kb_count, kb_current
#    print("Pressed", hex(ord(ch)))
    if ch in keymap:
        kb_current = keymap[ch]
        kb_count = 60

# Simulated ACIA (bridges to a socket)
acia_socket = None
acia_inbuffer = bytearray()

# Simulated ACIA status byte
def acia_status(address):
    if not acia_socket:
        return 0
    return 0x2 | bool(acia_inbuffer)

def acia_read(address):
    r = acia_inbuffer[0]
    del acia_inbuffer[0]
    return r

def acia_write(address,val):
    acia_socket.send(bytes([val]))

def acia_reader_thread(port):
    global acia_socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("",port))
    sock.listen(1),
    print("Waiting for client on port", port)
    acia_socket, addr = sock.accept()
    print("Connection from", addr)
    while True:
        data = acia_socket.recv(8192)
        if b'\x03' in data:
            keyboard_press(b'\x03')
            data = data.replace(b'\x03',b'')
        acia_inbuffer.extend(data)

def map_hardware(m):
    # Video RAM at 0xd000-xd400
    #m.subscribe_to_write(range(0xd000,0xd400),video_output)

    # Monitor the polled keyboard port
    m.subscribe_to_read([0xdf00], keyboard_read)
    m.subscribe_to_write([0xdf00], keyboard_write)

    # Bad memory address to force end to memory check
    m.subscribe_to_read([0x8000], lambda x: 0)

    # Map ACIA device
    m.subscribe_to_read([0xf000], acia_status)
    m.subscribe_to_read([0xf001], acia_read)
    m.subscribe_to_write([0xf001], acia_write)
    
    # Force full-time ACIA on
    m.subscribe_to_read([0x203], lambda x: 128)
    m.subscribe_to_read([0x205], lambda x: 128)

def main(args=None):
    print("##### OSI Superboard II Simulator")
    print("##### Use 'telnet localhost 12000' to connect and start a session.")
    print("##### Put the telnet session in character mode and type 'C' to start.")
    thr = threading.Thread(target=acia_reader_thread,args=(12000,))
    thr.daemon = True
    thr.start()

    c = py65.monitor.Monitor()
    map_hardware(c._mpu.memory)
    try:
        import readline
    except ImportError:
        pass

    c.onecmd("load rom.bin f800")
    c.onecmd("load basic.bin a000")
    c.onecmd("goto ff00")

    try:
        c.onecmd('version')
        c.cmdloop()
    except KeyboardInterrupt:
        c._output('')

if __name__ == "__main__":
    main()
