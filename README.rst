============
Metabase VCS
============


.. image:: https://img.shields.io/pypi/v/metabase_vcs.svg
        :target: https://pypi.python.org/pypi/metabase_vcs

.. image:: https://img.shields.io/travis/techindicium/metabase_vcs.svg
        :target: https://travis-ci.com/techindicium/metabase_vcs

.. image:: https://readthedocs.org/projects/metabase-vcs/badge/?version=latest
        :target: https://metabase-vcs.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




An attempt to serialize and keep dashboards in a VCS such as git


* Free software: Apache Software License 2.0
* Documentation: https://metabase-vcs.readthedocs.io.


Tracking Metabase Dashboards
---------------------------------------
So far metabase_vcs will only track dashboards, and this dashboards needs
to be declared at the tracked_dashboards.json file at the root of your repo

example of a tracked_dashboards.json file:

.. code-block::
        {
        "dashboards": [
                {
                        "name": "dashboard_one", # this will be the name of the json file exported
                        "id": 147   # the metabase dashboard id
                },
                {
                        "name": "dashboard_two",
                        "id": 166
                }
                ]
        }


Create a 'dashboards' dir at the root of your repo
then run


.. code-block::
        metabase_vcs export-metabase


This script will create json files represeting dashboards at
this dashboards dir

Then you can change a tracked dashboard, run the export-metabase again and
check the diffs

.. code-block::
        git diff dashboards/



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
