# sd-webui-inpaint-difference
## Overview
An A1111 extension to add a new operation mode in the `img2img` tab. It finds the inpaint mask to use based on the difference between two images.  

## Installation
- Go to `extensions` > `Install from URL` in the webui
- Paste
```
https://github.com/John-WL/sd-webui-inpaint-difference
```
in the `URL for extension's git repository` textbox
- Click the `Install` button
- Restart the Webui

## How to use
1) Get your image.
2) Modify it in your favorite illustration software.
3) Upload your initial image in the `Base image`, and upload the modified image in the `Altered image`.
4) Once both images are uploaded, the `Generated mask` will appear.
5) You're done! When clicking the `Generate` button, the operation mode will use the `Altered image` and the `Generated mask` to inpaint the image like you would normally expect with the other operation modes.

> Additional parameters are added under the operation mode as well to edit the mask. You can also look into the settings for the brush color and other options like that. 

