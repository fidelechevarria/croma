import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="croma",
    version="0.0.3",
    author="Fidel Echevarria Corrales",
    author_email="fidel.echevarria.corrales@gmail.com",
    description="A simple scientific visualization library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fidelechevarria/croma",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'vtk',
        # 'plotly',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='visualization animation graphics 3D',
    license='MIT',
    python_requires='>=3.6',
)