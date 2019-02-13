import lldb

def print_frame(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()

    for frame in thread:
        print >>result, str(frame)
            
def __lldb_init_module(debugger, internal_dict): 
    cmd = 'command script add -f cmds2.print_frame print_frame' 
    debugger.HandleCommand(cmd)
    s = 'The "print_frame" python command has been installed and is ready for use.'
    print s



