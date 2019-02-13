#### simple watchpoint example

[**loop.c**](../code/loop.c)

```
#include <stdio.h>

int main()
{
  int i,
      n = 5;
  for (i = 0; i < n; i++) {
    printf("%d\n", i);
  }
  return 0;
}
```

Now do

```
> clang loop.c -g -o loop
> export PATH=/usr/bin
```

and then

```
> lldb loop
(lldb) target create "loop"
Current executable set to 'loop' (x86_64).
(lldb) b main
Breakpoint 1: where = loop`main + 15 at loop.c:6, address = 0x0000000100000f3f
(lldb) r
Process 5725 launched: '/Users/telliott_admin/Desktop/loop' (x86_64)
Process 5725 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
    frame #0: 0x0000000100000f3f loop`main at loop.c:6
   3   	int main()
   4   	{
   5   	  int i,
-> 6   	      n = 5;
   7   	  for (i = 0; i < n; i++) {
   8   	    printf("%d\n", i);
   9   	  }
Target 0: (loop) stopped.
```

To set a watchpoint on i

```
(lldb) wa s v i
Watchpoint created: Watchpoint 1: addr = 0x7ffeefbffa08 size = 4 state = enabled type = w
    declare @ '/Users/telliott_admin/Desktop/loop.c:5'
    watchpoint spec = 'i'
    new value: 16438
(lldb) cont
Process 5725 resuming

Watchpoint 1 hit:
old value: 16438
new value: 0
Process 5725 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = watchpoint 1
    frame #0: 0x0000000100000f4d loop`main at loop.c:7
   4   	{
   5   	  int i,
   6   	      n = 5;
-> 7   	  for (i = 0; i < n; i++) {
   8   	    printf("%d\n", i);
   9   	  }
   10  	  return 0;
Target 0: (loop) stopped.
(lldb) p i
(int) $0 = 0
```

and continue

```
(lldb) cont
Process 5725 resuming
0

Watchpoint 1 hit:
old value: 0
new value: 1
Process 5725 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = watchpoint 1
    frame #0: 0x0000000100000f76 loop`main at loop.c:7
   4   	{
   5   	  int i,
   6   	      n = 5;
-> 7   	  for (i = 0; i < n; i++) {
   8   	    printf("%d\n", i);
   9   	  }
   10  	  return 0;
Target 0: (loop) stopped.
(lldb) p i
(int) $1 = 1
(lldb) 
```