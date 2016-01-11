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

OCCI
----
Occopus can use OCCI-enabled cloud providers of the 'EGI Federated Cloud
<https://www.egi.eu/infrastructure/cloud/>'_. For this, one must possess an X.509
certificate accepted within the FedCloud VO.

CloudBroker
-----------

This is special plugin serving resource allocation and program execution on
CloudBroker platform operated by `CloudBroker Inc. <http://cloudbroker.com>`_.

Using the CloudBroker plugin you can access all the different cloud types that are supported by
CloudBroker platform. These are:

- Amazon
- CloudSigma
- OpenStack
- OpenNebula

If you want to use clouds via the  CloudBroker platform, please, contact the CloudBroker GmbH:

- Email: info@cloudbroker.com
- Phone: +41 44 515 21 70
- Web: http://www.cloudbroker.com
   
