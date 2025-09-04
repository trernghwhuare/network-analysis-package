from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setup(
    name="network-analysis-package",
    version="0.1.0",
    author="Hua Cheng",
    author_email="trernghwhuare@aliyun.com",
    description="A package for analyzing neural network structures and connection ratios",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/network-analysis-package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'network-analysis=network_analysis_package.conn_ratio:main',
        ],
    },
)