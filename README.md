# VMware vRealize Automation

- [VMware vRealize Automation](#vmware-vrealize-automation)
  - [Introduction](#introduction)
  - [Documentation](#documentation)
  - [Postman Collection](#postman-collection)
  - [Python Recipes](#python-recipes)
  - [VMware Cloud Assembly IaaS API](#vmware-cloud-assembly-iaas-api)
    - [vRA Authentication (on-prem)](#vra-authentication-on-prem)
    - [vRA Cloud Authentication (SaaS)](#vra-cloud-authentication-saas)
    - [About](#about)
    - [Cloud Account](#cloud-account)
      - [Filtering output - array](#filtering-output---array)
      - [Filtering output - list](#filtering-output---list)
    - [Fabric Network](#fabric-network)
    - [Network](#network)
    - [Network Profile](#network-profile)
    - [Organization](#organization)
    - [Miscellaneous](#miscellaneous)


## Introduction

The following document describes the usage of VMware vRealize Automation Cloud Assembly IaaS REST API Interface. The API calls were tested with version 8.3.


## Documentation

- [vRA Cloud Assembly API](https://blogs.vmware.com/management/2021/02/vra-cloud-assembly-iaas-api.html)
- [vRealize Automation Cloud API Programming Guide](https://code.vmware.com/docs/11049/vrealize-automation-api-programming-guide)
- [vRealize Automation 8.4 API Programming Guide](https://code.vmware.com/docs/13520/vrealize-automation-8-4-api-programming-guide)
- [vRealize Automation Cloud Swagger API Documentation](https://www.mgmt.cloud.vmware.com/iaas/api/swagger/ui/)
- [vRA API Python](https://www.thehumblelab.com/vrealize-automation-api-with-python/)
- [Request Timing](https://blog.cloudflare.com/a-question-of-timing/)
- [Pretty Table](https://zetcode.com/python/prettytable/)


## Postman Collection

I have leveraged the publicly available **vRealize Automation Cloud Swagger API Documentation** in order to create a postman colleclection. The collection contains multiple folders such as `Authentication` and `IAAS`.

In order to get started, you need to populate the following collection variables with your specific environment:
- `CAS_ENDPOINT`
- `CAS_USERNAME`
- `CAS_PASSWORD` for vRA on-prem or `CAS_API_TOKEN` for vRA Cloud

In regards, to the `apiVersion`, the initial value is set to `2019-01-15`. Although it is not mandatory to include it with each request, it is highly recommended for future backward compatibility.

## Python Recipes

The repipes folder contains example code that leverages **requests** library to interact with vRealize Automation Cloud API.

In general, it loads `CAS_ENDPOINT` and `CAS_API_TOKEN` OS environment variables and stores them as python variables used as input for Bearer token generation function.

This function is then nested in other functions such as `get_cloud_accounts()` which retrieves and prints result using `prettytable` library.


## VMware Cloud Assembly IaaS API

The following section explains how authentication works for vRA and for vRA Cloud as well as sample REST API calls using `curl`.

### vRA Authentication (on-prem)

Most of the API calls require a token in Authorization header to be present in the request. You can this token by authenticating with username and password first.

Rename the `environment.example` file to `environment.sh` file in `ingredients` and update content to reflect your particular environment. Load the variables from this script using the `source` shell built in. 

```bash
# Load environment script
. ingredients/environment.sh

# Optionally verify content of Endpoint and Token
echo $CAS_ENDPOINT
echo $ACCESS_TOKEN
```

This script will generate an environemnt variable `ACCESS_TOKEN` that will be used for authenticating all API requests.

### vRA Cloud Authentication (SaaS)

Authentication for SaaS offering works differently than the on-prem solution. In order to generate **Access Token** you need to first create an **API Token**. 
1. Authenticate using your VMware Account at [vRA Cloud web portal](https://console.cloud.vmware.com/csp/gateway/discovery)
2. If you are member of multiple organizations, make sure the right one is selected
3. Navigate to **My Account** and click **API Tokens** tab
4. Click **GENERATE A NEW API TOKEN**
   1. Enter Token Name
   2. Under Organization Roles, select **Organization Owner**
   3. Under Service Roles, select **VMware Cloud Assemby Administrator** and **Service Broker Administrator**
5. Click **Generate**

Save token in environemnt variable, it will be next step.
```bash
CAS_API_TOKEN="<your-api-token>"
```

Optionally, measure you latency to API endpoints.

```bash
# Optionally find closes API endpoint
# endpoint name endpoint latency in seconds
bash 'ingredients/get_cas_endpoints.sh'
api.mgmt.cloud.vmware.com 0.919832
au.api.mgmt.cloud.vmware.com 1.458660
ca.api.mgmt.cloud.vmware.com 1.282106
de.api.mgmt.cloud.vmware.com 0.300723
jp.api.mgmt.cloud.vmware.com 1.189917
sg.api.mgmt.cloud.vmware.com 0.935056
```

```bash
# Set the vRA Cloud URL
CAS_ENDPOINT="https://api.mgmt.cloud.vmware.com"

# Generate Access Token

ACCESS_TOKEN=`curl --noproxy '*' \
--silent \
--request POST \
--header 'Content-Type: application/json' \
--data '{
"refreshToken": "'"$CAS_API_TOKEN"'"
}' \
"${CAS_ENDPOINT}/iaas/api/login" \
| jq -r .token`

# Optionally verify content of Endpoint and Token
echo $CAS_ENDPOINT
echo $ACCESS_TOKEN
```

After 25 minutes of inactivity, the access token times out and you must request it again.

### About

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
"${CAS_ENDPOINT}/iaas/api/about" \
| jq -r .
```

### Cloud Account

Get cloud accounts. Display `content` in JSON output.

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/cloud-accounts \
| jq -r .
```

#### Filtering output - array

Get cloud accounts. Display only `name`, `hostname`, `type`, `version` and `creator`.

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/cloud-accounts \
| jq -r '.content[] | {name: .name, 
                       hostName: .cloudAccountProperties.hostName, 
                       cloudAccountType: .cloudAccountType,
                       version: .customProperties.version,
                       createdByEmail: .customProperties.createdByEmail}'
```

Sample output from last request.
```json
{
  "name": "nsx-mgr.example.com",
  "hostName": "10.200.147.15",
  "cloudAccountType": "nsxt",
  "version": "2.5.0.0.0",
  "createdByEmail": "maros.kukan@example.com"
}
{
  "name": "vc.example.com",
  "hostName": "10.200.147.5",
  "cloudAccountType": "vsphere",
  "version": "6.7.0",
  "createdByEmail": "maros.kukan@example.com"
}
```

#### Filtering output - list

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/cloud-accounts \
| jq -r '.content[] | [.name, 
                       .cloudAccountProperties.hostName, 
                       .cloudAccountType,
                       .customProperties.version,
                       .customProperties.createdByEmail] 
                    | @csv'
```

Sample output from last request
```csv
"nsx-mgr.example.com","10.200.147.15","nsxt","2.5.0.0.0","maros.kukan@example.com"
"vc.example.com","10.200.147.5","vsphere","6.7.0","maros.kukan@example.com"
```


Get vSphere cloud accounts

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/cloud-accounts-vsphere \
| jq -r .
```

Get NSX-T cloud accounts

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/cloud-accounts-nsx-t \
| jq -r .
```

### Fabric Network

Get fabric networks

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/fabric-networks/ \
| jq -r .
```

Get fabric network with a given by id.
```bash
# Set Id
ID="82004918-eb6e-4a0b-aaa5-9e9eec254782"

curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/fabric-networks/${ID} \
| jq -r .
```

### Network

Get network domains

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/network-domains \
| jq -r .
```

Get networks

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/networks \
| jq -r .
```

Get networks with jq output filter

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/networks \
| jq -r '.content[] | {cidr: .cidr, name: .name,}'
```

### Network Profile

Get network profiles

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/network-profiles \
| jq -r .
```

Get network profile by id

```bash
# Set Id
ID="09311f12-16ab-4986-8fd1-e09f6fa77843"

curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/network-profiles/${ID} \
| jq -r .
```

Get network profiles with jq output filter

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "Authorization: Bearer ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/iaas/api/network-profiles \
| jq -r '.content[] | {name: .name, isolationType: .isolationType, isolationNetworkDomainCIDR: .isolationNetworkDomainCIDR}'
```

### Organization

Retrieve User Organization ID

```bash
curl --noproxy '*' \
--silent \
--insecure \
--request GET \
--insecure \
--header "csp-auth-token: ${ACCESS_TOKEN}" \
${CAS_ENDPOINT}/csp/gateway/am/api/loggedin/user/orgs \
| jq -r .refLinks[]
```

### Miscellaneous

Retrieve API version and Documentation link.

```bash
# Example for vRA Cloud
baseUrl="https://api.mgmt.cloud.vmware.com"
swaggerUrl=`curl --noproxy \
     --silent \
     https://api.mgmt.cloud.vmware.com/iaas/api/about \
     | jq -r '.supportedApis[0].documentationLink'`
```

Retrieve API documentation.

```bash
curl --noproxy '*' \
--silent \
--insecure \
${baseUrl}${swaggerUrl} \
| jq -r .
```