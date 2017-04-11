from setuptools import setup


setup(name='ladypy',
      version='alpha',
      description='Python library for simulating models of Language Dynamics',
      long_description='',
      classifiers=[],
      keywords=[],
      url='https://github.com/PluVian/ladypy',
      author='PluVian',
      author_email='urisa12@gmail.com',
      license='MIT',
      packages=['ladypy'],
      install_requires=[
          'numpy',
          'tqdm',
      ],
      include_package_data=True,
      zip_safe=False)
