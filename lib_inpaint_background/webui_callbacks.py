from modules.scripts import script_callbacks
from lib_inpaint_background.settings import create_settings_section
from lib_inpaint_background.ui import InpaintBackgroundTab
from sdwi2iextender import register_operation_mode


def setup_script_callbacks(enabled):
    script_callbacks.on_ui_settings(create_settings_section)
    if enabled:
        register_operation_mode(InpaintBackgroundTab)
