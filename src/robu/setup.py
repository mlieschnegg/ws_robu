from setuptools import setup

package_name = 'robu'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='michael.lieschnegg',
    maintainer_email='lieschnegg@lilatec.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'helloworld = robu.helloworld:main',
            'remotectrl = robu.remotectrl:main',
            'remotectrl_listener = robu.remotectrl_listener:main',
            'remotectrl_sus = robu.remotectrl_sus:main'
        ],
    },
)
