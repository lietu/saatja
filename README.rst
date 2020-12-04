.. image:: https://travis-ci.org/lietu/saatja.svg?branch=master
    :target: https://travis-ci.org/lietu/saatja

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://codecov.io/gh/lietu/saatja/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/lietu/saatja

.. image:: https://img.shields.io/github/issues/lietu/saatja
    :target: https://github.com/lietu/saatja/issues
    :alt: GitHub issues

.. image:: https://img.shields.io/pypi/dm/saatja
    :target: https://pypi.org/project/saatja/
    :alt: PyPI - Downloads

.. image:: https://img.shields.io/pypi/v/saatja
    :target: https://pypi.org/project/saatja/
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/saatja
    :target: https://pypi.org/project/saatja/
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
    :target: https://opensource.org/licenses/BSD-3-Clause

.. code-block::

    🇪🇪 Saatja (Estonian)
    🇺🇸 Sender (English)

    System to deliver webhooks cost-effectively


What is this?
=============

The main goal is to have a tool that can deliver webhooks effectively, ensuring retries are taken care of in case of issues, and cost-efficient deployment.

Primarily intended to be deployed to Google Cloud Run with Google Cloud Scheduler triggering it once per minute, but other deployments may be supported too with some changes.


Google Cloud Run Deployment
---------------------------

This is the primary intended way of deployment. Google Cloud Run is a very cost-efficient way of building scalable web applications as you only pay for CPU time used for processing requests, and it scales automatically. Read more about Google Cloud Run at `https://cloud.google.com/run <https://cloud.google.com/run>`_

You will need the Google Cloud SDK installed for these instructions, but you can perform this manually through the Google Cloud Console as well. Check `https://cloud.google.com/sdk/docs/install <https://cloud.google.com/sdk/docs/install>`_ for installation instructions.

.. code-block:: bash

    gcloud login
    gcloud config set project <your-gcp-project-name>

    # Check https://cloud.google.com/about/locations for regions with Cloud Run support
    gcloud run deploy saatja \
        --image saatja/saatja \
        --region europe-west1 \
        --platform managed \
        --allow-unauthenticated \
        --set-env-vars= "^@^API_KEYS=api,key,list@WEBHOOK_PREFIXES=https://,and,so,on"


Development
-----------

Running locally requires a Google Cloud Firestore emulator running locally in a predictable port. When you have the Google Cloud SDK installed as per instructions above you can run:

.. code-block:: bash

    gcloud components install beta cloud-firestore-emulator

    # then
    ./start_emulator.sh
    # or on Windows
    start_emulator.bat

Then to run Saatja in development mode, you can simply run it with `Poetry <https://python-poetry.org/docs/#installation>`_ as follows:

.. code-block:: bash

    poetry install
    poetry run saatja-dev

To run the unit tests use `Pytest <https://docs.pytest.org/en/stable/>`_:

.. code-block:: bash

    poetry run pytest

Before committing anything make sure you run `pre-commit <https://pre-commit.com>`_ in the repository.

.. code-block:: bash

    pre-commit install

    # If you've done changes before running the above command
    pre-commit run --all-files


License
-------

Licensing is important. This project itself uses BSD 3-clause license, but other libraries used by it may have their own licenses.

For more information check the `LICENSE <https://github.com/lietu/saatja/blob/master/LICENSE>`_ -file.


Contributing
============

This project is run on GitHub using the issue tracking and pull requests here. If you want to contribute, feel free to `submit issues <https://github.com/lietu/saatja/issues>`_ (incl. feature requests) or PRs here.

To test changes locally ``python setup.py develop`` is a good way to run this, and you can ``python setup.py develop --uninstall`` afterwards (you might want to also use the ``--user`` flag).
