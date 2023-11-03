(() => {
    const INPAINT_DIFFERENCE_POLLING_TIMEOUT = 500;

    document.addEventListener("DOMContentLoaded", () => {
        onInpaintDifferenceTabLoaded(setupCenterStyle);
    });


    function onInpaintDifferenceTabLoaded(callback) {
        const swapButton = getSwapButton();
        if (swapButton === null) {
            setTimeout(() => { onInpaintDifferenceTabLoaded(callback); }, INPAINT_DIFFERENCE_POLLING_TIMEOUT);
            return;
        }

        callback();
    }


    function setupCenterStyle() {
        const swapButton = getSwapButton();
        const form = swapButton.parentElement;
        form.style.position = 'relative';
        form.style.flexGrow = '0';
        form.style.padding = '10px';
    }


    function getSwapButton() {
        return document.querySelector('#img2img_inpaint_difference_swap_images');
    }
})();