.. _dev-api:

API
===

Basic features for Occopus-based applications
---------------------------------------------

Common functions of a generic Occopus app.

This module can be used to implement OCCO-based applications in a unified way. The module provides features for command-line and file based configuration of an Occopus application, and other generic features.

There are two ways to build an Occopus application.

    #. The components provided by Occopus can be used as simple librares: they can be imported and glued together with specialized code, a script.
    #. The other way is to use this module as the core of such an application. This module can build an Occopus architecture based on the contents of a YAML config file. (Utilizing the highly dynamic nature of YAML compared to other markup languages.)

The setup function expects a config file either through its cfg_path parameter, or it will try to get the path from the command line, or it will try some default paths (see occo.util.config.config for specifics). See the documentation of setup for details.


**data**
    occo.api.occoapp.args = None

Arguments parsed by argparse or an occo.util.config class.

**data**
    occo.api.occoapp.configuration = None

Configuration data loaded from the file(s) specified with ``--cfg``.

**data**
    occo.api.occoapp.infrastructure = None

The OCCO infrastructure defined in the configuration.

**func**
    occo.api.occoapp.setup(setup_args=None, cfg_path=None, auth_data_path=None)

Build an Occopus application from configuration.

**Parameters:**
    * ``setup_args (function)`` – A function that accepts an argparse.ArgumentParser object. This function can set up the argument parser as needed (mainly: add command line arguments).
    * ``cfg_path (str)`` – Optional. The path of the configuration file. If unspecified, other sources will be used (see occo.util.config.config for details).

Occopus Configuration
`````````````````````

Occopus uses YAML as a configuration language, mainly for its dynamic properties, and its human readability. The parsed configuration is a dictionary, containing both static parameters and objects already instantiated (or executed, sometimes!) by the YAML parser.

The configuration must contain the following items.

**logging**
    The logging configuration dictionary that will be used with logging.config.dictConfig to setup logging.

**components**
    The components of the Occopus architecture that’s need to be built.

    **resourcehandler**
        The ResourceHandler instance (singleton) to be used by other components (e.g. the InfraProcessor. Multiple backends can be supported by using a basic occo.resourcehandler.ResourceHandler instance here configured with multiple backend clouds/resources.

    **configmanager**
        The ConfigManager instance (singleton) to be used by other components (e.g. the InfraProcessor. Multiple backends can be supported by using a basic occo.resourcehandler.ConfigManager instance here configured with multiple backend service composers *(This feature is not yet implemented at the time of writing.)*.

    **uds**
        The storage used by this Occopus application.


Infrastructure Manager
----------------------

Occopus Infrastructure Manager

**class**
    ::

        occo.api.manager.InfrastructureManager(process_strategy='sequential')

    Manages a set of infrastructures. Each submitted infrastructure is assigned an InfrastructureMaintenanceProcess that maintains it.
    Compiling + storing the infrastructure is decoupled from starting provisioning. This enables the manager to attach to existing, but not provisioned infrastructures. I.e., if the manager fails, it can be restarted and reattached to previously submitted infrastructures.

    **Parameters:** process_strategy (str) – The identifier of the processing strategy for Infrastructure Processor

    **method**
        **add(infra_desc)**
            Compile, store, and start provisioning the given infrastructure. A simple composition of submit_infrastructure and start_provisioning.
            **Parameters:** infra_desc – An infrastructure description.

        **attach(infra_id)**
            Start provisioning an existing infrastructure.

            **Parameters:** infra_id (str) – The identifier of the infrastructure. The infrastructure must be already compiled and stored in the UDS.

        **detach(infra_id)**
            Stop provisioning an existing infrastructure.

            **Parameters:**	infra_id (str) – The identifier of the infrastructure. The infrastructure must be already compiled and stored in the UDS.

        **get(infra_id)**
            Get the managing process of the given infrastructure.

            **Parameters:**	infra_id (str) – The identifier of the infrastructure.
            **Raises InfrastructureIDNotFoundException:** if the infrastructure is not managed.

        **start_provisioning(infra_id)**
            Start provisioning the given infrastructure. An InfrastructureMaintenanceProcess is created for the given infrastructure. This process is then stored in a process table so it can be managed.
            This method can be used to attach the manager to infrastructures already started and having a state in the database.

            **Parameters:**	infra_id (str) – The identifier of the infrastructure. The infrastructure must be already compiled and stored in the UDS.
            **Raises InfrastructureIDTakenException:** when the infrastructure specified is already being managed.

        **stop_provisioning(infra_id, wait_timeout=60)**
            Stop provisioning the given infrastructure. The managing process of the infrastructure is terminated gracefully, so the infrastructure stops being maintained; the manager is detached from the infrastructure. The infrastructure itself will not be torn down.

            **Parameters:**	infra_id (str) – The identifier of the infrastructure.
            **Raises InfrastructureIDNotFoundException:** if the infrastructure is not managed.

        **submit_infrastructure(infra_desc)**
            Compile the given infrastructure and stores it in the UDS.

            **Parameters:**	infra_desc – An infrastructure description.

        **tear_down(infra_id)**
            Tear down an infrastructure. This method tears down a running, but unmanaged infrastructure. For this purpose, an Infrastructure Processor is created, so this method does not rely on the Enactor’s ability (non-existent at the time of writing) to tear down an infrastructure.
            If the infrastructure is being provisioned (the manager is attached), this method will fail, and not call stop_provisioning implicitly.

            **Parameters:**	infra_id (str) – The identifier of the infrastructure.
            **Raises ValueError:** if the infrastructure is being maintained by this manager. Call stop_provisioning first, explicitly.

    ::

        occo.api.manager.InfrastructureMaintenanceProcess(infra_id, enactor_interval=10, process_strategy='sequential')

    A process maintaining a single infrastructure. This process consists of an Enactor, and the corresponding Infrastructure Processor. The Enactor is instructed to make a pass at given intervals.

        **Parameters:**
            ``infra_id (str)`` – The identifier of the already submitted infrastructure.
            ``enactor_interval (float)`` – The number of seconds to elapse between Enactor passes.
            ``process_strategy (str)`` – The identifier of the processing strategy for Infrastructure Processor

