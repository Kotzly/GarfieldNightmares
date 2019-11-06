import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
     name='GarfieldNightmares',  
     version='0.1',
     author="Kotzly",
     author_email="paullo.augusto@hotmail.com",
     description="A Garfield comic generator. Your nightmares coming true.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Kotzly/GarfieldNightmares",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
     python_requires='>=3.6',
     install_requires=required,
 )
