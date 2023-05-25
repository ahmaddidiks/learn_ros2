from setuptools import setup

package_name = 'turtlesim_challenge'

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
    maintainer='didik',
    maintainer_email='adidiksetiyadi@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "turtlesim_controller = turtlesim_challenge.turtle_controller:main",
            "turtle_spawner = turtlesim_challenge.turtle_spawner:main"
        ],
    },
)
