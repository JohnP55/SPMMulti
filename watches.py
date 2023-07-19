from enum import Enum
import dolphin_memory_engine as dme

class Datatype(Enum):
    BYTE = 1
    HALFWORD = 2
    WORD = 3
    FLOAT = 4
    DOUBLE = 5
    STRING = 6
    BYTEARRAY = 7
    BITFIELD = 8

class MemoryWatch:
    def __init__(self, name: str, address: int, datatype: Datatype) -> None:
        self.name = name
        self.address = address
        self.datatype = datatype
    
    @staticmethod
    def read_halfword(address:int) -> int:
        return (dme.read_byte(address) << 8) + dme.read_byte(address+1)

    @staticmethod
    def read_string(address:int) -> int:
        s = ""
        i = 0
        cur_char = ""
        while (cur_char := chr(dme.read_byte(address+i))) != '\0':
            s += cur_char
            i += 1
        return s

    @staticmethod
    def write_halfword(address:int, value:int) -> None:
        value %= 65536
        dme.write_byte(address, value >> 8)
        dme.write_byte(address+1, value & 0xff)

    @staticmethod
    def write_string(address:int, value:str) -> None:
        for i,e in enumerate(value):
            dme.write_byte(address+i, ord(e))
        dme.write_byte(address+len(value), 0) # add the null terminator at the end
    
    _accessor_methods = {
        Datatype.BYTE: (dme.read_byte, dme.write_byte),
        Datatype.HALFWORD: (read_halfword, write_halfword),
        Datatype.WORD: (dme.read_word, dme.write_word),
        Datatype.FLOAT: (dme.read_float, dme.write_float),
        Datatype.DOUBLE: (dme.read_double, dme.write_double),
        Datatype.STRING: (read_string, write_string),
    }

    def read(self):
        if self.datatype == Datatype.BYTEARRAY:
            return dme.read_bytes(self.address, self.len)
        return (MemoryWatch._accessor_methods[self.datatype][0])(self.address)
    
    def write(self, value):
        (MemoryWatch._accessor_methods[self.datatype][1])(self.address, value)

class ByteArrayMemoryWatch(MemoryWatch):
    def __init__(self, name: str, address: int, size: int = 0) -> None:
        super().__init__(name, address, Datatype.BYTEARRAY)
        self.size = size
    
    def read(self) -> bytes:
        return dme.read_bytes(self.address, self.size)
    
    def write(self, value:bytes):
        self.size = len(value)
        dme.write_bytes(self.address, value)

class BitFieldMemoryWatch(MemoryWatch):
    def __init__(self, name: str, address: int, bitmask:int = 0):
        super().__init__(name, address, Datatype.BITFIELD)
        self.bitmask = bitmask
    
    def read(self) -> bool:
        return dme.read_byte(self.address) & self.bitmask == self.bitmask
    
    def write(self, value:bool) -> None:
        res = dme.read_byte(self.address)
        if value:
            res |= self.bitmask
        else:
            res &= ~self.bitmask
        dme.write_byte(self.address, res)



