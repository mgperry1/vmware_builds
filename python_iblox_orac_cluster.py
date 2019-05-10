#!/usr/bin/python
import logging
import requests
import json
import sys
import os
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pprint import pprint


# VARS
# user = "admin"
# passwd = "Techno123!"
# infoblox = "10.10.96.86"
# subnet_99 = '10.10.99.0'
# rac_cluster = 'oratest-1-1'
# private_subnet = '112'

# Sys.Argv VARS
user = sys.argv[1]
passwd = sys.argv[2]
infoblox = sys.argv[3]
subnet_99 = sys.argv[4]
rac_cluster = sys.argv[5]
private_subnet = sys.argv[6]
scan_name = sys.argv[7]

rac_cluster = rac_cluster.replace('[', '').replace(']', '').replace('"', '').replace("'", '') #.lstrip('u')
#rac_cluster = rac_cluster.decode()
node_list = [str(x.strip()).lstrip('u') for x in rac_cluster.split(',')]
for node in node_list:
    print(type(node))
print(node_list)

logging.basicConfig(level=logging.DEBUG)

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def subnet_ref(username, password, infoblox_ip, subnet):
    # Collect _ref for subnet 
    url = "https://{}/wapi/v2.7/network?network=".format(infoblox_ip)
    response = requests.get(url + subnet, auth=HTTPBasicAuth(username,password), verify = False)
    data = response.json()
    _ref = data[0]['_ref']
    
    return _ref


def collectNext3IPs(username, password, infoblox_ip, subnet, input_list):
    length = len(input_list)
    # Collect _ref for subnet 
    _ref = subnet_ref(username, password, infoblox_ip, subnet)

    # Use _ref to ask for next 3 IPs on subnet
    url = "https://{}/wapi/v2.7/".format(infoblox_ip)
    next_ip_func = '?_function=next_available_ip&num={}'.format(length)
    response = requests.post(url + _ref + next_ip_func , auth=HTTPBasicAuth(username,password), verify = False)  #, headers=headers)

    return response.json()

def test_host_ips(username, password, infoblox_ip, cluster_names):
    ip_list = collectNext3IPs(user, passwd, infoblox, subnet_99)

    zipped_lists = zip(cluster_names, ip_list['ips'])
    print(zipped_lists)


def add_A_Record(username, password, infoblox_ip, subnet, hostname, type_of_ip, name_list):
    ip_list = collectNext3IPs(username, password, infoblox_ip, subnet, hostname)

    _ref = subnet_ref(username, password, infoblox_ip, subnet)

    url = "https://{}//wapi/v2.7/record:a".format(infoblox_ip)

    headers = {"Content-Type": "application/json"}
    #hostname = "scan-{}.techlab.com".format(hostname)
    if isinstance(hostname, basestring):
        for ip in ip_list['ips']:
            # Add IPs being used into ip_structure dictionary
            if hostname in ip_structure["IPs"]:
                ip_structure["IPs"][hostname].append(ip)
            else:
                ip_structure["IPs"][hostname] = [ip]

            data = {"name": hostname, "ipv4addr": ip}

            #response = requests.post(url, auth=HTTPBasicAuth(username,password), verify = False, data=data)
    
    elif isinstance(hostname, list):
        zipped_lists = zip(hostname, ip_list['ips'], name_list)

        #print(zipped_lists)

        for host in zipped_lists:
            hostname = host[0]
            ip = host[1]
            vm_name = host[2]
            if type_of_ip not in ip_structure['VMs']:
                ip_structure['VMs'][type_of_ip] = []
            #if 
            VM_Obj = ip_structure['VMs'][type_of_ip]

            if type_of_ip == "public":
                ip_split = ip.split('.')
                public_gateway = "{}.{}.{}.{}".format(ip_split[0], ip_split[1], ip_split[2], '1')
                priv_ip = "{}.{}.{}.{}".format(ip_split[0], ip_split[1], private_subnet, ip_split[3])
                private_gateway = "{}.{}.{}.{}".format(ip_split[0], ip_split[1], private_subnet, '1')
                Public_VM_Data = {"Hostname": hostname, 'IP': ip, 'VM_Name': vm_name, 'IP_Type': 'public', "Gateway": public_gateway}
                # TODO: Make sure script does not attempt to provision this as an A RECORD in Infoblox
                Private_VM_Data = {"Hostname": hostname, 'IP': priv_ip, 'VM_Name': vm_name, 'IP_Type': 'private', "Gateway": private_gateway}
                VM_Obj.append(Public_VM_Data)
                if 'private' not in ip_structure['VMs']:
                    ip_structure['VMs']['private'] = []
                ip_structure['VMs']['private'].append(Private_VM_Data)
                #VM_Obj.append(Private_VM_Data)
            else:
                ip_split = ip.split('.')
                public_gateway = "{}.{}.{}.{}".format(ip_split[0], ip_split[1], ip_split[2], '1')
                VM_Data = {"Hostname": hostname, 'IP': ip, 'VM_Name': vm_name, 'IP_Type': type_of_ip, "Gateway": public_gateway}

                VM_Obj = ip_structure['VMs'][type_of_ip].append(VM_Data)
            # Modify the public IP to have private IP subnet and add to the same list
               

            #priv_ip = ip     


            #VM_Data = {"hostname": hostname, 'Public_IP': ip, 'Cluster_Name': vm_name, 'IP_Type': type_of_ip, 'Private_IP': priv_ip}
            #VM_Obj = ip_structure['VMs'][type_of_ip].append(VM_Data)

            # if 'IPs' in ip_structure['VMs'][type_of_ip]:
            #     VM_Obj = ip_structure['VMs'][type_of_ip]
            #     #VM_Obj
            #     ip_structure['VMs'][type_of_ip]['IPs'].append(ip)
            #     VM_Obj['Hostname'] = hostname
            #     VM_Obj['VM_Name'] = vm_name

            # else:
            #     ip_structure['VMs'][type_of_ip]['IPs'] = [ip]
            data = {"name": hostname, "ipv4addr": ip}



            response = requests.post(url, auth=HTTPBasicAuth(username,password), verify = False, data=data)


    #return response.json()

