from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="aiconclave",
    version="0.1.1",
    author="Arpit Sengar (arpy8)",
    author_email="arpitsengar99@gmail.com",
    description="This package contains the python scripts for the AI conclave exhibition.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arpy8/aiconclave",
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "tqdm",
        "termcolor",
        "opencv-python",
        "mediapipe",
        "pygame",
        "pyautogui",
        "pydirectinput",
        "customtkinter",
        "streamlit",
        "streamlit-option-menu",
    ],
    entry_points={
        "console_scripts": [
            "aiconclave=aiconclave.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'aiconclave': ['assets/chrome_dino/jump.mp3', 'assets/config.json', 'assets/tekken/TekkenGame.exe']},
    include_package_data=True,
    license="MIT"
)