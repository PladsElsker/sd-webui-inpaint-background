import gradio as gr

from modules.shared import opts
from modules.ui_components import FormRow

from lib_inpaint_background.globals import BackgroundGlobals
from lib_inpaint_background.model_choices import models
from lib_inpaint_background.mask_processing import compute_mask


class InpaintBackgroundTab:
    def __init__(self, tab_index: int):
        self.tab_index = tab_index
        BackgroundGlobals.tab_index = tab_index

        self.alpha_mask_row = None
        self.model_dropdown = None
        self.alpha_matting = None
        self.alpha_matting_erode_size = None
        self.alpha_matting_foreground_threshold = None
        self.alpha_matting_background_threshold = None

    def tab(self):
        with gr.TabItem('Inpaint background', id='inpaint_background', elem_id="img2img_inpaint_background_tab") as self.tab:
            with gr.Row():
                BackgroundGlobals.inpaint_img_component = gr.Image(label="Base image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_background")

            BackgroundGlobals.inpaint_mask_component = gr.Image(label="Background mask", interactive=False, type="pil", elem_id="mask_inpaint_background", tool="sketch", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_mask_brush_color)

    def section(self, _):
        with gr.Accordion(label='Inpaint background', open=False, visible=False) as self.ui_params:
            with FormRow():
                self.model_dropdown = gr.Dropdown(choices=models, value="u2net", show_label=False)
                self.alpha_matting = gr.Checkbox(label="Alpha matting", value=False)

            with FormRow(visible=False) as self.alpha_mask_row:
                self.alpha_matting_erode_size = gr.Slider(label="Erode size", minimum=0, maximum=40, step=1, value=10)
                self.alpha_matting_foreground_threshold = gr.Slider(label="Foreground threshold", minimum=0, maximum=255, step=1, value=240)
                self.alpha_matting_background_threshold = gr.Slider(label="Background threshold", minimum=0, maximum=255, step=1, value=10)

    def gradio_events(self, img2img_tabs: list):
        self._compute_mask_and_alpha_matting_params()
        self._additional_params_visibility(img2img_tabs)

    def _compute_mask_and_alpha_matting_params(self):
        params = {
            'fn': compute_mask,
            'inputs': [
                BackgroundGlobals.inpaint_img_component,
                self.model_dropdown,
                self.alpha_matting,
                self.alpha_matting_erode_size,
                self.alpha_matting_foreground_threshold,
                self.alpha_matting_background_threshold,
            ],
            'outputs': [
                BackgroundGlobals.inpaint_mask_component,
                self.alpha_mask_row
            ]
        }

        BackgroundGlobals.inpaint_img_component.upload(**params)
        BackgroundGlobals.inpaint_img_component.clear(**params)
        self.model_dropdown.change(**params)
        self.alpha_matting.change(**params)
        self.alpha_matting_erode_size.release(**params)
        self.alpha_matting_foreground_threshold.release(**params)
        self.alpha_matting_background_threshold.release(**params)

    def _additional_params_visibility(self, img2img_tabs):
        for i, tab in enumerate(img2img_tabs):
            tab.select(
                fn=lambda is_shown: gr.update(visible=is_shown),
                inputs=[gr.State(i == self.tab_index)],
                outputs=[self.ui_params]
            )
