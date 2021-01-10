import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="numeric_sets_dyaroshevych",  # Replace with your own username
    version="0.0.1",
    author="Dmytro Yaroshevych",
    author_email="dyaroshevych@gmail.com",
    description="A package for performing operations on numeric sets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dyaroshevych/numeric_sets",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    packages=["numeric_sets"],
    package_dir={"numeric_sets": "numeric_sets"},
)
