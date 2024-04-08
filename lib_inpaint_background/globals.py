from modules.shared import opts


class BackgroundGlobals:
    is_extension_enabled = opts.data.get('inpaint_background_enabled', True)
    show_image_under_mask = opts.data.get('inpaint_background_show_image_under_mask', True)
    mask_brush_color = opts.data.get('inpaint_background_mask_brush_color', '#ffffff')

    rembg_model_string = None
    rembg_session = None
