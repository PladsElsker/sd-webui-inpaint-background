from modules.shared import opts, OptionInfo
from modules import ui_components

from lib_inpaint_background.globals import BackgroundGlobals


def create_settings_section():
    section = ('inpaint_background', 'Inpaint Background')

    opts.add_option('inpaint_background_enabled', OptionInfo(True, 'Enable inpaint-background extension', section=section).needs_restart())
    opts.add_option('inpaint_background_show_image_under_mask', OptionInfo(True, 'Display the altered image under the mask', section=section))
    opts.add_option('inpaint_background_mask_brush_color', OptionInfo('#ffffff', 'Inpaint background brush color', ui_components.FormColorPicker, {}, section=section).info('brush color of inpaint background mask'))

    update_global_settings()


def update_global_settings():
    BackgroundGlobals.is_extension_enabled = opts.data.get('inpaint_background_enabled', True)
    BackgroundGlobals.show_image_under_mask = opts.data.get('inpaint_background_show_image_under_mask', True)
    BackgroundGlobals.mask_brush_color = opts.data.get('inpaint_background_mask_brush_color', '#ffffff')

    def image_under_mask_visibility_changed():
        BackgroundGlobals.show_image_under_mask = opts.data.get('inpaint_background_show_image_under_mask', True)

    def mask_brush_color_changed():
        BackgroundGlobals.mask_brush_color = opts.data.get('inpaint_background_mask_brush_color', '#ffffff')

    opts.onchange('inpaint_background_show_image_under_mask', image_under_mask_visibility_changed)
    opts.onchange('inpaint_background_mask_brush_color', mask_brush_color_changed)