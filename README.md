#### Debugging

I haven't used the debugger much, since in Python it's so easy to do "caveman debugging" with ``print`` statements.

But I was working on a project.

#### Floating point

I started by trying to understand the basics of floating point representation

- [floating point](files/floating-point.md)

and then to test it, came up with the idea of directly examining memory in the debugger.  

I started by trying gdb, finding that's not present in Developer's Tools anymore, and finding that the Homebrew version is broken.

That led me to lldb ([cheatsheet](quick ref.md)).

#### Debugging with lldb

- [Basic lldb commands, floating point](files/1.md)
- [simple watchpoint](files/wp.md)
- [custom commands](files/custom-commands.md)

Norm Matloff has a book about gdb.

- [debug Matloff insertion sort example](files/2.md)

#### Python stuff

- [Call Python script from lldb using .lldbinit file](files/3.md)
- [more about Python from lldb](files/4.md)
- [Fancier Python script triggered at watchpoint](files/6.md)

#### pdb

- [pdb, the Python debugger](files/5.md)

A shaggy dog story about gdb on macOS

- [gdb](files/gdb.md)