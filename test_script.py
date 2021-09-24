from echome import Session
import logging
import json
from echome.vm import Vm

# logging.getLogger().setLevel(logging.DEBUG)

# session = Session()
# vm_client:Vm = session.client("Vm")


# resp = vm_client.create(
#     ImageId="gmi-92fcfbbc",
#     InstanceType="standard.small",
#     NetworkProfile="home-network",
#     KeyName="echome",
#     PrivateIp="172.16.9.60",
#     Tags={
#         'Name': 'openvswitch'
#     }
# )
# print(resp)

#print(vm_client.stop("vm-7ecd866b"))

# vms = vm_client.describe_all()
# vms = vms["results"]
# print("VMs__________________________________")
# for vm in vms:
#     name = vm["tags"]["Name"] if "Name" in vm["tags"] else ""
#     print(f"{vm['instance_id']}\t{name}")

# resp = vm_client.terminate("vm-f603d655")
# resp = vm_client.terminate("vm-eb11bf5c")
# resp = vm_client.terminate("vm-b5427291")

# network_client = session.client("Network")
# networks = network_client.describe_all()
# networks = networks["results"]
# for network in networks:
#     print(json.dumps(network, indent=4))

# net = network_client.describe("vnet-517d0ed2")
# print(json.dumps(net, indent=4))

#thing = vm.describe_all()
# our_vm = vm.describe("vm-e7468d6e")
# print(our_vm.tags)


# ret = vm_client.create(
#     ImageId="gmi-fc1c9a62", 
#     InstanceSize="standard.micro",
#     NetworkType="BridgeToLan",
#     NetworkInterfacePrivateIp="172.16.9.26/24",
#     NetworkInterfaceGatewayIp="172.16.9.1",
#     KeyName="echome",
#     DiskSize="10G",
#     Tags={"Name": "test_instance", "Env": "staging", "Created_by": "mgutierrez"})

# ret = vm_client.create(
#     ImageId="gmi-fc1c9a62", 
#     InstanceSize="standard.medium",
#     NetworkType="BridgeToLan",
#     NetworkInterfacePrivateIp="172.16.9.21/24",
#     NetworkInterfaceGatewayIp="172.16.9.1",
#     KeyName="echome",
#     DiskSize="50G",
#     Tags={"Name": "kubernetes_worker_1", "Env": "staging", "Created_by": "mgutierrez"})

# ret = vm_client.create(
#     ImageId="gmi-fc1c9a62", 
#     InstanceSize="standard.medium",
#     NetworkType="BridgeToLan",
#     NetworkInterfacePrivateIp="172.16.9.22/24",
#     NetworkInterfaceGatewayIp="172.16.9.1",
#     KeyName="echome",
#     DiskSize="50G",
#     Tags={"Name": "kubernetes_worker_2", "Env": "staging", "Created_by": "mgutierrez"})

# print(ret)
#print(vm.status_code)


# resp = Session().client("Images").guest().register(
#     ImagePath="/mnt/nvme/guestimages/CentOS-7-x86_64-GenericCloud-2003.qcow2",
#     ImageName="CentOS 7",
#     ImageDescription="CentOS 7 Cloud image"
# )
# print(resp)

# guest_images = Session().client("Images").guest().describe_all()

# print("\nGuest Images_______________________")
# for guest_img in guest_images:
#     print(f"{guest_img['guest_image_id']}\t{guest_img['name']}")




# ssh_keys = Session().client("SshKey").describe_all()
# print("\nSSH Keys___________________________")
# for sshkey in ssh_keys:
#     print(f"{sshkey['key_id']}\t{sshkey['key_name']}\t{sshkey['fingerprint']}")


# # SshKeys
# sshkey = Session().client("SshKey")

# ret = sshkey.describe("echome")
#print(ret.fingerprint)