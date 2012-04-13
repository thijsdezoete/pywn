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
            print "Maximized window"
            window.unmaximize()
        (width1, height1) = self.screen1_dimension
        (width2, height2) = self.screen2_dimension
        continue_resize = True
        new_width = width1/2
        new_height = height1/2
        newY = 0
        #if window.is_maximized():
        #    continue_resize = False
        #    # maximize on other screen
        #    if self._window_screen ==  1:
        #        print 'window screen 1'
        #        if self._window_screen != 1:
        #            newX = width1 + 10
        #            window.maximize()
        #            window.set_geometry(0, 255, newX, newY, newX, new_height)
        #            self._window_screen = 1
        #        else:
        #            print 'window screen unmaximize and continue resize'
        #            # request unmaximize....
        #            window.unmaximize()
        #            continue_resize = True
        #    else:
        #        if self._window_screen != 2:
        #            newX = 0
        #            window.maximize()
        #            window.set_geometry(0, 255, newX, newY, newX, new_height)
        #            self._window_screen = 1
        #        else: 
        #            window.unmaximize()
        #            continue_resize = True

        #if not continue_resize:
        #    continue_resize = False
        #    return
        

        #if self.ws.get_windowstate(window.get_xid()) == 'div-right-scr-1':
        #    print 'move window from screen 1 to 2 move-continue: %s' % continue_resize
        #    self._window_screen = 2

        newY = 0
        if self._window_screen ==  1:
            new_width = width1/2
            new_height = height1
            newX = new_width 
            self.ws.set_windowstate(window.get_xid(), 'div-right-scr-1')
        else:
            new_width = width2/2
            new_height = height2
            newX = new_width + width1
            self.ws.set_windowstate(window.get_xid(), 'div-right-scr-2')
        print "Moving (%s) to x: %s, y: %s, width: %s, height: %s" % (window.get_name(), newX, newY, new_width, new_height)
        window.set_geometry(0, 255, newX, newY, new_width, new_height)

    def move_left(self, window):
        if window.is_maximized():
            print "Maximized window"
            window.unmaximize()
        (width1, height1) = self.screen1_dimension
        (width2, height2) = self.screen2_dimension
        if self._window_screen ==  1:
            new_width = width1/2
            new_height = height1
            newX = 0 
            newY = 0
        else:
            new_width = width2/2
            new_height = height2
            newX = width1
            newY = 0
        print "x: %s, y: %s, width: %s, height: %s" % (newX, newY, new_width, new_height)
        window.set_geometry(0, 255, newX, newY, new_width, new_height)
        
    def move_down(self, window):
        if window.is_maximized():
            print "Maximized window"
            window.unmaximize()
        else:
            (width1, height1) = self.screen1_dimension
            (width2, height2) = self.screen2_dimension
            if self._window_screen ==  1:
                new_width = width1
                new_height = height1/2
                newX = 0
                newY = new_height
            else:
                new_width = width2
                new_height = height2/2
                newX = new_height + width1
                newY = new_height
            print "x: %s, y: %s, width: %s, height: %s" % (newX, newY, new_width, new_height)
            window.set_geometry(0, 255, newX, newY, new_width, new_height)

    def move_up(self, window):
        window.maximize()
        #(width1, height1) = self.screen1_dimension
        #(width2, height2) = self.screen2_dimension
        #if self._window_screen ==  1:
        #    new_width = width1
        #    new_height = height1
        #    newX = 0
        #    newY = 0
        #else:
        #    new_width = width2
        #    new_height = height2
        #    newX = width1+1
        #    newY = 0
        #print "x: %s, y: %s, width: %s, height: %s" % (newX, newY, new_width, new_height)
        #window.set_geometry(0, 255, newX, newY, new_width, new_height)

    def init(self):
        self.screen1_dimension = (1680, 1050)
        self._window_screen = 0
        self.screen2_dimension = (1280, 1024)
        self.screen = wnck.screen_get_default()
        self.ws = WindowState()


    def main(self, direction):
        self.screen.force_update()
        windows = self.screen.get_windows()
        if len(windows) == 0:
            print "No windows found"
            return

        window = self.active_window(windows)
        if window is False:
            print 'Couldnt find active window in: %s' % windows
            return 

        state = self.ws.get_windowstate(window.get_xid())
        print state
        # screen 1 or 2?
        (wX, wY, wWidth, wHeight) = window.get_client_window_geometry()
        print "Window now:\nx: %s, y: %s, width: %s, height: %s" % (wX, wY, wWidth, wHeight)
        if wX < 1680:
            print 'Active window is on screen 1'
            self._window_screen = 1
        else:
            print 'Active window is on screen 2'
            self._window_screen = 2

        move_method = getattr(self, 'move_'+direction)
        print 'Moving window to: %s' % direction
        move_method(window)


if __name__ == '__main__':
    x = Producivity()
    x.init()
    keystr_right = "<Ctrl>Right"
    keybinder.bind(keystr_right, x.main, "right")
    keystr_left = "<Ctrl>Left"
    keybinder.bind(keystr_left, x.main, "left")
    keystr_left = "<Ctrl>Down"
    keybinder.bind(keystr_left, x.main, "down")
    keystr_left = "<Ctrl>Up"
    keybinder.bind(keystr_left, x.main, "up")
    try:
        gtk.main()
    except KeyboardInterrupt, e:
        wnck.wnck_shutdown()
        exit()
