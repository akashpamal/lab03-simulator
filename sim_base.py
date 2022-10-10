from calendar import c

# Used https://pyquestions.com/converting-a-number-to-binary-with-a-fixed-length to figure out how to make a fixed length binary string from an int

def get_bits(number, idx1, idx2):
    """Returns the bits of number between idx1 and idx2 as an integer"""
    if idx1 > idx2:
        low, num = idx2, idx1-idx2
    else:
        low, num = idx1, idx2-idx1
    return (number >> low) & ((1 << num)-1)


def execute(instruction, oldPC):
    """Handles a single instruction, returning the new PC"""
    global M, R, rsp
    
    bin_instruction = '{0:08b}'.format(instruction)
    # to do: add instructions here
    # if bin_instruction[0] == 1: # If set, an invalid instruction. Do not do work or advance the PC if this bit is 1.
    #     return oldPC
    
    icode = bin_instruction[0:4] # Specifies what action to take
    a = bin_instruction[4: 6] # The index of a register
    b = bin_instruction[6: 8] # The index of another register, or details about icode

    icode = int(icode, 2)
    a = int(a, 2)
    b = int(b, 2)

    if icode == 0:
        R[a] = R[b]
    elif icode == 1:
        R[a] += R[b]
    elif icode == 2:
        R[a] &= R[b]
    elif icode == 3:
        R[a] = M[R[b]]
    elif icode == 4:
        M[R[b]] = R[a]
    elif icode == 5:
        if b == 0:
            R[a] = ~R[a]
        elif b == 1:
            R[a] = -R[a]
        elif b == 2:
            R[a] = not R[a]
        elif b == 3:
            R[a] = oldPC
    elif icode == 6:
        if b == 0:
            R[a] = M[oldPC + 1]
        elif b == 1:
            R[a] += M[oldPC + 1]
        elif b == 2:
            R[a] &= M[oldPC + 1]
        elif b == 3:
            R[a] = M[M[oldPC + 1]]
        oldPC += 1 # net increase pc by 2
    elif icode == 7:
        if R[i] == 0 or R[i] >= 0x80:
            return R[b]
    elif icode == 8:
        pass
    else: # icode > 8
        if b == 0:
            rsp -= 1
            M[rsp] = R[a]
        elif b == 1:
            R[a] = M[rsp]
            rsp += 1
        elif b == 2:
            R[a] = M[oldPC+2]
            oldPC = M[oldPC+1] - 1 # net don't change pc
        else: # b == 3
            rsp -= 1
            oldPC = M[rsp]

    return oldPC + 1



# initialize memory and registers
R = [0 for i in range(4)]
M = [0 for i in range(256)]
rsp = 0xFF

# initialize control registers; do not modify these directly
_ir = 0
_pc = 0


def cycle():
    """Implement one clock cycle"""
    global M, R, _pc, _ir, rsp
    
    # execute
    _ir = M[_pc]
    _pc = execute(_ir, _pc)
    
    # enforce the fixed-length nature of values
    for i in range(len(R)): R[i] &= 0b11111111
    for i in range(len(M)): M[i] &= 0b11111111
    _pc &= 0b11111111
    

def showState():
    """Displays all processor state to command line"""
    print('-'*40)
    print('last instruction = 0b{:08b} (0x{:02x})'.format(_ir, _ir))
    for i in range(4):
        print('Register {:02b} = 0b{:08b} (0x{:02x})'.format(i, R[i], R[i]))
    print('next PC = 0b{:08b} (0x{:02x})'.format(_pc, _pc))
    print('//////////////////////// Memory \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
    for i in range(0, 256, 16):
        print('0x{:02x}-{:02x}'.format(i, i+15), end=': ')
        for j in range(16):
            print('{:02x}'.format(M[i+j]), end=' ')
        print()
        if not any(M[i+j:]):
            break
    print('-'*40)


if __name__ == '__main__':
    import sys, os.path
    
    if len(sys.argv) <= 1:
        print('USAGE: python', sys.argv[0], 'memory.txt\n    where memory.txt is a set of bytes in hex')
        print('USAGE: python', sys.argv[0], 'byte [byte, byte, ...]\n    where the bytes are in hex and will be loaded into memory before running')
        quit()
    
    if os.path.exists(sys.argv[1]):
        with open(sys.argv[1]) as f:
            i = 0
            for b in f.read().split():
                M[i] = int(b, 16)
                i += 1
    else:
        i = 0
        for b in sys.argv[1:]:
            M[i] = int(b, 16)
            i += 1
    
    showState()
    while True:
        n = input('Take how many steps (0 to exit, default 1)? ')
        try:
            n = int(n)
        except:
            n = 1
        if n <= 0: break
        for i in range(n):
            cycle()
            showState()
