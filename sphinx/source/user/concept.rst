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
cloud technology neutral, open source and easily extendable. OCCOpus works based 
on an infrastructure description that describes the services to be deployed in 
the cloud and the order of their deployment. OCCOpus deploys the services in 
the cloud according to deployment order specified in the
description. 

OCCOpus not only deploys the services but checks their
availability and accessibility before deploying the next service. Furthermore,
the description can contain contextualization information for every
deployable service and based on that information OCCOpus carries out
contextualization for the deployed services. As a result after contextualization
the services can call each other, i.e. they can collaborate to realize a higher
level service called as virtual infrastructure.

OCCOpus can be used in three different ways:

#. Desktop software (i.e. as command line util): In this case virtual infrastructure 
   developers can run OCCOpus on their desktop machine and they give the infrastructure 
   description as input to OCCOpus together with their credentials to the target cloud 
   where they want to deploy theinfrastructure. Based on the description OCCOpus deploys 
   and activates the infrastructure in the cloud and then exits. Then any potential user 
   can use the infrastructure that were built by OCCOpus in the cloud(s). 

#. REST API: OCCOpus can expose its functionalities through a web service with RESTful
   interface. The functionalities like deployment, management, destroy, etc. can
   be realized through REST calls. The current version of OCCOpus as service
   provides manual scaling, too.

#. Library providing the OCCOpus API: In this case infrastructure developers can create 
   a program that deploys the infrastructure in the cloud by calling the OCCOpus APIs. 
   APIs provide a more fine-tuned controlling of the deployment, and management process 
   while further functionalities can be added to the extendable OCCOpus architecture.
   
