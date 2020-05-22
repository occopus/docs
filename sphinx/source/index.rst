Introduction
############

This document is envisaged to introduce the abilities of Occopus, a cloud orchestrator
framework developed at SZTAKI (Hungary) to create and manage flexible computing
infrastructures and services in a single or multi cloud system.

.. sidebar:: How to start?

   Get started in minutes.
   Follow the :ref:`installation` guide!

What is Occopus?
****************

Occopus is an easy-to-use hybrid cloud orchestration tool. It is a framework that provides features
for configuring and orchestrating distributed applications (so called virtual infrastructures) on
single or multi cloud systems. Occopus can be used by application developers and devops to create
and deploy complex virtual infrastructures as well as to manage them at deployment time and at runtime.


.. figure:: images/logo/occo_licence.png
    :align: right

**If you use Occopus, please cite at least one of the following publications:**

* Kovács, J. & Kacsuk, P. Occopus: a Multi-Cloud Orchestrator to Deploy and Manage Complex Scientific Infrastructures J Grid Computing (2018) 16: 19. https://doi.org/10.1007/s10723-017-9421-3
* Lovas, R ; Nagy, E ; Kovacs, J Cloud agnostic Big Data platform focusing on scalability and cost-efficiency ADVANCES IN ENGINEERING SOFTWARE 125 pp. 167-177. , 11 p. (2018) http://dx.doi.org/10.1016%2Fj.advengsoft.2018.05.002
* József Kovács, Péter Kacsuk, Márk Emődi, Deploying Docker Swarm cluster on hybrid clouds using Occopus, Advances in Engineering Software, Volume 125, 2018, Pages 136-145, ISSN 0965-9978, https://doi.org/10.1016/j.advengsoft.2018.08.001.
* Kacsuk, P., Kovács, J. & Farkas, Z. The Flowbster Cloud-Oriented Workflow System to Process Large Scientific Data Sets J Grid Computing (2018) 16: 55. https://doi.org/10.1007/s10723-017-9420-4
* Lovas, R ; Farkas, A ; Marosi, A Cs ; Acs, S ; Kovacs, J ; Szaloki, A ; Kadar, B Orchestrated Platform for Cyber-Physical Systems COMPLEXITY 2018 pp. 1-16. Paper: 8281079 , 16 p. (2018) http://dx.doi.org/10.1155%2F2018%2F8281079

.. toctree::
   :maxdepth: 4
   :caption: User guide

   user-doc-concept.rst
   user-doc-features.rst
   user-doc-clouds.rst
   user-doc-setup.rst
   user-doc-createinfra.rst
   user-doc-api-user.rst
   user-doc-release_notes.rst
   user-doc-contact.rst


.. toctree::
   :maxdepth: 3
   :caption: Tutorials

   tutorial-resource-plugins
   tutorial-configmanager-plugins
   tutorial-building-clusters
   tutorial-autoscaling-infrastructures
   tutorial-flowbster
   tutorial-bigdata-ai

.. toctree::
   :maxdepth: 3
   :caption: Developer guide

   dev-doc-packages.rst
   dev-doc-api.rst
   dev-docs.rst