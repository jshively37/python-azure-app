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


def parse_vms(vm_dict) -> list:
    """Take an Azure VM list and parse it returning the VMs that match on Name tag

    Args:
        vm_dict (dict): Dictionary from Azure SDK containing all the VMs.

    Returns:
        my_vms_list (list): List of tuples containing data necessary to start VMs
    """
    my_vms_list = []
    for vm in vm_dict:
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
