import setuptools
from setuptools_behave import behave_test

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colorgrade",
    version="0.0.1",
    author="Alexey Kuznetsov",
    author_email="kuznecov.alexey@gmail.com",
    description="Conditional formatting for terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrsmith/colorgrade",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    entry_points={"console_scripts": ["colorgrade=colorgrade:main", "colorgrade_test=colorgrade:test_color_scaler",],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["colorful>=0.5.4", "colour>=0.1.5",],
    tests_require=["behave>=1.2.6", "flake8>=3.7.8", "pyhamcrest>=2.0.2", "pytest>=5.2.0",],
    setup_requires=["pytest-runner",],
    cmdclass={"behave_test": behave_test,},
)
