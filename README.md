This package is used for OSU teststand monitering and software level interlock system.

## Content
* [Package dependency](#package-dependency)
* [Equipments](#equipments)
* [Instructions](#instructions)
* [References](#references)

## Package dependency
- influxDB
- pyvisa

## Equipments
- [Keysight DAQ970](https://www.keysight.com/us/en/assets/9018-04738/user-manuals/9018-04738.pdf?success=true)

## Instructions

### Set up influxDB
This is the database to store DCS data  
Run the following command at once including the last EOF

```
cat <<EOF | sudo tee /etc/yum.repos.d/influxdb.repo
[influxdb]
name = InfluxDB Repository - RHEL \$releasever
baseurl = https://repos.influxdata.com/rhel/\$releasever/\$basearch/stable
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
EOF
```

Install and start influxDB
```
sudo yum install -y influxdb
sudo systemctl start influxdb
influx
...
> create database "dcsDB"
> exit
```

### Set up Grafana
This is a web application to see the contents of influxdb
Run the folowing command at once

```
cat <<EOF | sudo tee /etc/yum.repos.d/grafana.repo
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF
```

Install and start Grafana
```
sudo yum install -y grafana
sudo systemctl start grafana-server
```

## References
- [Keysight SCPI](http://literature.cdn.keysight.com/litweb/pdf/ads2001/esgprog/1prep8.html)
