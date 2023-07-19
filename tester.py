from watches import *
import dolphin_memory_engine as dme
import time

# Connect to Dolphin
dme.hook()

# Wait if Dolphin isn't hooked
if not dme.is_hooked():
    print(f'{"[" + "Console" + "]":>15}Not Hooked, waiting for connection to Dolphin')
    while not dme.is_hooked():
        time.sleep(0.01)
        dme.hook()
    print(f'{"[" + "Console" + "]":>15} Hooked')
else:
    print(f'{"[" + "Console" + "]":>15} Hooked')

a = MemoryWatch("some byte", 0x80FB0000, Datatype.BYTE)
b = MemoryWatch("some halfword", 0x80FB0002, Datatype.HALFWORD)
c = MemoryWatch("some word", 0x80FB0004, Datatype.WORD)
d = MemoryWatch("some float", 0x80FB0008, Datatype.FLOAT)
e = MemoryWatch("some double", 0x80FB000C, Datatype.DOUBLE)
f = MemoryWatch("some string", 0x80FB0014, Datatype.STRING)
g = ByteArrayMemoryWatch("some byte array", 0x80FB0050, 5)
h = BoolMemoryWatch("some bool", 0x804CEAED)

print(g.read())
a.write(0xea)
b.write(0x9225)
c.write(0x804cd458)
d.write(1.5)
e.write(3.0)
f.write("this is a string")
f.write("smaller string")
g.write(bytes([0xeb, 0xe4, 0x2a, 0x22, 0x5e, 0x85, 0x93, 0xe4, 0x48, 0xd9, 0xc5, 0x45, 0x73, 0x81, 0xaa, 0xf7]))
h.write(False)

print(a.read())
print(b.read())
print(c.read())
print(d.read())
print(e.read())
print(f.read())
print(g.read())

welderberg300Pipe = GSWFMemoryWatch("FlipFlop Pipe", 534)
welderberg300Pipe.write(False)

input("Press enter to set it to 1")
welderberg300Pipe.write(True)

input("Press enter to set it to 0")
welderberg300Pipe.write(False)