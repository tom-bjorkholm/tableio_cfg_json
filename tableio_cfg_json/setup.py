#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup  # type: ignore[import-untyped]

setup(
  name='tableio-cfg-json', version='1.1.1',
  description='config-as-json configuration encapsulation for tableio.',
  author='Tom Björkholm', author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12', packages=['tableio_cfg_json'],
  package_dir={'tableio_cfg_json': 'src/tableio_cfg_json'},
  package_data={'tableio_cfg_json': ['py.typed', '*.pyi']},
  install_requires=[
    'tableio >= 1.1',
    'config-as-json >= 1.4',
    'wizard-ui-bridge[textual] >= 1.1.1',
  ])
