import json
import requests
import requests.exceptions as re

# define the filters to only allow specific services and regions
service_filters = [{
        "service_name":"AMAZON_CONNECT",
        "regions":["us-east-1","us-east-2"]
    },{
        "service_name":"EC2",
        "regions":["us-east-1","us-east-2"]
    },{
        "service_name":"CLOUDFRONT",
        "regions":["GLOBAL"]
    }]

# data structure to capture the filtered regions, services and number of ips
filtered_results = {}

# download the ip ranges into memory
try:
    r = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json')
    result = r.json()
# handle network exceptions
except re.RequestException as e:
    raise SystemExit(e)

# iterate through all of the result IPv4 prefixes
for prefix in result["prefixes"]:
    # store attributes about the current record
    service_name = prefix["service"]
    region = prefix["region"]
    ip_prefix = prefix['ip_prefix']
    
    # iterate through all of the filters, checking to see if we should keep the records
    for service_filter in service_filters:
        # store relevent attributes of the current filter
        service_filter_name = service_filter["service_name"]
        service_filter_regions = service_filter["regions"]

        # filter out services that do not match any filter (by service name or selected region)
        if service_name != service_filter_name or region not in service_filter_regions:
            continue

        else:
            # add a starter data structure if the service does not yet exist in the filtered results
            if service_name not in filtered_results:
                filtered_results[service_name] = {
                    'regions':[],
                    'ip_prefixes':[]
                }
            
            # get the data structure that stores the results for this service/region combination
            service_stats = filtered_results[service_name]

            # add the region if it is not present in the current record
            if region not in service_stats["regions"]:
                service_stats["regions"].append(region)
            
            # add the unique IP prefix
            service_stats['ip_prefixes'].append(ip_prefix)

# printing the results, you can add your own additional firewall automation starting here
print(json.dumps(filtered_results, indent=4, sort_keys=True))
