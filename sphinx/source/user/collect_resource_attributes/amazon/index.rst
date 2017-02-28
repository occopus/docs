
Amazon
======

.. _collect_amazon:

This tutorial helps users how the attributes for the resource section in the node definition can be collected from the web interface of the Amazon cloud.

First of all, you need of course an Amazon AWS account. Using Amazon AWS is implemented using the EC2 interface, thus the :ref:`EC2-Helloworld <ec2-helloworld>`  tutorial is a good starting point.

In case of Amazon EC2, the following information is necessary to start up a node in an Occopus infrastructure:

* Security credentials (access key and secret key)
* Amazon region name and its EC2 endpoint
* an image ID (AMI)
* an instance type
* at least one security group ID
* a key pair name
* a subnet identifier.

**Security credentials (access key and secret key)**

You can get your access key and secret key through the web interface of Amazon AWS:

1. Visit the `AWS console <https://console.aws.amazon.com/console/home>`_.

2. In the top right corner, select "Security credentials" under your profile as shown in the following screenshot:

.. image:: collecting_resource_attributes_amazon_fig1.png
  
3. Expand the Access keys menu, as shown in the following screenshot:

.. image:: collecting_resource_attributes_amazon_fig2.png
 
4. Click on the "Create New Access Key" button to create new credentials if you don't know the Secret Access Key of your already existing key(s). A window similar to the following screenshot will appear. Here you can make your **Access Key ID** and **Secret Access Key** appear, but you can also download your credentials for later use.

  .. image:: collecting_resource_attributes_amazon_fig3.png

**Amazon region name and its EC2 endpoint**

Amazon hosts its services in multiple regions. There are two possible ways to get region names and their relevant EC2 endpoints: using the EC2 command line tools or the web interface.

**Use the web interface to get region names and EC2 endpoints**

The Amazon Documentation `Amazon Documentation <http://docs.aws.amazon.com/general/latest/gr/rande.html#ec2_region>`_  has a list of available regions and their EC2 endpoints. In order to get the complete EC2 endpoint URL for Occopus, simply add ``https://`` before the Endpoint specified by the table shown in the `Amazon Documentation <http://docs.aws.amazon.com/general/latest/gr/rande.html#ec2_region>`_'s table.
For example, the EC2 endpoint URL of the ``eu-west-1`` region is ``https://ec2.eu-west-1.amazonaws.com.`` Simple as that.


**Use the EC2 command line tools to get region names and EC2 endpoints**

Follow the `EC2 command line tool setup guide <http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/ec2-cli-get-set-up.html>`_ to set up and configure EC2 command line tools onto your machine. Once done, you can use the ``ec2-describe-regions`` command to list available regions and EC2 endpoints:


   .. code:: yaml

    $ ec2-describe-regions  -H
    REGION	Name 	        Endpoint
    REGION	eu-west-1	ec2.eu-west-1.amazonaws.com
    REGION	ap-southeast-1	ec2.ap-southeast-1.amazonaws.com
    REGION	ap-southeast-2	ec2.ap-southeast-2.amazonaws.com
    REGION	eu-central-1	ec2.eu-central-1.amazonaws.com
    REGION	ap-northeast-1	ec2.ap-northeast-1.amazonaws.com
    REGION	us-east-1	ec2.us-east-1.amazonaws.com
    REGION	sa-east-1	ec2.sa-east-1.amazonaws.com
    REGION	us-west-1	ec2.us-west-1.amazonaws.com
    REGION	us-west-2	ec2.us-west-2.amazonaws.com

Here, the second column shows the region name, the third column shows the EC2 endpoint for the given region. You should prefix the endpoint name with ``https://`` for receiving the endpoint URL for Occopus.

**Get image ID**

Two possible methods are available to get a proper image ID: using the EC2 CLI tools' ``ec2-describe-images -a`` command and the web interface. The second one is preferred, as one can get a more user-friendly description of the picked on image.

In the AWS EC2 management console, select **AMIs** from the **IMAGES** menu. Search for an AMI, as shown in the screenshot below:


 .. image:: collecting_resource_attributes_amazon_fig4.png

Here, the value of the **AMI ID** column contains the image identifier.


**Get instance type**

The instance type determines the characteristics (CPU, memory) of the VM created. You can get the names and properties of the instance types supported by Amazon through the `Instance types documentation <https://aws.amazon.com/ec2/instance-types/>`_.


**Get security group IDs**

Security groups define the network traffic allowed for the instances to be started. Thus, you should create security groups in order to enable SSH or HTTP traffic into your VM.
The following screenshot shows a number of security groups already defined. Select those you'd like to attach to the VM started by Occous. The value of the **Group ID** column contains the values which are needed by Occopus.

  .. image:: collecting_resource_attributes_amazon_fig5.png


**Get keypair name**

Key pairs are importd into your running VM so SSH access is possible. You can check the name of available keypairs in the AWS EC2 management console, under the **Key Pairs** menu as shown in the following screenshot. The value of the **Key pair name** is the one Occopus needs.

  .. image:: collecting_resource_attributes_amazon_fig6.png


**Get Subnet identifier**

You can get the list of available subnets through the AWS VPC dashboard, by selecting **Subnets** from the menu as shown in the following screenshot. You should use the value of the **Subnet ID** column for Occopus.

  .. image:: collecting_resource_attributes_amazon_fig7.png


**Closing**

With all the above values, now you can modify the :ref:`EC2-Helloworld <ec2-helloworld>` tutorial to run on Amazon.
