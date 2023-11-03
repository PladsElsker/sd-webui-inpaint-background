import gradio as gr

from modules.shared import opts
from modules.ui_components import FormRow

from lib_inpaint_background.globals import BackgroundGlobals
from lib_inpaint_background.context_pack import ParentBlock
from lib_inpaint_background.model_choices import models
from lib_inpaint_background.mask_processing import compute_mask


def create_inpaint_background_tab():
    with ParentBlock():
        with gr.TabItem('Inpaint background', id='inpaint_background', elem_id="img2img_inpaint_background_tab") as tab_inpaint_background:
            with gr.Row():
                BackgroundGlobals.inpaint_img_component = gr.Image(label="Base image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_background")

            BackgroundGlobals.inpaint_mask_component = gr.Image(label="Background mask", interactive=False, type="pil", elem_id="mask_inpaint_background", tool="sketch", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_mask_brush_color)

    return tab_inpaint_background


def inject_inpaint_background_generation_params_ui():
    with ParentBlock():
        with gr.Tab(label='Rembg parameters') as inpaint_background_params:
            with FormRow():
                model_dropdown = gr.Dropdown(choices=models, value="u2net", show_label=False)
                alpha_matting = gr.Checkbox(label="Alpha matting", value=False)

            with FormRow(visible=False) as alpha_mask_row:
                alpha_matting_erode_size = gr.Slider(label="Erode size", minimum=0, maximum=40, step=1, value=10)
                alpha_matting_foreground_threshold = gr.Slider(label="Foreground threshold", minimum=0, maximum=255, step=1, value=240)
                alpha_matting_background_threshold = gr.Slider(label="Background threshold", minimum=0, maximum=255, step=1, value=10)

            alpha_matting.change(
                fn=lambda x: gr.update(visible=x),
                inputs=[alpha_matting],
                outputs=[alpha_mask_row],
            )

    params = {
        'fn': compute_mask,
        'inputs': [
            BackgroundGlobals.inpaint_img_component,
            model_dropdown,
            alpha_matting,
            alpha_matting_erode_size,
            alpha_matting_foreground_threshold,
            alpha_matting_background_threshold,
        ],
        'outputs': [BackgroundGlobals.inpaint_mask_component]
    }

    BackgroundGlobals.inpaint_img_component.upload(**params)
    BackgroundGlobals.inpaint_img_component.clear(**params)

    BackgroundGlobals.ui_params = inpaint_background_params,
