.. _concept:

Concept
=======

OCCOpus is a framework that provides automatic features for configuring and
orchestrating distributed applications on single or multi cloud systems. OCCOpus
can be used by application developers and application controllers to manage
services/infrastructures at deployment time and at runtime as well as to create
and provide complex services/infrastructures to be built by one click even by
novice cloud users (hence from the name OCCOpus).
It has many similarities with HEAT, Juju, etc. Its main advantage that it is
cloud technology neutral, open source and easily extendable. It is also
integrated with CloudBroker Platform (CBP) so users can easily deploy in the
cloud by CBP not only individual cloud services but also complex, interconnected
set of cloud services in every type of clouds that are supported by CBP.
OCCOpus works based on an infrastructure descriptor file that describes the
services to be deployed in the cloud and the order of their deployment. OCCOpus
deploys the services in the cloud according to deployment order specified in the
descriptor file. OCCOpus not only deploys the services but checks their
availability and accessibility before deploying the next service. Furthermore,
the descriptor file can contain contextualization information for every
deployable service and based on that information OCCOpus carries out
contextualization for the deployed services. As a result after contextualization
the services can call each other, i.e. they can collaborate to realize a higher
level service called as virtual infrastructure.
OCCOpus can be used in two different ways:

# Desktop software: In this case virtual infrastructure developers can run
OCCOpus on their desktop machine and they give the service descriptor file as
input to OCCOpus together with their login information to the cloud where they
want to deploy the virtual infrastructure. Based on the descriptor file OCCOpus
deploys and activates the virtual infrastructure in the cloud and then exits.
Then any potential user can use the virtual infrastructure that were built by
OCCOpus in the cloud(s). If the virtual infrastructure developer wants to build
another virtual infrastructure in the cloud they have to run again OCCOpus with
the descriptor file of the new virtual infrastructure as input file.

# Library providing the OCCOpus API: In this case virtual infrastructure
developers create a program that deploys the virtual infrastructure in the cloud
by calling the OCCOpus APIs when it is needed.
It is also planned to create an OCCOpus service that accepts descriptor files
and cloud identifiers and deploys the virtual infrastructure described by the
descriptor files in the identified clouds. It will have the advantage that will
not only deploy the virtual infrastructure but will take care of its monitoring,
self-healing and scale up and down according to its actual load.
In order to enhance the understanding of OCCOpus and its operations, one should
familiarize themselves with a number of founding concepts for OCCOpus. These
concepts are presented here.


