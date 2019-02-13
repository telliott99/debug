#### run

-  ``r`` or ``run``

Stopping and resetting a running process keeps breakpoints.

- ``ctrl-C`` stops runaway program

```
process launch --stop-at-entry
```

#### break

All of these are equivalent: 

- ``b main``
- ``br s -n main``
- ``breakpoint set --name main``


- ``br`` is short for ``breakpoint``
- ``b`` is an <i>alias</i> for ``breakpoint set``

hence ``br main`` is not valid because there's no ``set``.

- ``br disable --name main``
- ``br enable --name main``
- ``br clear --name main``

```
b 18
b file.c:12
br list
```

Clearing or removing breakpoints uses their ids

```
b clear 1
br delete 1
```

```
br set foo condition (x > 3)
breakpoint set --name foo --name bar
```

If lldb says something like ``breakpoint pending`` what it means is that it couldn't find any actual locations to match the logical breakpoint.

#### watch

- ``watchpoint set variable global_var``
- ``wa s v global_var``  same as above
- ``watch z > 128`` conditional

can also do

```
watchpoint modify 1 -c (condition)
```

to add a condition to an existing watchpoint.

#### step

- ``s`` or ``step`` to step <b>into</b> a function
- ``n`` or ``next`` to step over a function
- ``si``
- ``ni``
- ``c`` or ``continue`` go to next breakpoint

more

- ``finish`` the current frame
- ``until``  finish a loop but stay in frame
- ``thread return <RETURN EXPRESSION>``

#### print

- ``p variable-name``
- ``fr v``      frame vars
- ``ta v  ``    global vars

By default, lldb prints all vars.

```
(lldb) fr v
(int) i = 12342
(float) f = 0.0000000000000000000000000000000000000000459149455
```

specify which one(s) to print

```
(lldb) fr v i
(int) i = 12342
```

#### list

Shows code at a line number or ...

- ``list <line-num>``
- ``list <memory-address>``
- ``list -[<count>]``

- ``thread list``

#### backtrace

```
(lldb) bt
* thread #1, stop reason = instruction step over
  * frame #0: 0x0000000100004001 dyld`_dyld_start + 1
```

#### examine memory

- ``x foo``
- ``x/4b &foo``
- ``x/4b 0xbffff3c0``

formatting:  4 means 4 bytes requested, hex is default output.

##### look at registers

- ``p/t $rax``
- ``register write rax 123``

#### frame

The frame of the currently executing function is ``frame 0``

- ``f 0`` or ``frame 0`` change to frame of caller

```
(lldb) f 0
frame #0: 0x0000000100000fa5 min`main at min.c:3
   1   	int main()
   2   	{
-> 3   	  int i = 258;
   4   	  float f = 3.141592653589793;
   5   	  return 0;
   6   	}
```

- ``u`` or ``up`` go from ``1`` to ``0`` e.g.
- ``d`` or ``down``

#### thread

- ``t <thread-id>`` or ``thread <thread-id>``

to change threads

#### info

- ``info break``

#### help

- ``help breakpoints``

#### command completion

lldb supports command completion.  Hence, if we have a C function ``func`` and do ``b f<TAB>``

```
(lldb) b func 
Breakpoint 2: where = min`func + 12 at min1.c:4, address = 0x0000000100000f1c
```

#### alias

```
command unalias b
command alias b breakpoint
help command alias
command alias bpl breakpoint list
```

```
command alias bfl breakpoint set -f %1 -l %2
```

``bfl`` for ``breakpoint-file-line``, would now take two positional arguments for the file name and the line number.
