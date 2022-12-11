# Hadoop Core Cluster Configuration



## Pros

- Easy to install.
- Good for running and debugging purposes.
- Beginner friendly.
- Setup does not take much time, some can focus on logic and application development.
## Cons:
- Cannot handle large set of data.
- One cannot experience cluster-based architecture.

Follow below steps for configuration 

- Create a GCP account.
- Enable VM instance API: API & Services -> Enable API & Services -> First time it will ask to enable VM Instances
- An VM instance will be created under Compute Engine -> VM Instances
- Go to Create Instance (this will be our master node) -> Here specify the configuration for Image:
- Name: User Defined
- Region and Zone: Location near to User as per requirement
- Machine configuration: N1
- Machine Type: n1-standard-4 (we can choose this as per project
requirement, in our case we are handling huge amount of data, so we
chose 4 virtual CPUs)
- Change Boot disk configuration: (User centric)
- Operating System: CentOS
- Boot Disk Type: Standard Persistent disk
- Allow Firewall: Allow HTTP traffic and Allow HTTPS traffic, in order to
access Cloudera Manager UI.
- Advanced options: Not required in our case.
- Create instance by clicking on "create.” 



      0  sudo passwd
      1  cd /
      2  clear
      3  sudo systemctl stop firewalld
      4  sudo systemctl disable firewalld
      5  vi /etc/selinux/config
      6  setenforce 0
      7  echo "never" > /sys/kernel/mm/transparent_hugepage/enabled
      8  file=/etc/ssh/sshd_config
      9  cp -p $file $file.old && awk ' $1=="PermitRootLogin" {$2="yes"} $1=="PasswordAuthentication" {$2="yes"} $1=="PubkeyAuthentication" {$1="PubkeyAuthentication"} {print} ' $file.old > $file
      10  yum install ntp -y
      11  systemctl start ntpd
      12  systemctl enable ntpd
      13  vi /etc/sysctl.conf
      14  yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel make -y
      17  cd /opt/
      18  curl -O https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz
      19  tar -zxvf Python-3.7.11.tgz
      20  cd /opt/Python-3.7.11
      21  ./configure --enable-shared --prefix=/usr/bin
      22 
      23  make install
      24  cp --no-clobber ./libpython3.7.so* /lib64/
      25  chmod 755 /lib64/libpython3.7.so*
      26  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/