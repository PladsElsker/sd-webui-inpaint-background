import launch


if not launch.is_installed('onnxruntime') and not launch.is_installed('onnxruntime-gpu'):
    # with older versions of a webui you need to check for both cpu and gpu onnxruntime otherwise it will fail to detect it properly
    import torch.cuda as cuda
    # torch imported here only when necessary, importing it at the beginning would immediately slow down load time
    if cuda.is_available():
        launch.run_pip('install onnxruntime-gpu')
    else:
        launch.run_pip('install onnxruntime')

pip_dependencies = [
    'rembg==2.0.38 --no-deps',
    'pymatting',
    'pooch'
]

for dependency in pip_dependencies:
    if '==' in dependency:
        dependency_no_version = dependency[:dependency.index('=')]
    else:
        dependency_no_version = dependency
    if not launch.is_installed(dependency_no_version):
        launch.run_pip(f"install {dependency}", f"{dependency} for sd-webui-inpaint-background")


if not launch.is_installed('sdwi2iextender'):
    launch.run_pip(f'install sdwi2iextender', f"sdwi2iextender for sd-webui-inpaint-background")
