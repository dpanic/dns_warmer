# dns_warmer
Purpos of DNS Warmer is to parse dnsmasq logs, extract top N most requested hostnames and requery them every N minutes to keep DNS cache warm.

Software is designed and tested with Pi-hole. 
Good thing is to have /etc/dnsmasq.d/02-pihole.conf

```
cache-size=30000
min-cache-ttl=300
```

## Cronjob
You can set cronjob something like this:

```*/5 * * * * sleep $((RANDOM\%15)) && ionice -c idle nice -19 /bin/bash /home/atomicpi/dns_warmer/devops/dns_warmer.sh  > /dev/null 2>&1```
