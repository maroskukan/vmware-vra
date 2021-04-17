# VMware vRealize Automation

- [VMware vRealize Automation](#vmware-vrealize-automation)
  - [Introduction](#introduction)
  - [Documentation](#documentation)
  - [VMware Cloud Assembly IaaS API](#vmware-cloud-assembly-iaas-api)
    - [Authentication](#authentication)
    - [About](#about)
    - [Cloud Account](#cloud-account)
    - [Fabric Network](#fabric-network)
    - [Network](#network)
    - [Network Profile](#network-profile)
    - [Organization](#organization)
    - [Miscellaneous](#miscellaneous)


## Introduction

The following document describes the usage of VMware vRealize Automation Cloud Assembly IaaS REST API Interface. The following calls were tested with version 8.3.

## Documentation

[vRA API Docs](https://code.vmware.com/docs/13205/vrealize-automation-8-3-api-programming-guide)
[vRA API Overview](https://blogs.vmware.com/management/2021/02/vra-cloud-assembly-iaas-api.html)
[Authentication](https://code.vmware.com/docs/13205/vrealize-automation-8-3-api-programming-guide/GUID-AC1E4407-6139-412A-B4AA-1F102942EA94.html)
[vRA API Python](https://www.thehumblelab.com/vrealize-automation-api-with-python/)


## VMware Cloud Assembly IaaS API

### Authentication

Most of the API calls require a token in Authorization header to be present in the request. You can this token by authenticating with username and password first.

Rename the `environment.example` file to `environment.sh` file in `ingredience` and update content to reflect your particular environment. Load the variables from this script using the `source` shell built in. 

```bash
# Load environment script
. ingredience/environment.sh

# Optionally verify content of Endpoint and Token
echo $CAS_ENDPOINT
echo $ACCESS_TOKEN
```

This script will generate an environemnt variable `ACCESS_TOKEN` that will be used for authenticating all API requests.

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

Get cloud accounts

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

```bash
#    ***************************************************************************
#    ********************     Retrieve Swagger Definition   ********************
#    ***************************************************************************
curl --noproxy '*' \
--silent \
--insecure \
${CAS_ENDPOINT}/iaas/api/swagger \
| jq -r .
```