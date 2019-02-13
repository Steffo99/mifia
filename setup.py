import setuptools

with open("README.md", "r") as file:
    readme = file.read()

setuptools.setup(
    name="mifia",
    version="0.0.1",
    author="Stefano Pigozzi",
    author_email="ste.pigozzi@gmail.com",
    description="A package to run Mafia and similar games with Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Steffo99/thats-how-mifia-works",
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires="~=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ]
)
