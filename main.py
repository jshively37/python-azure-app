import os
import typing as t

try:
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.compute import ComputeManagementClient
    from dotenv import load_dotenv
except ImportError:
    print("Please run pip install -r requirements.txt")

load_dotenv()
SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID")
NAME = os.environ.get("NAME")


def parse_vms(vm_list) -> t.Dict:
    """Take an Azure VM list and parse it returning the VMs that match on Name

    Args:
        vm_list (dict): List of Azure VMs.

    Returns:
        t.Dict: Dictionary formatted with VM tags matching name
    """
    for vm in vm_list:
        # my_vm_dict = {}
        if (
            vm.tags
            and vm.tags.get("owner")
            and NAME.lower() in vm.tags["owner"].lower()
        ):
            print(vm)
        return {}


if __name__ == "__main__":
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    compute_client = ComputeManagementClient(
        credential=credential, subscription_id=SUBSCRIPTION_ID
    )
    vm_list = compute_client.virtual_machines.list_all()
    parse_vms(vm_list=vm_list)
