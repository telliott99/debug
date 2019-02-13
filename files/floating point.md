#### Floating point representation

I found a page about floating point [here](http://fabiensanglard.net/floating_point_visually_explained/).

Here is a 32-bit example.  There are three components

```
S = 1 bit
E = 8 bits
M = 32 - 9 = 23 bits
```

``S`` is the <i>sign</i> bit.  Say we want to represent pi as a floating point value.  ``S = 0`` since ``pi > 0``.

``E`` is the exponent.  

Imagine constructing a series of <i>windows</i> or ranges ``2^n, 2^n+1``.  

In this case ``2 < 3.14 < 4`` so the window is ``[2,4]`` and starts at ``2^1``.  However, the exponent ``E`` is not ``1``.  For some reason ``E`` counts down

```
E = 128 - exp = 127
  = 0x 100 0000 0
```

Last, we must determine ``M``.  Compute the difference between our number (normalized to x.yyyy) and the beginning of the range, and divide that by the length of the range.  Let's call that ``o`` for offset:

```
o = (pi - 2)/(4-2) = pi/2 - 1
  = 0.5707963267948966
M = 2^23 * o
  = 4788186.633322284
```

The result is truncated, fractional digits are lost.

```
  = 4788186
  = 0x 100 1001 0000 1111 1101 1010
```

Since

```
>>> e = 2**23 * 1.0
>>> e
8388608.0
>>> 2 * (4788186/e + 1)
3.141592502593994
>>> 2 * (4788187/e + 1)
3.1415927410125732
>>>
```

Thus, all we can say is that pi lies between ``3.14159250..`` and ``3.14159274..``

Combining these results:

```
S = 0x 0
E =  0x 100 0000 0
M =            0x 100 1001 0000 1111 1101 1010

0100 0000 0100 1001 0000 1111 1101 1010
```

In hex, that is ``40 49 0f db``

#### Python

Take a look using the ``bitstring`` [module](https://pythonhosted.org/bitstring/packing.html
):

```
>>> from math import pi
>>> import bitstring
>>> b = bitstring.pack('>d', pi)
>>> sbit, wbits, pbits = b[:1], b[1:12], b[12:]
>>> wbits.bin
'10000000000'
>>> pbits.bin
'1001001000011111101101010100010001000010110100011000'
>>> 
```

The result is a bit funny because this is a 64-bit precision value.  However, aside from the additional binary digits this part checks out.

And ``struct``:

```
>>> import struct
>>> struct.pack('f', pi)
'\xdb\x0fI@'
>>> str(_)
'\xdb\x0fI@'
>>> struct.Struct('f').unpack(_)
(3.1415927410125732,)
>>> pi
3.141592653589793
>>> 
```

The hex part also checks out (``hex(ord('I'))`` is ``0x49`` and ``hex(ord('I'))`` is ``0x40``).

Notice that the result returned is the upper bound on the window:  ``3.14159274..``

#### Using a C with a debuggger

Not that I don't trust Python, but I'm not quite sure of the results above because we tell Python what we have, with that ``f``.

So I found a nice [page](https://www.recurse.com/blog/5-learning-c-with-gdb) showing another way.

First, write a minimal C program.  We don't print anything so we don't need any libraries.

*minimal.c*
```
int main()
{
  int i = 258;
  float f = 3.141592653589793;
  return 0;
}
```

I used ``clang`` to compile it:

```
clang  -g minimal.c -o minimal
```

I tried to use ``gdb``, but there were issues.  I will write about that separately.  Instead, I used ``lldb`` which is provided by the Developer Tools.  There's a [cheatsheat](https://lldb.llvm.org/lldb-gdb.html) and other resources on the web.

It also has an issue, that it was picking up the Homebrew python, and that caused an issue, but it's easily fixed by manipulating PATH.

```
> PATH=/usr/bin /usr/bin/lldb minimal
(lldb) target create "minimal"
Current executable set to 'minimal' (x86_64).
(lldb) b main
Breakpoint 1: where = minimal`main + 21 at minimal.c:3, address = 0x0000000100000fa5
(lldb) r
Process 1028 launched: '/Users/telliott_admin/Desktop/minimal' (x86_64)
Process 1028 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
    frame #0: 0x0000000100000fa5 minimal`main at minimal.c:3
   1   	int main()
   2   	{
-> 3   	  int i = 258;
   4   	  float f = 3.141592653589793;
   5   	  return 0;
   6   	}
Target 0: (minimal) stopped.
(lldb) n
Process 1028 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = step over
    frame #0: 0x0000000100000fac minimal`main at minimal.c:4
   1   	int main()
   2   	{
   3   	  int i = 258;
-> 4   	  float f = 3.141592653589793;
   5   	  return 0;
   6   	}
Target 0: (minimal) stopped.
(lldb) x/4xb &i
0x7ffeefbffa18: 0x02 0x01 0x00 0x00
(lldb) x/4db &i
0x7ffeefbffa18: 2
0x7ffeefbffa19: 1
0x7ffeefbffa1a: 0
0x7ffeefbffa1b: 0
(lldb) print sizeof(f)
(unsigned long) $2 = 4
(lldb) n
Process 1028 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = step over
    frame #0: 0x0000000100000fb1 minimal`main at minimal.c:5
   2   	{
   3   	  int i = 258;
   4   	  float f = 3.141592653589793;
-> 5   	  return 0;
   6   	}
Target 0: (minimal) stopped.
(lldb) x/4xb &f
0x7ffeefbffa14: 0xdb 0x0f 0x49 0x40
```

We did ``b main`` to set a breakpoint, ``r`` to run up to the breakpoint, to ``n`` (next) to get past where the float ``f`` is assigned its value, and then we ``x`` examine the memory at the address of f, ``&f``.

The result is "little-endian"

```
0xdb 0x0f 0x49 0x40

0x40 b0100 0000
0x49 b0100 1001
0x0f b0000 1111
0xdb b1101 1011
```

Concatenate the results and compare with ``E`` and ``M`` (or simply recall the hex output from previously).

```
01000000010010010000111111011011
        b10010010000111111011010
b10000000

```

There is one slight difference:  the very last bit is a ``1``.  I believe the reason for this is that the offset is more than half way along the interval, so the upper end of the interval is what is chosen for the value.  This explains the Python result as well.