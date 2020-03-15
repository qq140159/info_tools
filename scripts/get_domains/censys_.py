from lib.config import *
import censys.certificates
import censys.ipv4
import censys
import sys

def censys_subdomains(simple_url):  # https://censys.io/
    if None in [censys_api_id, censys_api_secret]:
        sys.stderr.write(
            '[!] Please set your Censys API ID and secret from your environment (CENSYS_API_ID and CENSYS_API_SECRET) or from the command line.\n')
        exit(1)
    try:
        censys_certificates = censys.certificates.CensysCertificates(api_id=censys_api_id,
                                                                     api_secret=censys_api_secret)
        certificate_query = 'parsed.names: %s' % simple_url
        certificates_search_results = censys_certificates.search(certificate_query, fields=['parsed.names'])

        for search_result in certificates_search_results:
            domain = "".join(search_result["parsed.names"])
            if "*" not in domain and domain not in domain_list:
                domain_list.append(domain)
    except Exception as e:
        print(e)
