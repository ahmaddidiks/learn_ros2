from setuptools import setup

package_name = 'py_pkg'

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
    maintainer_email='didik@student.undip.ac.id',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "py_node = py_pkg.first_py_node:main",
            "robot_news_station = py_pkg.robot_news_station:main",
            "smartphone = py_pkg.smartphone:main"
        ],
    },
)
