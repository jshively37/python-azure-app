import os
from collections import namedtuple

try:
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.compute import ComputeManagementClient
    from dotenv import load_dotenv
except ImportError:
    print("Please run pip install -r requirements.txt")

load_dotenv()
SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID")
NAME = os.environ.get("NAME")


def parse_vms(vm_dict) -> list:
    """Take an Azure VM list and parse it returning the VMs that match on Name tag

    Args:
        vm_dict (dict): Dictionary from Azure SDK containing all the VMs.

    Returns:
        my_vms_list (list): List of tuples containing data necessary to start VMs
    """
    vm_named_tuple = namedtuple("resource_group_name", "rg_name vm_name")
    my_vms_list = []
    for vm in vm_dict:
        if (
            vm.tags
            and vm.tags.get("owner")
            and NAME.lower() in vm.tags["owner"].lower()
        ):
            # We need to pass the resource group name to start the VM. The only reference group
            # reference in the data returned in list_all is the id which is the API endpoint.
            # We can split on vm id using resourceGroups/ and then / again to return the resource
            # group.
            # I'll look to see if there is a cleaner way to return the resource group name.
            _ = vm.id.split("resourceGroups/")
            resource_group_name = _[1].split("/")[0]
            my_vms_list.append(vm_named_tuple(resource_group_name, vm.name))
    return my_vms_list


if __name__ == "__main__":
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    compute_client = ComputeManagementClient(
        credential=credential, subscription_id=SUBSCRIPTION_ID
    )
    my_vms = parse_vms(compute_client.virtual_machines.list_all())
    for vm in my_vms:
        compute_client.virtual_machines.begin_start(
            resource_group_name=vm.rg_name, vm_name=vm.vm_name
        )