def del_A_Record(username, password, infoblox_ip, hostname):
    # Ask for _ref for hostname
    url = 'https://{}/wapi/v2.7/record:a?name={}'.format(infoblox_ip, hostname)
    response = requests.get(url, auth=HTTPBasicAuth(username,password), verify = False)
    hostnames = response.json()
    #print(json)
    url = "https://{}//wapi/v2.7/".format(infoblox_ip)

    responses = []
    for host in hostnames:
        _ref = host['_ref']
        #print(_ref)
        response = requests.delete(url + _ref, auth=HTTPBasicAuth(username,password), verify = False) #, data=data)
        responses.append(response.json())
    
    if not responses:
        responses = "Couldn't find any hosts by that hostname"

    return responses

    #headers = {"Content-Type": "application/json"}
    #hostname = "scan-{}.techlab.com".format(hostname)
    
    # use _ref to delete the A Record for that hostname
    #response = requests.delete(url + _ref, auth=HTTPBasicAuth(username,password), verify = False, data=data)
    #print(ip_list)
    # for ip in ip_list['ips']:
    #     data = {"name": hostname, "ipv4addr": ip}
    #     print(data['name'])
    # #print(url + _ref)
    #     response = requests.delete(url, auth=HTTPBasicAuth(username,password), verify = False, data=data)


    #return response.json()

#next3_IPs = collectNext3IPs(user, passwd, infoblox, subnet_99)
#print(next3_IPs)

#TODO: Instead of having it modify the last num here, need it to take in multiple mosts and pass them in unchanged...
hostname = rac_cluster[:-2]

#cluster = ['{}-1'.format(hostname), '{}-2'.format(hostname), '{}-3'.format(hostname)]
cluster = node_list

hostname_structure = {}
# TODO: Need to figure out how to properly pass the scan name in here and also find the name in the above cluster var
hostname_structure['scan'] = ['{}.techlab.com'.format(scan_name) for x in cluster]
#hostname_structure['scan'] = ['scan-' +x[:-2] + '.techlab.com' for x in cluster]
hostname_structure['vip'] = ['{}-vip.techlab.com'.format(x) for x in cluster]
hostname_structure['public'] = ['{}.techlab.com'.format(x) for x in cluster]

print(hostname_structure['scan'])
print(hostname_structure['vip'])
print(hostname_structure['public'])

#print(cluster)
ip_structure = {}
ip_structure["VMs"] = {}

#test_host_ips(user, passwd, infoblox, cluster)




#add_A_Record(user, passwd, infoblox, subnet_99, next3_IPs, cluster)

pub_record = add_A_Record(user, passwd, infoblox, subnet_99, hostname_structure['public'], 'public', cluster)
vip_record = add_A_Record(user, passwd, infoblox, subnet_99, hostname_structure['vip'], 'vip', cluster)
scan_record = add_A_Record(user, passwd, infoblox, subnet_99, hostname_structure['scan'], 'scan', cluster)



#print(ip_structure['IPs'].keys())
# pub_ips = ip_structure['VMs']['public_private']
# for pub_ip in pub_ips:
#     ip = pub_ips[pub_ip][0]
#     ip_split = ip.split('.')
#     priv_ip = "{}.{}.{}.{}".format(ip_split[0], ip_split[1], private_subnet, ip_split[3])
#     # Modify the public IP to have private IP subnet and add to the same list
#     pub_ips[pub_ip].append(priv_ip)
    


# rm_scan_ips = del_A_Record(user, passwd, infoblox, 'scan-{}.techlab.com'.format(hostname)))
# rm_vip_ips = del_A_Record(user, passwd, infoblox, '{}-vip.techlab.com'.format(hostname))
# rm_pub_ips = del_A_Record(user, passwd, infoblox, '{}.techlab.com'.format(hostname))


keys = ip_structure.keys()
print(ip_structure)

ensure_dir('./clusters/')

with open('./clusters/ip_structure.json', 'w') as fp:
    json.dump(ip_structure, fp, indent=4, sort_keys=True)

# The passed in cluster name/scan name will be the name of the file created
cluster_filename = "{}.json".format(scan_name)

with open("./clusters/{}".format(cluster_filename), 'w') as fp:
    json.dump(ip_structure, fp, indent=4, sort_keys=True)

#delete = raw_input("Do you want to delete, Y/N? ")
# if delete[0] == 'Y' or 'y':
#     # TODO UPDATE.. To once again delete the whole set of records
#     for key in keys:
#         del_A_Record(user, passwd, infoblox, key)
