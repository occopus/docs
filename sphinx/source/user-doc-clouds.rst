.. _user-doc-clouds:

Supported Resources
===================

Occopus has an extendible, pluginable architecture for interfacing external
tools and services. The actual version contains four different resource plugin implementations for handling clouds and one for docker containers.

EC2
---

Occopus can utilise cloud resources supporting the `Amazon Elastic Compute Cloud (EC2) interface <https://aws.amazon.com/ec2>`_.

Nova
----

Occopus has a resource plugin to interface with `NOVA API
<http://docs.openstack.org>`_. With this interface `OpenStack
<http://www.openstack.org/>`_ type cloud systems can be utilised.

Azure
-----

The Azure and Azure ACI resource plugins of Occopus enables the usage of `Azure <https://azure.microsoft.com//>`_ resources.

CloudBroker
-----------

This is a special resource plugin serving resource allocation and program execution on CloudBroker platform operated by `CloudBroker Inc. <http://cloudbroker.com>`_.

Using the CloudBroker plugin you can access all the different cloud types that are supported by
CloudBroker platform. These are:

- Amazon
- CloudSigma
- OpenStack
- OpenNebula

If you want to use clouds via the  CloudBroker platform, please, contact the CloudBroker GmbH:

- Email: info@cloudbroker.com
- Web: http://www.cloudbroker.com

Docker
------

Occopus has a resource plugin which enables to utilise
pure `Docker <http://www.docker.com>`_ or `Swarm <https://docs.docker.com/engine/swarm/>`_ resources. With this plugin it is possible to deploy containers and to combine them into an infrastructure.

CloudSigma
----------

The CloudSigma resource plugin of Occopus enables the usage of `CloudSigma <https://www.cloudsigma.com/>`_ resources.

