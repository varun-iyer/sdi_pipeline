from setuptools import setup, find_packages

setup(
    name="sdi",
    version="0.91",
    py_modules=["sdi", "openfits"],
    packages=find_packages(include=["openfits"]),
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        sdi=sdi:cli
    """,
)
