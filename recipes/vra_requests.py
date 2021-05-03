from prettytable import PrettyTable
from requests import request
from os import environ


# Get Environment variables
def load_creds():
    fqdn = environ.get('CAS_ENDPOINT')
    refreshtoken = environ.get('CAS_API_TOKEN')
    return fqdn, refreshtoken

# vRealize Automation Cloud - Generate Access (Bearer) Token
def vrac_auth(fqdn,refreshtoken):
    url = "{}/iaas/api/login".format(fqdn)
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        }    
    payload = '{{ "refreshToken": "{}" }}'.format(refreshtoken)
    response = request("POST", url, data=payload, headers=headers).json()
    auth = "Bearer {}".format(response['token'])
    return auth

# Print cloud account summary
def get_cloud_accounts(fqdn,auth):
    url = "{}/iaas/api/cloud-accounts".format(fqdn)
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
        }
    headers['authorization'] = auth
    content = request("GET", url, headers=headers).json()['content']
    pt = PrettyTable(['Name',
                      'Hostname',
                      'Type',
                      'Version',
                      'Creator'])
    pt.align = "l"
    for element in content:
        pt.add_row((element['name'],
                    element['cloudAccountProperties']['hostName'],
                    element['cloudAccountType'],
                    element['customProperties']['version'],
                    element['customProperties']['createdByEmail']))
    return print(pt)


# Main function
def main():
    # Load credentials
    fqdn, refreshtoken = load_creds()

    # Call function
    get_cloud_accounts(fqdn,vrac_auth(fqdn,refreshtoken))

    # Example output
    # +---------------------+---------------+---------+-----------+------------------------+
    # | Name                | Hostname      | Type    | Version   | Creator                |
    # +---------------------+---------------+---------+-----------+------------------------+
    # | nsx-mgr.example.com | 10.200.147.15 | nsxt    | 2.5.0.0.0 | maros.kukan@domain.com |
    # | vc.example.com      | 10.200.147.5  | vsphere | 6.7.0     | maros.kukan@domain.com |
    # +---------------------+---------------+---------+-----------+------------------------+


if __name__ == "__main__":
    main()