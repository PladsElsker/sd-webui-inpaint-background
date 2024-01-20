# sd-webui-inpaint-background
## Overview
A1111 extension that adds a new operation mode in the `img2img` tab. It finds a background mask using rembg.  

## Installation
1) Go to Extensions > Available
2) Click the `Load from:` button
3) Enter "inpaint background" in the search bar
4) Click the `Install` button of the "inpaint background" Tab cell
5) Restart the webui

## Usage
- Go to `img2img` -> `Generation` -> `Inpaint background`
- Upload your `Base image`. The extension will generate a mask as soon as you upload it
- Generate images

> Additional options are added in the inpaint parameters.  
> You can play with them to select the background detection model and configure alpha matting. 
