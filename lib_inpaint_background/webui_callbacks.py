from modules.scripts import script_callbacks

from lib_inpaint_background.globals import BackgroundGlobals
from lib_inpaint_background.settings import create_settings_section
from lib_inpaint_background.ui import create_inpaint_background_tab, inject_inpaint_background_generation_params_ui
from lib_inpaint_background.webui_nasty_hijacks import hijack_generation_params_ui, register_tabitem_to_tab_list


def on_before_component(_, **kwargs):
    if not BackgroundGlobals.is_extension_enabled:
        return

    elem_id = kwargs.get('elem_id', None)

    if elem_id == 'img2img_batch_inpaint_mask_dir':
        tab_inpaint_background = create_inpaint_background_tab()
        BackgroundGlobals.img2img_tab = tab_inpaint_background

    if elem_id == 'img2img_mask_alpha':
        inject_inpaint_background_generation_params_ui()

    if elem_id == 'img2img_inpaint_full_res':
        register_tabitem_to_tab_list()
        hijack_generation_params_ui()


def on_ui_settings():
    create_settings_section()


def setup_script_callbacks():
    script_callbacks.on_before_component(on_before_component)
    script_callbacks.on_ui_settings(on_ui_settings)
