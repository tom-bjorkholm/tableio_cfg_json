#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup  # type: ignore[import-untyped]

setup(
  name='wizard-ui-bridge', version='1.1',
  description='User interface bridge for wizards asking a user questions.',
  author='Tom Björkholm', author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12', packages=['wizard_ui_bridge'],
  package_dir={'wizard_ui_bridge': 'src/wizard_ui_bridge'},
  package_data={'wizard_ui_bridge': ['py.typed']},
  install_requires=[
    'config-as-json >= 1.4',
  ],
  extras_require={'textual': ['textual >= 8.2.8']})
