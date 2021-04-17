# VMware vRealize Automation

- [VMware vRealize Automation](#vmware-vrealize-automation)
  - [Introduction](#introduction)
  - [Documentation](#documentation)
  - [VMware Cloud Assembly IaaS API](#vmware-cloud-assembly-iaas-api)
    - [Authentication](#authentication)


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