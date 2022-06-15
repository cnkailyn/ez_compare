import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ez_compare",
    version="0.1",
    author="kailyn",
    author_email="cnkailyn@gmail.com",
    description="Easily to compare two text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cnkailyn/ez_compare",
    packages=setuptools.find_packages(),
    install_requires=['diff_match_patch==20200713'],
)
