.. _clouds:

Supported Clouds
================

Occopus has an extendible, pluginable architecture for interfacing external
tools and services. The actual version contains 3 different plugin implementations 
for handling clouds.

EC2
---

Occopus can utilise cloud resources supporting the `Amazon Elastic Compute Cloud 
(EC2) interface <https://aws.amazon.com/ec2>`_. This is a general interface, 
however the tool has been tested mainly on `Opennebula clouds <opennebula.org>`_.

Nova
----

Occopus has a backend implementation to interface with `NOVA API
<http://docs.openstack.org>`_. With this interface `OpenStack
<http://www.openstack.org/>`_ type cloud systems
can be utilised.

CloudBroker
-----------

This is special plugin serving resource allocation and program execution on
CloudBroker platform operated by `CloudBroker Inc. <http://cloudbroker.com>`_.
   
