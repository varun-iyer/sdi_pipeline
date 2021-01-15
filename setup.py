from setuptools import setup

setup(
    name="sdi-test-imagepipe",
    version="1.0",
    py_modules=["sdi"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        sdi=sdi:cli
    """,
)
