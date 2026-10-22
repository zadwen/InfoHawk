"""Bounded DNS lookups, with absence distinguished from lookup failure."""
import dns.exception
import dns.resolver
from modules.utils import domain_name

RECORD_TYPES = ('A', 'AAAA', 'MX', 'NS', 'TXT', 'CAA')


def lookup(domain, resolver=None, record_types=RECORD_TYPES):
    domain = domain_name(domain)
    resolver = resolver or dns.resolver.Resolver()
    records = {}
    for kind in record_types:
        try:
            answer = resolver.resolve(domain, kind, lifetime=4)
            records[kind] = {'status': 'ok', 'values': [r.to_text() for r in answer]}
        except dns.resolver.NXDOMAIN:
            records[kind] = {'status': 'domain_not_found', 'values': []}
            break
        except dns.resolver.NoAnswer:
            records[kind] = {'status': 'no_records', 'values': []}
        except dns.exception.Timeout:
            records[kind] = {'status': 'timeout', 'values': []}
        except (dns.resolver.NoNameservers, dns.exception.DNSException, OSError):
            records[kind] = {'status': 'lookup_failed', 'values': []}
    return {'domain': domain, 'records': records, 'source': 'System DNS resolver'}
