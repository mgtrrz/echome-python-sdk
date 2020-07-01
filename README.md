# ecHome Python SDK

This Python library is for use with interacting with the [ecHome](https://github.com/mgtrrz/echome/) virtual machine manager.

This library allows for managing aspects of ecHome with classes. The SDK is responsible for starting and authenticating user sessions, making the calls to the API, returning raw JSON responses, and in the future, objects based on the services.

If you're looking for a CLI interface for managing your ecHome server, visit [echome-cli](https://github.com/mgtrrz/echome-cli/) and install the CLI tool which uses this library. If you're interested in programmatically interfacing with ecHome, this is the library to do so.

## Authentication

This library works by using config/credentials in the user's home directory in `.echome`. Fill in the contents of the files with the following information:

File: `~/.echome/config`
```
[default]
server=<ECHOME-SERVER-IP>
format=table
```

Replace `<ECHOME-SERVER-IP>` with the IP address of the server running ecHome. The format can either be `table` or `json`. This variable is only used in the ecHome CLI.

File: `~/.echome/credentials`
```
[default]
access_id = <AUTH-ID>
secret_key = <AUTH-SECRET-KEY>
```

Alternatively, set the following environment variables at a minimum:
```
export ECHOME_SERVER=<ECHOME-SERVER-IP>
export ECHOME_ACCESS_ID=<AUTH-ID>
export ECHOME_SECRET_KEY=<AUTH-SECRET-KEY>
```

## Example code

An example for interacting with the SDK:

```
from echome import Session, Vm, Images, SshKey

import json

vm_client = Session().client("Vm")

vms = vm_client.describe_all()
print("VMs__________________________________")
for vm in vms:
    name = vm["tags"]["Name"] if "Name" in vm["tags"] else ""
    print(f"{vm['instance_id']}\t{name}")

guest_images = Session().client("Images").guest().describe_all()
print("\nGuest Images_______________________")
for guest_img in guest_images:
    print(f"{guest_img['guest_image_id']}\t{guest_img['name']}")

ssh_keys = Session().client("SshKey").describe_all()
print("\nSSH Keys___________________________")
for sshkey in ssh_keys:
    print(f"{sshkey['key_id']}\t{sshkey['key_name']}\t{sshkey['fingerprint']}")

```

```
python3 test_script.py 
VMs__________________________________
vm-a8b30fda     ubiquiti controller
vm-b49c2840     ansible_host
vm-29b73556     kubernetes_master
vm-2bfecdf6     kubernetes_worker_1
vm-2e10d36e     kubernetes_worker_2

Guest Images_______________________
gmi-d60beeba    Ubuntu 16.04 Server
gmi-fc1c9a62    Ubuntu 18.04 Server
gmi-1326e63a    Windows 10 May 2020 64-bit
gmi-6341042a    Windows Server 2020 R2 Standard Eval 64-bit

SSH Keys___________________________
key-5393842a    example_key     MD5:98:6c:0f:e5:fb:cb:74:5d:fa:f8:3c:f1:03:e3:35:5b
key-91c8cbd8    test_key        MD5:62:dd:13:e9:7f:a9:be:23:cf:df:64:ac:4b:63:77:d9
key-8ff552b8    echome  MD5:d4:d2:12:d3:95:81:9a:10:ba:43:43:15:45:08:a7:bc
```



## Authors

* **mgtrrz** - *Initial work* - [Github](https://github.com/mgtrrz) - [Twitter](https://twitter.com/marknine)

See also the list of [contributors](https://github.com/mgtrrz/echome/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
