#### custom commands

```
> cd /Users/telliott_admin/Dropbox/Github/Github.newnew/debug 
> export PATH=/usr/bin
> lldb exe/min
(lldb) target create "exe/min"
Current executable set to 'exe/min' (x86_64).
(lldb) b main
Breakpoint 1: where = min`main + 21 at min.c:3, address = 0x0000000100000fa5
(lldb) r
Process 2790 launched: '/Users/telliott_admin/Dropbox/Github/Github.newnew/debug/exe/min' (x86_64)
Process 2790 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
    frame #0: 0x0000000100000fa5 min`main at min.c:3
   1   	int main()
   2   	{
-> 3   	  int i = 258;
   4   	  float f = 3.141592653589793;
   5   	  return 0;
   6   	}
Target 0: (min) stopped.
```

Now add a breakpoint on line 4.  ``br command add 2`` refers to the 2nd breakpoint:

```
(lldb) b 4
Breakpoint 2: where = min`main + 28 at min.c:4, address = 0x0000000100000fac
(lldb) br command add 2
Enter your debugger command(s).  Type 'DONE' to end.
> fr v 
> DONE
```

The DONE disappears and we return to ``(lldb)``.

```
(lldb) continue
Process 2790 resuming
(lldb)  fr v
(int) i = 258
(float) f = 0.0000000000000000000000000000000000000000459149455

Process 2790 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 2.1
    frame #0: 0x0000000100000fac min`main at min.c:4
   1   	int main()
   2   	{
   3   	  int i = 258;
-> 4   	  float f = 3.141592653589793;
   5   	  return 0;
   6   	}
Target 0: (min) stopped.
```

When we hit breakpoint 2, the script executed ``fr v``, printing the values of ``i`` and ``f``.

