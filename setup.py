from setuptools import find_packages, setup  # type: ignore

setup(
    name='pathobj_handler',
    version='1.0.0',
    description='',
    description_content_type='',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/toritamantaro/path-object-handler',
    author='toritamantaro',
    # packages=find_packages(),
    python_requires='>=3.8',
    # include_package_data=True,
    license='MIT',
    install_requires=[ # requirements.txtに記述し読込でも良
        # 'PyYAML==5.4.1',
        'python-dateutil',
    ],
)