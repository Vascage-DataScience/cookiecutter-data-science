packages = [
    "black",
    "flake8",
    "isort",
    "pip",
    "python-dotenv",
]

basic = [
    "ipython",
    "jupyterlab",
    "matplotlib",
    "notebook",
    "numpy",
    "pandas",
    "scikit-learn",
    "holoscan",
    "monai",
    "monai-deploy-app-sdk",
    "monai-generative",
    "nvidia-cublas-cu12",
    "nvidia-cuda-cupti-cu12",
    "nvidia-cuda-nvrtc-cu12",
    "nvidia-cuda-runtime-cu12",
    "nvidia-cudnn-cu12",
    "nvidia-cufft-cu12",
    "nvidia-curand-cu12",
    "nvidia-cusolver-cu12",
    "nvidia-cusparse-cu12",
    "nvidia-ml-py",
    "nvidia-nccl-cu12",
    "nvidia-nvjitlink-cu12",
    "nvidia-nvtx-cu12",
    "scikit-image",
    "scipy",
    "torch",
    "torchvision",
]

scaffold = [
    "typer",
    "loguru",
    "tqdm",
]


def write_dependencies(
    dependencies, packages, pip_only_packages, repo_name, module_name, python_version
):
    if dependencies == "requirements.txt":
        with open(dependencies, "w") as f:
            lines = sorted(packages)

            lines += ["" "-e ."]

            f.write("\n".join(lines))
            f.write("\n")

    elif dependencies == "environment.yml":
        with open(dependencies, "w") as f:
            lines = [
                f"name: {repo_name}",
                "channels:",
                "  - conda-forge",
                "dependencies:",
            ]

            lines += [f"  - python={python_version}"]
            lines += [f"  - {p}" for p in packages if p not in pip_only_packages]

            lines += ["  - pip:"]
            lines += [f"    - {p}" for p in packages if p in pip_only_packages]
            lines += ["    - -e ."]

            f.write("\n".join(lines))

    elif dependencies == "Pipfile":
        with open(dependencies, "w") as f:
            lines = ["[packages]"]
            lines += [f'{p} = "*"' for p in sorted(packages)]

            lines += [f'"{module_name}" ={{editable = true, path = "."}}']

            lines += ["", "[requires]", f'python_version = "{python_version}"']

            f.write("\n".join(lines))