watches = [
    MemoryWatch("Camera Mode", 0x8076ae48, Datatype.HALFWORD),
    MemoryWatch("Camera Position X", 0x8076af9c, Datatype.FLOAT),      
    MemoryWatch("Camera Position Y", 0x8076afa0, Datatype.FLOAT),      
    MemoryWatch("Camera Position Z", 0x8076afa4, Datatype.FLOAT),      
    MemoryWatch("Character 1", 0x804ceadc, Datatype.WORD),
    MemoryWatch("Character 2", 0x804ceae0, Datatype.WORD),
    MemoryWatch("Character 3", 0x804ceae4, Datatype.WORD),
    MemoryWatch("Character 4", 0x804ceae8, Datatype.WORD),
    MemoryWatch("Coordinate X", 0x804cd4b4, Datatype.FLOAT),
    MemoryWatch("Coordinate Y", 0x804cd4b8, Datatype.FLOAT),
    MemoryWatch("Coordinate Z", 0x804cd4bc, Datatype.FLOAT),
    MemoryWatch("Stored Z Position (7-3)", 0x804ce95c, Datatype.FLOAT),
    MemoryWatch("Hitbox X and Z", 0x804cd5ec, Datatype.FLOAT),
    MemoryWatch("Hitbox Y", 0x804cd5f0, Datatype.FLOAT),
    MemoryWatch("wallScanDistance", 0x804cd5fc, Datatype.FLOAT),
    MemoryWatch("HR X cord", 0x804cd830, Datatype.FLOAT),
    MemoryWatch("HR Y cord", 0x804cd834, Datatype.FLOAT),
    MemoryWatch("HR Z cord", 0x804cd838, Datatype.FLOAT),
    MemoryWatch("Effect", 0x804cd46b, Datatype.BYTE),
    MemoryWatch("Angle", 0x804cd5d0, Datatype.FLOAT),
    MemoryWatch("State", 0x804cd485, Datatype.BYTE),
    MemoryWatch("Sub State", 0x804cd494, Datatype.WORD),
    MemoryWatch("Cutscene Count (keyOff)", 0x804cd48d, Datatype.BYTE),
    MemoryWatch("Initial Speed", 0x804cd5a4, Datatype.FLOAT),
    MemoryWatch("Max Speed", 0x804cd5a8, Datatype.FLOAT),
    MemoryWatch("Pixl Coordinate X", 0x804cd07c, Datatype.FLOAT),
    MemoryWatch("Pixl Coordinate Y", 0x804cd080, Datatype.FLOAT),
    MemoryWatch("Pixl Coordinate Z", 0x804cd084, Datatype.FLOAT),
    MemoryWatch("Read Only Speed X and Z", 0x804cd5ac, Datatype.FLOAT),
    MemoryWatch("Respawn X", 0x804cd830, Datatype.FLOAT),
    MemoryWatch("Respawn Y", 0x804cd834, Datatype.FLOAT),
    MemoryWatch("Respawn Z", 0x804cd838, Datatype.FLOAT),
    MemoryWatch("Speed", 0x804cd828, Datatype.FLOAT),
    MemoryWatch("Flags", 0x804cd458, Datatype.WORD),
    MemoryWatch("Flags Misc", 0x804cd45c, Datatype.WORD),
    MemoryWatch("Flags Disp", 0x804cd460, Datatype.WORD),
    MemoryWatch("Flags Status", 0x804cd468, Datatype.WORD),
    MemoryWatch("Flags Effect", 0x804cd46c, Datatype.BYTE),
    MemoryWatch("X Scaling", 0x804cd514, Datatype.FLOAT),
    MemoryWatch("Y Scaling", 0x804cd518, Datatype.FLOAT),
    MemoryWatch("Z Scaling", 0x804cd51c, Datatype.FLOAT),
    MemoryWatch("Item slot 1", 0x804cea88, Datatype.HALFWORD),
    MemoryWatch("Item slot 2", 0x804cea8a, Datatype.HALFWORD),
    MemoryWatch("Item slot 3", 0x804cea8c, Datatype.HALFWORD),
    MemoryWatch("Item slot 4", 0x804cea8e, Datatype.HALFWORD),
    MemoryWatch("Item slot 5", 0x804cea90, Datatype.HALFWORD),
    MemoryWatch("Item slot 6", 0x804cea92, Datatype.HALFWORD),
    MemoryWatch("Item slot 7", 0x804cea94, Datatype.HALFWORD),
    MemoryWatch("Item slot 8", 0x804cea96, Datatype.HALFWORD),
    MemoryWatch("Item slot 9", 0x804cea98, Datatype.HALFWORD),
    MemoryWatch("Item slot 10", 0x804cea9a, Datatype.HALFWORD),
    MemoryWatch("Key Item 1", 0x804cea48, Datatype.HALFWORD),
    MemoryWatch("Key Item 2", 0x804cea4a, Datatype.HALFWORD),
    MemoryWatch("Key Item 3", 0x804cea4c, Datatype.HALFWORD),
    MemoryWatch("Key Item 4", 0x804cea4e, Datatype.HALFWORD),
    MemoryWatch("Key Item 5", 0x804cea50, Datatype.HALFWORD),
    MemoryWatch("Key Item 6", 0x804cea52, Datatype.HALFWORD),
    MemoryWatch("Key Item 7", 0x804cea54, Datatype.HALFWORD),
    MemoryWatch("Key Item 8", 0x804cea56, Datatype.HALFWORD),
    MemoryWatch("Key Item 9", 0x804cea58, Datatype.HALFWORD),
    MemoryWatch("Key Item 10", 0x804cea5a, Datatype.HALFWORD),
    MemoryWatch("Key Item 11", 0x804cea5c, Datatype.HALFWORD),
    MemoryWatch("Key Item 12", 0x804cea5e, Datatype.HALFWORD),
    MemoryWatch("Key Item 13", 0x804cea60, Datatype.HALFWORD),
    MemoryWatch("Key Item 14", 0x804cea62, Datatype.HALFWORD),
    MemoryWatch("Key Item 15", 0x804cea64, Datatype.HALFWORD),
    MemoryWatch("Key Item 16", 0x804cea66, Datatype.HALFWORD),
    MemoryWatch("Key Item 17", 0x804cea68, Datatype.HALFWORD),
    MemoryWatch("Key Item 18", 0x804cea6a, Datatype.HALFWORD),
    MemoryWatch("Key Item 19", 0x804cea6c, Datatype.HALFWORD),
    MemoryWatch("Key Item 20", 0x804cea6e, Datatype.HALFWORD),
    MemoryWatch("Key Item 21", 0x804cea70, Datatype.HALFWORD),
    MemoryWatch("Key Item 22", 0x804cea72, Datatype.HALFWORD),
    MemoryWatch("Key Item 23", 0x804cea74, Datatype.HALFWORD),
    MemoryWatch("Key Item 24", 0x804cea76, Datatype.HALFWORD),
    MemoryWatch("Key Item 25", 0x804cea78, Datatype.HALFWORD),
    MemoryWatch("Key Item 26", 0x804cea7a, Datatype.HALFWORD),
    MemoryWatch("Key Item 27", 0x804cea7c, Datatype.HALFWORD),
    MemoryWatch("Key Item 28", 0x804cea7e, Datatype.HALFWORD),
    MemoryWatch("Key Item 29", 0x804cea80, Datatype.HALFWORD),
    MemoryWatch("Key Item 30", 0x804cea82, Datatype.HALFWORD),
    MemoryWatch("Key Item 31", 0x804cea84, Datatype.HALFWORD),
    MemoryWatch("Key Item 32", 0x804cea86, Datatype.HALFWORD),
    MemoryWatch("Pixl slot 1", 0x804ceaec, Datatype.WORD),
    MemoryWatch("Pixl slot 2", 0x804ceaf0, Datatype.WORD),
    MemoryWatch("Pixl slot 3", 0x804ceaf4, Datatype.WORD),
    MemoryWatch("Pixl slot 4", 0x804ceaf8, Datatype.WORD),
    MemoryWatch("Pixl slot 5", 0x804ceafc, Datatype.WORD),
    MemoryWatch("Pixl slot 6", 0x804ceb00, Datatype.WORD),
    MemoryWatch("Pixl slot 7", 0x804ceb04, Datatype.WORD),
    MemoryWatch("Pixl slot 8", 0x804ceb08, Datatype.WORD),
    MemoryWatch("Pixl slot 9", 0x804ceb0c, Datatype.WORD),
    MemoryWatch("Pixl slot 10", 0x804ceb10, Datatype.WORD),
    MemoryWatch("Pixl slot 11", 0x804ceb14, Datatype.WORD),
    MemoryWatch("Pixl slot 12 (Unused)", 0x804ceb18, Datatype.WORD),
    MemoryWatch("Pixl slot 13 (Unused)", 0x804ceb1c, Datatype.WORD),
    MemoryWatch("Pixl slot 14 (Unused)", 0x804ceb20, Datatype.WORD),
    MemoryWatch("Pixl slot 15 (Unused)", 0x804ceb24, Datatype.WORD),
    MemoryWatch("Pixl slot 16 (Unused)", 0x804ceb28, Datatype.WORD),
    MemoryWatch("File name", 0x804e2570, Datatype.STRING),
    MemoryWatch("Savefile ID", 0x804e262c, Datatype.WORD),
    MemoryWatch("Language", 0x804e2558, Datatype.WORD),
    MemoryWatch("Game Speed", 0x804e256c, Datatype.FLOAT),
    MemoryWatch("Map to Save", 0x804e2594, Datatype.STRING),
    MemoryWatch("NextArea", 0x804cf240, Datatype.STRING),
    MemoryWatch("NextBero", 0x804cf280, Datatype.STRING),
    MemoryWatch("NextMap", 0x804cf260, Datatype.STRING),
    MemoryWatch("NowSeq", 0x8056d0d8, Datatype.WORD),
    MemoryWatch("NextSeq", 0x8056d0dc, Datatype.WORD),
    MemoryWatch("Sequence Position", 0x804e2690, Datatype.WORD),
    MemoryWatch("In Transition", 0x807aefac, Datatype.WORD),
    MemoryWatch("Out Transition", 0x807aefb0, Datatype.WORD),
    MemoryWatch("Map Transition Stage", 0x804cf364, Datatype.WORD),
    MemoryWatch("2-3 Rubees", 0x804e2b61, Datatype.WORD),
    MemoryWatch("Rubees to Win (Generator Room)", 0x804c9994, Datatype.WORD),
    MemoryWatch("Rubees to Win / 30 (VIP Room)", 0x804c9998, Datatype.WORD),
    MemoryWatch("3D Gauge", 0x804cea3c, Datatype.WORD),
    MemoryWatch("Attack", 0x804cea30, Datatype.WORD),
    MemoryWatch("Coins", 0x804cea44, Datatype.WORD),
    MemoryWatch("Flipside Tokens", 0x804cf0b0, Datatype.WORD),
    MemoryWatch("HP", 0x804cea34, Datatype.WORD),
    MemoryWatch("Level", 0x804cea2c, Datatype.WORD),
    MemoryWatch("Max HP", 0x804cea38, Datatype.WORD),
    MemoryWatch("Score", 0x804cea40, Datatype.WORD),
    MemoryWatch("3D Mode", 0x8076ae4a, Datatype.HALFWORD),
    MemoryWatch("Effect Timer", 0x804ce2e0, Datatype.FLOAT),
    MemoryWatch("Current Character", 0x804cd490, Datatype.BYTE),
    MemoryWatch("Gravity Side", 0x804ce7bb, Datatype.BYTE),
    MemoryWatch("Gravity Vector X", 0x804ce7c8, Datatype.FLOAT),
    MemoryWatch("Gravity Vector Y", 0x804ce7cc, Datatype.FLOAT),
    MemoryWatch("Gravity Vector Z", 0x804ce7d0, Datatype.FLOAT),
    MemoryWatch("Gravity Vector Reciprocal X", 0x804ce7bc, Datatype.FLOAT),
    MemoryWatch("Gravity Vector Reciprocal Y", 0x804ce7c0, Datatype.FLOAT),
    MemoryWatch("Gravity Vector Reciprocal Z", 0x804ce7c4, Datatype.FLOAT),
    MemoryWatch("Inputs", 0x804cd764, Datatype.BYTE),
    MemoryWatch("Invincibility Timer", 0x804cd4a0, Datatype.FLOAT),
    MemoryWatch("Map Render Mode", 0x8076afdb, Datatype.BYTE),
    MemoryWatch("Mega Star Timer", 0x804cd840, Datatype.FLOAT),
    MemoryWatch("Pane #", 0x804ce9a8, Datatype.WORD),
    MemoryWatch("Pit IGT", 0x804d0e08, Datatype.WORD),
    MemoryWatch("Pit Key X", 0x80781eb4, Datatype.FLOAT),
    MemoryWatch("Pit Key Y", 0x80781eb8, Datatype.FLOAT),
    MemoryWatch("Pit Key Z", 0x80781ebc, Datatype.FLOAT),
    MemoryWatch("Pit Room", 0x804e2a95, Datatype.BYTE),
    MemoryWatch("Pixl State", 0x804cd05f, Datatype.BYTE),
    MemoryWatch("RNG seed", 0x8056d13c, Datatype.WORD),
    MemoryWatch("Swimming Speed", 0x804cd5b0, Datatype.FLOAT),
    MemoryWatch("Time Freeze", 0x804e2560, Datatype.WORD),
    MemoryWatch("Tippi", 0x804cd398, Datatype.WORD),
    MemoryWatch("Tippi State", 0x804cd3b8, Datatype.WORD),
    MemoryWatch("MarioGameSpeedScale", 0x8056d908, Datatype.FLOAT),
    MemoryWatch("Gravity (Ascent) (Mario)", 0x803e744c, Datatype.FLOAT),
    MemoryWatch("Gravity (Descent) (Mario)", 0x803e745c, Datatype.FLOAT),
    BitFieldMemoryWatch("FlipFlop Pipe", 0x804E26D5, 0x40)
]

def find_watch(name: str) -> MemoryWatch:
    for watch in watches:
        if watch.name == name:
            return watch
    return None