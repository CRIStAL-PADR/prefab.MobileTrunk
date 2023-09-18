from setuptools import setup

package_name = 'keyboard_trunk_controller'

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
    maintainer='speed',
    maintainer_email='speed@pretil.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'keyboard_controller = keyboard_trunk_controller.keyboard_controller:main', 
        'set_position_to_float64_converter = keyboard_trunk_controller.set_position_to_float64_converter:main' 
        ],
},
)
