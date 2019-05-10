# DBAAS Lab Deployment Scripts

## List of Contents
| *Ansible Playbooks* |
| ------------------- |
| rebuild_Lab_Oracle_SA_VM.yml | 
| rebuild_Lab_Oracle_RAC_VM.yml | 
| rebuild_Lab_MSSQL_Win.yml | 

| *Example Inventory files* |
| ------------------------|
| vmware-RAC-lab-env.yml |
| vmware-SA-inv.yml |

| *PowerShell PowerCLI Scripts* |
|-----------------------------|
| rebuild_lab_Oracle_RAC_VMDK.ps1 |
| Run_rebuild_lab_Oracle_RAC_VMDK.ps1 |

- - -
> These scripts all require you to input your vCenter Username/Password. The Ansible Playbooks create VM's based on the names passed in from the Inventory File
> This can be done either through the Command line or you can insert it as a static variable.

> The PowerCLI scripts require you to install PowerShell, and PowerCLI. [PowerCLI Install](https://www.virtualizationhowto.com/2017/05/vmware-powercli-6-5-1-new-way-install/)

> If you are on a Mac or Linux you will need to install PowerShell Core and PowerCLI Core 

> [Mac PowerShell Core/PowerCLI Core Install](https://blogs.vmware.com/PowerCLI/2018/03/installing-powercli-10-0-0-macos.html)

> [Linux PowerShell Core Install](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-linux?view=powershell-6)

> [Linux PowerCLI Core Install(Needs testing)](https://virtualizationreview.com/articles/2017/06/01/how-to-install-and-use-powershell-and-powercli-on-linux.aspx)

## Explanation of Scripts
__**rebuild_Lab_Oracle_SA_VM.yml**__ :

This is an Ansible playbook that clones the Oracle RAC Template in vCenter and configures it as a Standalone Oracle VM.
vmware-SA-inv.yml is an example inventory file to feed into this Playbook

```python
ansible-playbook -i vmware-SA-inv.yml rebuild_Lab_Oracle_SA_VM.yml
```

__**rebuild_Lab_Oracle_RAC_VM.yml**__ :

This is an Ansible playbook that clones the Oracle RAC Template in vCenter and configures N-number of VMs as Oracle RAC VMs.
vmware-RAC-lab-env.yml is an example inventory file to feed into this Playbook

```python
ansible-playbook -i vmware-RAC-lab-env.yml rebuild_Lab_Oracle_RAC_VM.yml
```

__**rebuild_Lab_MSSQL_Win.yml**__ :

This is an Ansible playbook that clones the Oracle RAC Template in vCenter and configures N-number of VMs as Oracle RAC VMs.
vmware-SA-inv.yml is an example inventory file to feed into this Playbook

__**rebuild_lab_Oracle_RAC_VMDK.ps1**__ :

This is a PowerCLI script that creates Multi-Writer VMDKs and attaches them to the Oracle RAC Master Node VM. Then it attaches those VMDK's to the next two nodes in the cluster.

__**Run_rebuild_lab_Oracle_RAC_VMDK.ps1**__ :

This is a PowerShell script that runs the "rebuild_lab_Oracle_RAC_VMDK.ps1" file up to 3 times, depending on how many nodes(Oracle RAC Master Node Hostnames) you pass in.

```powershell
powershell ./Run_rebuild_lab_Oracle_RAC_VMDK.ps1 -vcname irv.techlab.com -vcuser MyvCenterUsername -vcpass MyvCenterPass -Master1 oralab01 -Master2 oralab04 -Master3 oralab07 -DataStore [pure_vmfs6_03]
```