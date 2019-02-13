import lldb

def print_frame(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()

    for frame in thread:
        print >>result, str(frame)
    
def print_vars(debugger, command, *args):
    exe_ctx = args[0]
    result = args[1]
    target = exe_ctx.GetTarget()
    thread = exe_ctx.GetThread()
    
    for frame in thread:
        for e in frame.vars:
            print >>result, str(e)
            
def __lldb_init_module(debugger, internal_dict): 
    cmd = 'command script add -f cmds3.print_vars pv' 
    debugger.HandleCommand(cmd)
    s = 'The "print_vars" python command has been installed and is ready for use.'
    print s



