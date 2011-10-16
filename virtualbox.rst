Notes on how to set up a virutalbox instance from scratch as far until ezjail-remote can be brought in.

 * configure the first network adapter in host-only mode, this will become ``em0``
 * configure the second network adapter in NAT mode, this will become ``em1``

 As root in the console edit ``/etc/rc.conf`` and add::

    sshd_enable="YES"
    ifconfig_em0="inet 192.168.56.50 netmask 0xffffff00"
    ifconfig_em1="DHCP"
    ipv4_addrs_em0="192.168.56.51-61/32"
    hostname="vm.local"

then::

    mv /etc/ssh/sshd_config{,/sample}


then edit /etc/ssh/sshd_config like so::

    ListenAddress 192.168.56.50
    PermitRootLogin yes
    Subsystem       sftp    /usr/libexec/sftp-server
    UseDNS          no

then::

    passwd
    reboot

You now can log into the VM as root with the given password at 192.168.56.50.
In particular you can bootstrap the VM like so::

    ezjail-remote -H root@192.168.56.50 install


