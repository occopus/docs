
CloudSigma
==========

.. _collect_cloudsigma:

The following tutorial will help users how the attributes for the resource section in the node definition can be collected from the web interface of the CloudSigma cloud.

A minimal version of the resource section for CloudSigma may look like as follows:

  .. code:: yaml
    
            resource:
              type: cloudsigma
              endpoint: https://zrh.cloudsigma.com/api/2.0
              libdrive_id: <uuid_of_selected_drive_from_library>
              description:
                cpu: 2000
                mem: 2147483648
                pubkeys:
                  -
                    <uuid_of_your_registered_public_key>
                nics:
                  -
                    firewall_policy: <uuid_of_your_registered_firewall_policy>
                    ip_v4_conf:
                      conf: dhcp
            contextualisation:
              ...

The example above assumes the followings:
  #. Virtual machine will be started at the Zurich site, see ``endpoint`` attribute. To use an alternative location, select one from `the cloudsigma documentation on API endpoints <https://cloudsigma-docs.readthedocs.io/en/latest/general.html#api-endpoint>`_.
  #. CPU speed will be 2000Mhz. See ``cpu`` attribute.
  #. Memory size will be 2GByte. See ``mem`` attribute.
  #. VM will have a public ip address defined by dhcp. See ``ip_v4_conf`` attribute.

You need to collect the following 3 more attributes to complete the section:
 #. ``libdrive_id``
 #. ``pubkeys``
 #. ``firewall_policy``

 **libdrive_id**

    The value of this attribute is an uuid refering to a particular drive in the storage library on which an operating system is preinstalled usually. After login to `the CloudSigma Web UI <https://zrh.cloudsigma.com/ui/#/library>`_, select ``Storage/Library`` menu and a full list of available drives will be listed.

    .. image:: cloudsigma-library-drives-list.png

    Assuming we need an ``Ubuntu 14.04 LTS(Trusty)``, scroll down and search for that drive.

    .. image:: cloudsigma-library-drives-select-ubuntu.png

    Then click on the item and copy its uuid from the address bar.

    .. image:: cloudsigma-library-drives-get-ubuntu-uuid.png

    As a result, the ``libdrive_id`` attribute in the resource section will be ``0644fb79-0a4d-4ca3-ad1e-aeca59a5d7ac`` referring to the drive containing an ``Ubuntu 14.04 LTS(Trusty)`` operating system.

 **pubkeys**

    The value of this attribute is the uuid refering to a particular public key registered under your CloudSigma account. To register a new ssh keypair, generated or upload one at page under the ``Access & Security/Keys Management`` menu. On this page you can see the list of registered keys and their uuid.

    .. image:: cloudsigma-public-ssh-keys.png

    As a result, the ``pubkeys`` attribute in the resource section will be ``d7c0f1ee-40df-4029-8d95-ec35b34dae1e`` in this case refering to the selected key. Multiple keys can be specified, if necessary.

 **firewall_policy**
  
    The value of this attribute is the uuid refering to a particular firewall policy registered under your CloudSigma account. To register a new firewall policy, use the page under the ``Networking/Policies`` menu. On this page you can see the list of registered firewall policies.

    .. image:: cloudsigma-firewall-policy-list.png

    Click on the firewall policy to be applied on the VM, the new page will show the uuid of the policy.

    .. image:: cloudsigma-firewall-policy-get-uuid.png

    As a result, the ``firewall_policy`` attribute in the resource section will be ``fd97e326-83c8-44d8-90f7-0a19110f3c9d`` in this case refering to the selected policy. In this policy, port 22 is open for ssh. Multiple policies can be specified, if necessary.

The finalised resource section with the uuids gathered in the example above will look like this:

  .. code:: yaml

            resource:
              type: cloudsigma
              endpoint: https://zrh.cloudsigma.com/api/2.0
              libdrive_id: 0644fb79-0a4d-4ca3-ad1e-aeca59a5d7ac
              description:
                cpu: 2000
                mem: 2147483648
                pubkeys:
                  -
                    d7c0f1ee-40df-4029-8d95-ec35b34dae1e
                nics:
                  -
                    firewall_policy: fd97e326-83c8-44d8-90f7-0a19110f3c9d
                    ip_v4_conf:
                      conf: dhcp
            contextualisation:
              ...

.. important::
   
   Collect the uuids under your account instead of using the ones in this example!

.. important::
 
   The resource section must follow YAML syntax! Make sure intendation is proper, avoid using <tab>, use spaces!
