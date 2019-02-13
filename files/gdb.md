#### trying gdb

Homebrew has a formula for gdb.

```
> brew install gdb
Updating Homebrew...
==> Auto-updated Homebrew!
..
==> Downloading https://homebrew.bintray.com/bottles/gdb
Already downloaded: /Users/telliott_admin/Library/Caches/Homebrew/downloads/da5afc0b249339dbfc57d2c96e065ece3207ee9eaa53d99444663234d7a3b7b8--gdb-8.2.1.mojave.bottle.tar.gz
==> Pouring gdb-8.2.1.mojave.bottle.tar.gz
==> Caveats
gdb requires special privileges to access Mach ports.
You will need to codesign the binary. For instructions, see:

  https://sourceware.org/gdb/wiki/BuildingOnDarwin

On 10.12 (Sierra) or later with SIP, you need to run this:

  echo "set startup-with-shell off" >> ~/.gdbinit
==> Summary
🍺  /usr/local/Cellar/gdb/8.2.1: 55 files, 26.9MB
> 
```

Let's ignore the warning and just try:

```
> gdb min
..
(gdb) b main
Breakpoint 1 at 0x100000fa5: file code/min.c, line 3.
(gdb) r
Starting program: /Users/telliott_admin/Desktop/min 
Unable to find Mach task port for process-id 3943: (os/kern) failure (0x5).
 (please check gdb is codesigned - see taskgated(8))
(gdb) 
```

#### Code-signing

[Permissions instructions](https://sourceware.org/gdb/wiki/PermissionsDarwin)

Following the instructions, I used the Keychain Access app to make a self-signed certificate.  Check our work:

```
> security find-certificate -c gdb-cert
keychain: "/Library/Keychains/System.keychain"
version: 256
class: 0x80001000 
attributes:
..
```

Check that it's not expired (see instructions).  Construct ``gdb-entitlement.xml`` (again, see instructions).  And sign it:

```
> codesign --entitlements gdb-entitlement.xml -fs gdb-cert $(which gdb)
>
```

Check our work:

```
> codesign -vv $(which gdb)
/usr/local/bin/gdb: valid on disk
/usr/local/bin/gdb: satisfies its Designated Requirement
>
```

Reboot to "refresh" various things...  Also

```
> echo "set startup-with-shell off" >> ~/.gdbinit
```

Does it work?

```
> gdb min
..
(gdb) b main
Breakpoint 1 at 0x100000fa5: file code/min.c, line 3.
(gdb) r
Starting program: /Users/telliott_admin/Desktop/min 
[New Thread 0x2703 of process 652]
```

And it hangs.  The Homebrew version is 8.2.1.

Try [this](https://gist.github.com/gravitylow/fb595186ce6068537a6e9da6d8b5b96d) (user lokoum)

```
brew uninstall --force gdb
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/c3128a5c335bd2fa75ffba9d721e9910134e4644/Formula/gdb.rb
> gdb --version
GNU gdb (GDB) 8.0.1
```

and 

```
codesign -fs [cert-name] /usr/local/bin/gdb
```

Try it:

```
BFD: /Users/telliott_admin/Desktop/min: unknown load command 0x32
BFD: /Users/telliott_admin/Desktop/min: unknown load command 0x32
"/Users/telliott_admin/Desktop/min": not in executable format: File format not recognized
```

This is the problem I got to the last time I tried this.  Check the first answer [here](https://stackoverflow.com/questions/52529838/gdb-8-2-cant-recognized-executable-file-on-macos-mojave-10-14).

```
> otool -l min
..
Load command 8
       cmd LC_BUILD_VERSION
   cmdsize 32
  platform macos
       sdk 10.14
     minos 10.14
    ntools 1
      tool ld
   version 409.12
```

To fix this, you'll have to build ``gdb`` from source.

So I did that and code-signed it and ... it kinda sorta starts and then hangs.  But when you kill and restart gdb it appears to work.

```
(gdb) b main
Breakpoint 1 at 0x100000fa5: file code/min.c, line 3.
(gdb) r
Starting program: /Users/telliott_admin/Dropbox/Github/Github.newnew/debug/exe/min 
[New Thread 0x1c03 of process 39922]
warning: unhandled dyld version (15)

Thread 2 hit Breakpoint 1, main () at code/min.c:3
3	  int i = 258;
(gdb) p i
$1 = 12342
(gdb) n
4	  float f = 3.141592653589793;
(gdb) p i
$2 = 258
(gdb)
```

