#! /usr/bin/env python
import wnck
import gtk, keybinder
import pdb


class WindowState(object):
    _windows = {}

    def set_windowstate(self, window, newstate):
        self._windows[window] = newstate

    def get_windowstate(self, window):
        try:
            state = self._windows[window]
        except KeyError, e:
            state = None
        return state

class Producivity(object):
    def active_window(self, windowlist):
        for window in windowlist:
            if window.is_active():
                return window
        
        return False

    def move_right(self, window):

        if window.is_maximized():
            window.unmaximize()
        new_width = self.width1/2
        new_height = self.height1/2
        newY = 0

        if self._window_screen == 1 and self.ws.get_windowstate(window.get_xid()) == 'div-right-scr-1':
            self._window_screen = 2
            self.move_left(window)
            return

        if self._window_screen ==  1:
            new_width = self.width1/2
            new_height = self.height1
            newX = new_width 
            self.ws.set_windowstate(window.get_xid(), 'div-right-scr-1')
        else:
            new_width = self.width2/2
            new_height = self.height2
            newX = new_width + self.width1
            self.ws.set_windowstate(window.get_xid(), 'div-right-scr-2')
        window.set_geometry(0, 255, newX, newY, new_width, new_height)

    def move_left(self, window):
        if window.is_maximized():
            window.unmaximize()

        if self._window_screen == 2 and self.ws.get_windowstate(window.get_xid()) == 'div-left-scr-2':
            self._window_screen = 1
            self.move_right(window)
            return

        if self._window_screen ==  1:
            new_width = self.width1/2
            new_height = self.height1
            newX = 0 
            newY = 0
            self.ws.set_windowstate(window.get_xid(), 'div-left-scr-1')
        else:
            new_width = self.width2/2
            new_height = self.height2
            newX = self.width1
            newY = 0
            self.ws.set_windowstate(window.get_xid(), 'div-left-scr-2')
        window.set_geometry(0, 255, newX, newY, new_width, new_height)
        
    def move_down(self, window):
        if window.is_maximized():
            window.unmaximize()
        else:
            if self._window_screen ==  1:
                new_width = self.width1
                new_height = self.height1/2
                newX = 0
                newY = new_height
                self.ws.set_windowstate(window.get_xid(), 'div-down-scr-2')
            else:
                new_width = self.width2
                new_height = self.height2/2
                newX = new_height + self.width1
                newY = new_height
                self.ws.set_windowstate(window.get_xid(), 'div-down-scr-2')
            window.set_geometry(0, 255, newX, newY, new_width, new_height)

    def move_up(self, window):
        msg = 'div-up-scr-%s' % (str(self._window_screen))
        if self.ws.get_windowstate(window.get_xid()) != msg:
            if self._window_screen == 1:
                new_width = self.width1
                new_height = self.height1/2
                newX = 0
                newY = 0
                self.ws.set_windowstate(window.get_xid(), 'div-up-scr-1')
            else:
                new_width = self.width2
                new_height = self.height2/2
                newX = self.width1
                newY = new_height
                self.ws.set_windowstate(window.get_xid(), 'div-up-scr-2')
                
            window.set_geometry(0, 255, newX, newY, new_width, new_height)
        else:
            window.maximize()

    def detect_screens(self):
        import commands
        (exitcode, commandoutput) = commands.getstatusoutput("xrandr | grep ' connected'")

        windows = {}
        incr = 1

        #FUGLY! REFACTOR CANDIDATE!
        for entry in commandoutput.split("\n"):
            windows[incr] = {}
            first_occ = entry.split('x', 1)
            lst_of_words = first_occ[0].split(' ')
            for word in lst_of_words:
                if word.isdigit():
                    windows[incr]['width'] = int(word)
            windows[incr]['height'] = int(first_occ[1].split('+')[0])
            incr = incr +1

        return windows


    def init(self):
        screens = self.detect_screens()
        for i in range(0, len(screens)):
            n =i+1
            name = 'screen%s_dimension' % (str(n))
            scr_w = 'width%s' % (str(n))
            scr_h = 'height%s' % (str(n))
            # magic to create: screenX_dimension (width, height) tuples
            setattr(self, name, (screens[n]['width'], screens[n]['height']))
            setattr(self, scr_w, screens[n]['width']) 
            setattr(self, scr_h, screens[n]['height']) 

        self._window_screen = 0
        self.screen = wnck.screen_get_default()
        self.ws = WindowState()

    def silent_shutdown(self):
        self.screen = None
        if 'wnck_shutdown' in dir(wnck):
            wnck.wnck_shutdown()


    def main(self, direction):
        self.screen.force_update()
        windows = self.screen.get_windows()
        if len(windows) == 0:
            #print "No windows found"
            return

        window = self.active_window(windows)
        if window is False:
            #print 'Couldnt find active window in: %s' % windows
            return 

        state = self.ws.get_windowstate(window.get_xid())

        # screen 1 or 2?
        (wX, wY, wWidth, wHeight) = window.get_client_window_geometry()
        #print "Window now:\nx: %s, y: %s, width: %s, height: %s" % (wX, wY, wWidth, wHeight)
        if wX < self.width1:
            #print 'Active window is on screen 1'
            self._window_screen = 1
        else:
            #print 'Active window is on screen 2'
            self._window_screen = 2

        move_method = getattr(self, 'move_'+direction)
        #print 'Moving window to: %s' % direction
        move_method(window)


if __name__ == '__main__':
    MagicKey = '<Super>'
    x = Producivity()
    x.init()
    keystr_right = MagicKey+"Right"
    keybinder.bind(keystr_right, x.main, "right")
    keystr_left = MagicKey+"Left"
    keybinder.bind(keystr_left, x.main, "left")
    keystr_left = MagicKey+"Down"
    keybinder.bind(keystr_left, x.main, "down")
    keystr_left = MagicKey+"Up"
    keybinder.bind(keystr_left, x.main, "up")
    try:
        gtk.main()
    except KeyboardInterrupt, e:
        x.silent_shutdown()
        exit()
