#define _GNU_SOURCE
#include <gtk/gtk.h>
#include <gmodule.h>

/*
 * gtk_popup_rgba: GTK3 Module
 * Ensures GtkMenu and popup windows request an RGBA (32-bit depth) visual
 * instead of the default 24-bit system visual on X11 composited screens.
 * This allows client-side rounded corners (border-radius) to render with
 * true alpha transparency without pitch-black corner artifacts.
 */

static void (*orig_window_realize)(GtkWidget *widget) = NULL;

static void popup_window_realize(GtkWidget *widget) {
    if (GTK_IS_WINDOW(widget)) {
        GtkWindow *win = GTK_WINDOW(widget);
        if (gtk_window_get_window_type(win) == GTK_WINDOW_POPUP) {
            GdkScreen *screen = gtk_widget_get_screen(widget);
            if (screen && gdk_screen_is_composited(screen)) {
                GdkVisual *rgba = gdk_screen_get_rgba_visual(screen);
                if (rgba) {
                    gtk_widget_set_visual(widget, rgba);
                }
            }
        }
    }
    if (orig_window_realize) {
        orig_window_realize(widget);
    }
}

static void install_hook(void) {
    if (!orig_window_realize) {
        GtkWidgetClass *wclass = GTK_WIDGET_CLASS(g_type_class_ref(GTK_TYPE_WINDOW));
        orig_window_realize = wclass->realize;
        wclass->realize = popup_window_realize;
    }
}

G_MODULE_EXPORT void gtk_module_init(gint *argc, gchar ***argv[]) {
    install_hook();
}

G_MODULE_EXPORT void gtk_module_display_init(GdkDisplay *display) {
    install_hook();
}

__attribute__((constructor))
static void ctor(void) {
    install_hook();
}
