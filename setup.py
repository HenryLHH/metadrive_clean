from setuptools import setup, find_packages

setup(name='fsrl_metadrive',
      packages=["fsrl_metadrive"],
      include_package_data=True,
      version='0.1.0',
      install_requires=['setuptools<=65.6.3',
                        # 'tianshou==0.5.0',
                        'metadrive-simulator==0.2.6.0'])

