from lib_inpaint_background.globals import BackgroundGlobals
from lib_inpaint_background.webui_nasty_hijacks import hijack_img2img_processing
from lib_inpaint_background.webui_callbacks import setup_script_callbacks


if BackgroundGlobals.is_extension_enabled:
    hijack_img2img_processing()

setup_script_callbacks()
