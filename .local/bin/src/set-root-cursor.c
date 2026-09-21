#include <X11/Xlib.h>
#include <X11/Xcursor/Xcursor.h>

int main() {
    Display *dpy = XOpenDisplay(NULL);
    if (!dpy) return 1;
    Cursor c = XcursorLibraryLoadCursor(dpy, "left_ptr");
    XDefineCursor(dpy, DefaultRootWindow(dpy), c);
    XFlush(dpy);
    XCloseDisplay(dpy);
    return 0;
}
