import launch


pip_dependencies = [
    'rembg==2.0.38 --no-deps',
    'onnxruntime',
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
