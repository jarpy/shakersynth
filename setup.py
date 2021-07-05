import setuptools  # type: ignore

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="Shakersynth",
    version="0.7.0",
    author="Toby McLaughlin",
    author_email="toby@jarpy.net",
    description="Bass shaker synthesizer for DCS World.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jarpy/shakersynth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
    ],
    python_requires='>=3.7',
    install_requires=[
        'func-timeout',
        'python-configuration[yaml]',
        'pyo',
        'pyaml',
        'wxPython',
    ],
    scripts=['bin/shakersynth.bat'],
    package_data={'': ['Shakersynth.lua']},
    include_package_data=True,
)
