from prettytable import PrettyTable
from requests import request
from os import environ


def vrac_load_creds():
    """Loads and returns vRealize Automation Cloud Fully Qualified Domain Name and
    Refresh Token from system environment variable.  

    Returns:
        tuple: a tuple of strings containing FQDN and Refresh Token
    """
    fqdn = environ.get('CAS_ENDPOINT')
    refreshtoken = environ.get('CAS_API_TOKEN')
    return fqdn, refreshtoken


def vrac_auth(fqdn,refreshtoken):
    """Gets vRealize Automation Fully Qualified Domain Name and Refresh Token and
    returns HTTP Bearer (access) Authentication Header content.

    Args:
        fqdn (str): vRealize Automation Cloud Fully Qualified Domain Name
        refreshtoken (str): vRealize Automation Refresh Token

    Returns:
        string: HTTP Bearer authentication header
    """
    url = "{}/iaas/api/login".format(fqdn)
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        }    
    payload = '{{ "refreshToken": "{}" }}'.format(refreshtoken)
    response = request("POST", url, data=payload, headers=headers).json()
    auth = "Bearer {}".format(response['token'])
    return auth


def get_cloud_accounts(fqdn,auth):
    """Gets vRealize Automation Fully Qualified Domain Name and HTTP Bearer 
    authentication and prints a formatted list of Cloud Accounts.

    Args:
        fqdn (str): vRealize Automation Cloud Fully Qualified Domain Name
        auth (str): HTTP Bearer authentication header

    Returns:
        string: Pretty formatted table of vRA Cloud Accounts summary
    """
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



def main():
    # Load credentials
    fqdn, refreshtoken = vrac_load_creds()

    # Call function
    get_cloud_accounts(fqdn,vrac_auth(fqdn,refreshtoken))

    # Example output
    # +---------------------+---------------+---------+-----------+-------------------------+
    # | Name                | Hostname      | Type    | Version   | Creator                 |
    # +---------------------+---------------+---------+-----------+-------------------------+
    # | nsx-mgr.example.com | 10.200.147.15 | nsxt    | 2.5.0.0.0 | maros.kukan@example.com |
    # | vc.example.com      | 10.200.147.5  | vsphere | 6.7.0     | maros.kukan@example.com |
    # +---------------------+---------------+---------+-----------+-------------------------+


if __name__ == "__main__":
    main()