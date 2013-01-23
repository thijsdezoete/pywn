import subprocess

#output, error = subprocess.Popen(
#                    command.split(' '), stdout=subprocess.PIPE,
#                    stderr=subprocess.PIPE).communicate()


def transform_xrandr_output(xrandr):
    #print xrandr
    # find the '+0+0' part, which is listed after the resolution currently used in this screen
    first_index = xrandr.find('+0+0')
    print first_index

    return xrandr


def query_xrandr(in_file=None):
    """ returns list of connected screens and their resolutions """
    xrandr_info_command = "xrandr"

    # Get from file or query xrandr
    if not in_file:
        _xrandr = subprocess.Popen([xrandr_info_command], stdout=subprocess.PIPE)
    else:
        print 'Getting resolutions from file...'
        _xrandr = subprocess.Popen(['cat', in_file], stdout=subprocess.PIPE)

    connected_devices = subprocess.Popen(['grep',  " connected"], stdin=_xrandr.stdout, stdout=subprocess.PIPE)
    #connected_devices = subprocess.Popen(['grep',  "x"], stdin=_xrandr.stdout, stdout=subprocess.PIPE)
    _xrandr.stdout.close()
    all_windows = []
    while connected_devices.poll() is None:
        output = connected_devices.stdout.readline().rstrip()
        if output == '':
            # we don't need empty lines
            continue
        print output
        print connected_devices.poll()
        all_windows.append(output)

    return all_windows

    test = [transform_xrandr_output(window) for window in all_windows]

    print test

    #test = [resolution for resolution in output]
    #print test

    #
    #(exitcode, commandoutput) = commands.getstatusoutput("xrandr | grep ' connected'")
    #windows = {}
    #incr = 1
    ##FUGLY! REFACTOR CANDIDATE!
    #for entry in commandoutput.split("\n"):
    #    windows[incr] = {}
    #    first_occ = entry.split('x', 1)
    #    lst_of_words = first_occ[0].split(' ')
    #    for word in lst_of_words:
    #        if word.isdigit():
    #            windows[incr]['width'] = int(word)
    #    windows[incr]['height'] = int(first_occ[1].split('+')[0])
    #    incr = incr + 1
    #return windows

if __name__ == '__main__':
    import sys

    x = query_xrandr() if len(sys.argv) < 2 else query_xrandr(sys.argv[1])

    print x
    #if len(sys.argv) < 2:
    #    x = query_xrandr()
    #else:
    #    x = query_xrandr(sys.argv[1])
