import rembg
import gradio as gr
import numpy as np
import cv2
from PIL import Image

from lib_inpaint_background.globals import BackgroundGlobals


def compute_mask(
    base_img_pil,
    model_str,
    alpha_matting_enabled,
    alpha_matting_erode_size,
    alpha_matting_foreground_threshold,
    alpha_matting_background_threshold,
    img2img_mask_blur,
):
    if base_img_pil is None:
        return None, None, gr.update(visible=alpha_matting_enabled)

    base_img = np.array(base_img_pil)
    mask = compute_mask_rembg(
        base_img, model_str,
        alpha_matting=alpha_matting_enabled,
        alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
        alpha_matting_background_threshold=alpha_matting_background_threshold,
        alpha_matting_erode_size=alpha_matting_erode_size,
    )
    blurred_mask = blur(mask, img2img_mask_blur)
    visual_mask = colorize(blurred_mask)
    if BackgroundGlobals.show_image_under_mask:
        visual_mask = add_image_under_mask(blurred_mask, visual_mask, np.array(base_img).astype(np.int32))

    return Image.fromarray(mask.astype(np.uint8), mode=base_img_pil.mode), Image.fromarray(visual_mask.astype(np.uint8), mode=base_img_pil.mode), gr.update(visible=alpha_matting_enabled)


def compute_mask_blur_only(
    base_img,
    mask_img,
    img2img_mask_blur,
):
    if mask_img is None:
        return None

    mask = np.array(mask_img)
    blurred_mask = blur(mask, img2img_mask_blur)
    visual_mask = colorize(blurred_mask)
    if BackgroundGlobals.show_image_under_mask:
        visual_mask = add_image_under_mask(blurred_mask, visual_mask, np.array(base_img).astype(np.int32))

    return Image.fromarray(visual_mask.astype(np.uint8), mode=base_img.mode)


def compute_mask_rembg(base_img, model_str, **kwargs):
    if model_str == "None":
        BackgroundGlobals.rembg_model_string = model_str
        BackgroundGlobals.rembg_session = None
        return np.zeros_like(base_img)
    
    if BackgroundGlobals.rembg_model_string != model_str:
        BackgroundGlobals.rembg_model_string = model_str
        BackgroundGlobals.rembg_session = rembg.new_session(model_str, providers=['CPUExecutionProvider'])
    
    kwargs["session"] = BackgroundGlobals.rembg_session

    mask = np.array(rembg.remove(Image.fromarray(base_img), **kwargs).getchannel("A"))
    mask = 255 - mask
    return np.stack((mask, mask, mask), axis=-1)


def colorize(mask):
    color_str = BackgroundGlobals.mask_brush_color
    color = np.array([int(color_str[i:i+2], 16)/255 for i in range(1, 7, 2)])
    return mask * color


def add_image_under_mask(original_mask, colorized_mask, base, t=1):
    normalized_mask = original_mask / 255
    opacity_mask = (base*(1-t) + colorized_mask*t)
    return base*(1-normalized_mask) + opacity_mask*normalized_mask


# similar to how StableDiffusionProcessingImg2Img does it
def blur(mask, blur_amount):
    np_mask = np.array(mask)
    kernel_size = 2 * int(2.5 * blur_amount + 0.5) + 1
    return cv2.GaussianBlur(np_mask, (kernel_size, kernel_size), blur_amount)
