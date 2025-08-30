from setuptools import setup, find_packages

setup(
    name="network-analysis-package",
    version="0.1.0",
    author="Hua Cheng",
    description="A package for analyzing neural network structures and connections",
    long_description=open("README.md").read() if open("README.md").read() else "A package for analyzing neural network structures and connections",
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/network-analysis-package",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "analyze-networks=network_analysis_package.analysis:main",
        ],
    },
)