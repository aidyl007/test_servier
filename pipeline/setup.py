import setuptools # type: ignore

setuptools.setup(
    name='SERVIER-PACKAGE',
    version='0.1',
    install_requires=["google-cloud-storage==2.18.2"],
    packages=setuptools.find_packages(),
)