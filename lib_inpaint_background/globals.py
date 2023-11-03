from modules.shared import opts


class BackgroundGlobals:
    img2img_tab = None
    tab_index = None
    base_image = None
    generated_mask = None
    is_extension_enabled = opts.data.get('inpaint_difference_enabled', True)
    show_image_under_mask = opts.data.get('inpaint_difference_show_image_under_mask', True)
    mask_brush_color = opts.data.get('inpaint_difference_mask_brush_color', '#ffffff')
