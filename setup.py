from setuptools import setup

setup(
    name="sdi",
    version="0.90",
    py_modules=["sdi", "openfits", "__main__"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        sdi=__main__:cli
    """,
)
