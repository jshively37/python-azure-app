import os

try:
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.compute import ComputeManagementClient
    from dotenv import load_dotenv
except ImportError:
    print("Please run pip install -r requirements.txt")

load_dotenv()
SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID")
NAME = os.environ.get("NAME")


def parse_vms(vm_list) -> list:
    """Take an Azure VM list and parse it returning the VMs that match on Name

    Args:
        vm_list (dict): List of Azure VMs.

    Returns:
        my_vms_list (list): List of tuples used to start VMs
    """
    my_vms_list = []
    for vm in vm_list:
        if (
            vm.tags
            and vm.tags.get("owner")
            and NAME.lower() in vm.tags["owner"].lower()
        ):
            _ = (vm.name, vm.id)
            my_vms_list.append(_)
    return my_vms_list


if __name__ == "__main__":
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    compute_client = ComputeManagementClient(
        credential=credential, subscription_id=SUBSCRIPTION_ID
    )
    my_vms = parse_vms(compute_client.virtual_machines.list_all())
    for vm in my_vms:
        print(vm)
