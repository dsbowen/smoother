import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smoother",
    version="0.0.3",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="Computes non-parametric distributions by optizing a constrained smoothing function",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsbowen/smoother",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.19.1',
        'scipy>=1.5.2'
    ]
)