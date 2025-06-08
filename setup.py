from setuptools import setup, find_packages

setup(
    name="thompson-transcription",
    version="0.1.0",
    packages=find_packages(where="scripts"),
    package_dir={"": "scripts"},
    install_requires=[
        "opencv-python-headless==4.11.*",
        "opencv-contrib-python==4.11.*",
        "numpy==1.26.*",
        "scikit-image==0.23.*",
        "pillow==10.*",
        "kraken==3.*",
        "pyyaml==6.*",
        "tqdm==4.*",
        "pandas==2.*",
        "wandb",
    ],
    extras_require={
        "dev": ["pytest==7.*", "black==23.*", "flake8==6.*"],
    },
    python_requires=">=3.9",
)
