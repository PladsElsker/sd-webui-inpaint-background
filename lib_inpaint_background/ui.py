import gradio as gr

from modules.shared import opts
from modules.ui_components import FormRow

from lib_inpaint_background.model_choices import models
from lib_inpaint_background.mask_processing import compute_mask, compute_mask_blur_only


class InpaintBackgroundTab:
    requested_elem_ids = ["img2img_mask_blur"]

    def __init__(self):
        self.inpaint_img_component = None
        self.inpaint_mask_component = None
        self.inpaint_visual_mask_component = None
        self.alpha_mask_row = None
        self.model_dropdown = None
        self.alpha_matting = None
        self.alpha_matting_erode_size = None
        self.alpha_matting_foreground_threshold = None
        self.alpha_matting_background_threshold = None

    def image_components(self):
        self.inpaint_img_component = gr.Image(label="Base image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_background")
        self.inpaint_img_component.unrender()
        self.inpaint_mask_component = gr.Image(visible=False, label="Altered image", interactive=True, type="pil", elem_id="mask_inpaint_background")
        return self.inpaint_img_component, self.inpaint_mask_component

    def tab(self):
        with gr.TabItem('Inpaint background', id='inpaint_background', elem_id="img2img_inpaint_background_tab") as self.tab:
            with gr.Row():
                self.inpaint_img_component.render()
            
            self.inpaint_visual_mask_component = gr.Image(label="Background mask", interactive=False, type="pil", elem_id="mask_inpaint_background", tool="sketch", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_mask_brush_color)

    def section(self, components):
        self.img2img_mask_blur = components["img2img_mask_blur"]

        with gr.Accordion(label='Inpaint background', open=False, visible=False) as self.ui_params:
            with FormRow():
                self.model_dropdown = gr.Dropdown(choices=models, value="u2net", show_label=False)
                self.alpha_matting = gr.Checkbox(label="Alpha matting", value=False)

            with FormRow(visible=False) as self.alpha_mask_row:
                self.alpha_matting_erode_size = gr.Slider(label="Erode size", minimum=0, maximum=40, step=1, value=10)
                self.alpha_matting_foreground_threshold = gr.Slider(label="Foreground threshold", minimum=0, maximum=255, step=1, value=240)
                self.alpha_matting_background_threshold = gr.Slider(label="Background threshold", minimum=0, maximum=255, step=1, value=10)

    def gradio_events(self, selected: gr.Checkbox):
        self._compute_mask_and_alpha_matting_params()
        self._compute_mask_blur_only()
        self._additional_params_visibility(selected)

    def _compute_mask_and_alpha_matting_params(self):
        params = dict(
            fn=compute_mask,
            inputs=[
                self.inpaint_img_component,
                self.model_dropdown,
                self.alpha_matting,
                self.alpha_matting_erode_size,
                self.alpha_matting_foreground_threshold,
                self.alpha_matting_background_threshold,
                self.img2img_mask_blur,
            ],
            outputs=[
                self.inpaint_mask_component,
                self.inpaint_visual_mask_component,
                self.alpha_mask_row,
            ],
        )

        self.inpaint_img_component.upload(**params)
        self.inpaint_img_component.clear(**params)
        self.model_dropdown.change(**params)
        self.alpha_matting.change(**params)
        self.alpha_matting_erode_size.release(**params)
        self.alpha_matting_foreground_threshold.release(**params)
        self.alpha_matting_background_threshold.release(**params)

    def _compute_mask_blur_only(self):
        params = dict(
            fn=compute_mask_blur_only,
            inputs=[
                self.inpaint_img_component, 
                self.img2img_mask_blur,
            ],
            outputs=[
                self.inpaint_visual_mask_component,
            ],
        )

        self.img2img_mask_blur.release(**params)

    def _additional_params_visibility(self, selected: gr.Checkbox):
        selected.change(
            fn=lambda is_shown: gr.update(visible=is_shown),
            inputs=[selected],
            outputs=[self.ui_params]
        )
