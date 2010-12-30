#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2010, Bryan Davis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright notice, 
#     this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright 
#     notice, this list of conditions and the following disclaimer in the 
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
"""Utitlities for dealing with ip addresses.

  Functions:
    - validate_ip: Validate a dotted-quad ip address.
    - ip2long: Convert a dotted-quad ip address to a network byte order 32-bit 
      integer.
    - long2ip: Convert a network byte order 32-bit integer to a dotted quad ip 
      address.
    - ip2hex: Convert a dotted-quad ip address to a hex encoded network byte
      order 32-bit integer.
    - hex2ip: Convert a hex encoded network byte order 32-bit integer to a
      dotted-quad ip address.
    - validate_cidr: Validate a CIDR notation ip address.
    - cidr2block: Convert a CIDR notation ip address into a tuple containing 
      network block start and end addresses.

  Objects:
    - IpRange: Range of ip addresses providing ``in`` and iteration.
    - IpRangeList: List of IpRange objects providing ``in`` and iteration.


  The IpRangeList object can be used in a django settings file to allow CIDR 
  notation and/or (start, end) ranges to be used in the INTERNAL_IPS list.

  Example:
    INTERNAL_IPS = IpRangeList(
        '127.0.0.1',
        '192.168/16',
        ('10.0.0.1', '10.0.0.19'),
        )

"""
__version__ = '0.5.0-dev'

__all__ = (
        'validate_ip', 'ip2long', 'long2ip', 'ip2hex', 'hex2ip',
        'validate_cidr', 'cidr2block',
        'IpRange', 'IpRangeList',
        )

import re


# sniff for python2.x / python3k compatibility "fixes'
try:
    basestring = basestring
except NameError:
    # 'basestring' is undefined, must be python3k
    basestring = str


try:
    next = next
except NameError:
    # builtin next function doesn't exist
    def next (iterable):
        return iterable.next()


_DOTTED_QUAD_RE = re.compile(r'^(\d{1,3}\.){0,3}\d{1,3}$')

def validate_ip (s):
    """Validate a dotted-quad ip address.

    The string is considered a valid dotted-quad address if it consists of 
    one to four octets (0-255) seperated by periods (.).


    >>> validate_ip('127.0.0.1')
    True

    >>> validate_ip('127.0')
    True

    >>> validate_ip('127.0.0.256')
    False

    >>> validate_ip(None)
    Traceback (most recent call last):
        ...
    TypeError: expected string or buffer


    Args:
        s: String to validate as a dotted-quad ip address
    Returns:
        True if str is a valid dotted-quad ip address, False otherwise
    """
    if _DOTTED_QUAD_RE.match(s):
        quads = s.split('.')
        for q in quads:
            if int(q) > 255:
                return False
        return True
    return False
#end validate_ip

_CIDR_RE = re.compile(r'^(\d{1,3}\.){0,3}\d{1,3}/\d{1,2}$')

def validate_cidr (s):
    """Validate a CIDR notation ip address.

    The string is considered a valid CIDR address if it consists of one to 
    four octets (0-255) seperated by periods (.) followed by a forward slash 
    (/) and a bit mask length (1-32).


    >>> validate_cidr('127.0.0.1/32')
    True

    >>> validate_cidr('127.0/8')
    True

    >>> validate_cidr('127.0.0.256/32')
    False

    >>> validate_cidr('127.0.0.0')
    False

    >>> validate_cidr(None)
    Traceback (most recent call last):
        ...
    TypeError: expected string or buffer


    Args:
        str: String to validate as a CIDR ip address
    Returns:
        True if str is a valid CIDR address, False otherwise
    """
    if _CIDR_RE.match(s):
        ip, mask = s.split('/')
        if validate_ip(ip):
            if int(mask) > 32:
                return False
        else:
            return False
        return True
    return False
#end validate_cidr

def ip2long (ip):
    """
    Convert a dotted-quad ip address to a network byte order 32-bit integer.


    >>> ip2long('127.0.0.1')
    2130706433

    >>> ip2long('127.1')
    2130706433

    >>> ip2long('127')
    2130706432

    >>> ip2long('127.0.0.256') is None
    True


    Args:
        ip: Dotted-quad ip address (eg. '127.0.0.1')

    Returns:
        Network byte order 32-bit integer or None if ip is invalid
    """
    if not validate_ip(ip):
        return None
    quads = ip.split('.')
    if len(quads) == 1:
        # only a network quad
        quads = quads + [0, 0, 0]
    elif len(quads) < 4:
        # partial form, last supplied quad is host address, rest is network
        host = quads[-1:]
        quads = quads[:-1] + [0,] * (4 - len(quads)) + host

    lngip = 0
    for q in quads:
        lngip = (lngip << 8) | int(q)
    return lngip
#end ip2long

_MAX_IP = 0xffffffff
_MIN_IP = 0x0

def long2ip (l):
    """
    Convert a network byte order 32-bit integer to a dotted quad ip address.


    >>> long2ip(2130706433)
    '127.0.0.1'

    >>> long2ip(_MIN_IP)
    '0.0.0.0'

    >>> long2ip(_MAX_IP)
    '255.255.255.255'

    >>> long2ip(None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for >>: 'NoneType' and 'int'

    >>> long2ip(-1) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected int between 0 and 4294967295 inclusive

    >>> long2ip(374297346592387463875L) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected int between 0 and 4294967295 inclusive

    >>> long2ip(_MAX_IP + 1) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected int between 0 and 4294967295 inclusive


    Args:
        l: Network byte order 32-bit integer
    Returns:
        Dotted-quad ip address (eg. '127.0.0.1')
    """
    if _MAX_IP < l or l < 0:
        raise TypeError("expected int between 0 and %d inclusive" % _MAX_IP)
    return '%d.%d.%d.%d' % (l>>24 & 255, l>>16 & 255, l>>8 & 255, l & 255) 
#end long2ip

def ip2hex (addr):
    """
    Convert a dotted-quad ip address to a hex encoded number.

    >>> ip2hex('0.0.0.1')
    '00000001'
    >>> ip2hex('127.0.0.1')
    '7f000001'
    >>> ip2hex('127.255.255.255')
    '7fffffff'
    >>> ip2hex('128.0.0.1')
    '80000001'
    >>> ip2hex('128.1')
    '80000001'
    >>> ip2hex('255.255.255.255')
    'ffffffff'

    """
    netip = ip2long(addr)
    if netip is None:
        return None
    return "%08x" % netip
#end ip2hex

def hex2ip (hex_str):
    """
    Convert a hex encoded integer to a dotted-quad ip address.

    >>> hex2ip('00000001')
    '0.0.0.1'
    >>> hex2ip('7f000001')
    '127.0.0.1'
    >>> hex2ip('7fffffff')
    '127.255.255.255'
    >>> hex2ip('80000001')
    '128.0.0.1'
    >>> hex2ip('ffffffff')
    '255.255.255.255'

    """
    try:
        netip = int(hex_str, 16)
    except ValueError:
        return None
    return long2ip(netip)
#end hex2ip

def cidr2block (cidr):
    """
    Convert a CIDR notation ip address into a tuple containing the network 
    block start and end addresses.


    >>> cidr2block('127.0.0.1/32')
    ('127.0.0.1', '127.0.0.1')

    >>> cidr2block('127/8')
    ('127.0.0.0', '127.255.255.255')

    >>> cidr2block('127.0.1/16')
    ('127.0.0.0', '127.0.255.255')

    >>> cidr2block('127.1/24')
    ('127.1.0.0', '127.1.0.255')

    >>> cidr2block('127.0.0.3/29')
    ('127.0.0.0', '127.0.0.7')

    >>> cidr2block('127/0')
    ('0.0.0.0', '255.255.255.255')


    Args:
        cidr: CIDR notation ip address (eg. '127.0.0.1/8')
    Returns:
        Tuple of block (start, end) or None if invalid
    """
    if not validate_cidr(cidr):
        return None

    ip, prefix = cidr.split('/')
    prefix = int(prefix)

    # convert dotted-quad ip to base network number
    # can't use ip2long because partial addresses are treated as all network 
    # instead of network plus host (eg. '127.1' expands to '127.1.0.0')
    quads = ip.split('.')
    baseIp = 0
    for i in range(4):
        baseIp = (baseIp << 8) | int(len(quads) > i and quads[i] or 0)

    # keep left most prefix bits of baseIp
    shift = 32 - prefix
    start = baseIp >> shift << shift

    # expand right most 32 - prefix bits to 1
    mask = (1 << shift) - 1
    end = start | mask
    return (long2ip(start), long2ip(end))
#end cidr2block

class IpRange (object):
    """
    Range of ip addresses.

    Converts a CIDR notation address, tuple of ip addresses or start and end 
    addresses into a smart object which can perform ``in`` and ``not in`` 
    tests and iterate all of the addresses in the range.


    >>> r = IpRange('127.0.0.1', '127.255.255.255')
    >>> '127.127.127.127' in r
    True

    >>> '10.0.0.1' in r
    False

    >>> 2130706433 in r
    True

    >>> r = IpRange('127/24')
    >>> print(r)
    ('127.0.0.0', '127.0.0.255')

    >>> r = IpRange('127/30')
    >>> for ip in r:
    ...     print(ip)
    127.0.0.0
    127.0.0.1
    127.0.0.2
    127.0.0.3

    >>> print(IpRange('127.0.0.255', '127.0.0.0'))
    ('127.0.0.0', '127.0.0.255')
    """
    def __init__ (self, start, end=None):
        """
        Args:
            start: Ip address in dotted quad format or CIDR notation or tuple 
                of ip addresses in dotted quad format
            end: Ip address in dotted quad format or None
        """
        if end is None:
            if isinstance(start, tuple):
                # occurs when IpRangeList calls via map to pass start and end
                start, end = start

            elif validate_cidr(start):
                # CIDR notation range
                start, end = cidr2block(start)

            else:
                # degenerate range
                end = start

        start = ip2long(start)
        end = ip2long(end)
        self.startIp = min(start, end)
        self.endIp = max(start, end)
    #end __init__

    def __repr__ (self):
        """
        >>> print(IpRange('127.0.0.1'))
        ('127.0.0.1', '127.0.0.1')

        >>> print(IpRange('10/8'))
        ('10.0.0.0', '10.255.255.255')

        >>> print(IpRange('127.0.0.255', '127.0.0.0'))
        ('127.0.0.0', '127.0.0.255')
        """
        return (long2ip(self.startIp), long2ip(self.endIp)).__repr__()
    #end __repr__

    def __contains__ (self, item):
        """
        Implements membership test operators `in` and `not in` for the address 
        range.


        >>> r = IpRange('127.0.0.1', '127.255.255.255')
        >>> '127.127.127.127' in r
        True

        >>> '10.0.0.1' in r
        False

        >>> 2130706433 in r
        True

        >>> 'invalid' in r
        Traceback (most recent call last):
            ...
        TypeError: expected dotted-quad ip address or 32-bit integer


        Args:
            item: Dotted-quad ip address
        Returns:
            True if address is in range, False otherwise
        """
        if isinstance(item, basestring):
            item = ip2long(item)
        if type(item) not in [type(1), type(_MAX_IP)]:
            raise TypeError(
                "expected dotted-quad ip address or 32-bit integer")

        return self.startIp <= item <= self.endIp
    #end __contains__

    def __iter__ (self):
        """
        Return an iterator over the range.


        >>> iter = IpRange('127/31').__iter__()
        >>> next(iter)
        '127.0.0.0'
        >>> next(iter)
        '127.0.0.1'
        >>> next(iter)
        Traceback (most recent call last):
            ...
        StopIteration
        """
        i = self.startIp
        while i <= self.endIp:
            yield long2ip(i)
            i += 1
    #end __iter__
#end class IpRange

class IpRangeList (object):
    """
    List of IpRange objects.

    Converts a list of dotted quad ip address and/or CIDR addresses into a 
    list of IpRange objects. This list can perform ``in`` and ``not in`` tests 
    and iterate all of the addresses in the range.

    This can be used to convert django's conf.settings.INTERNAL_IPS list into 
    a smart object which allows CIDR notation.


    >>> INTERNAL_IPS = IpRangeList('127.0.0.1','10/8',('192.168.0.1','192.168.255.255'))
    >>> '127.0.0.1' in INTERNAL_IPS
    True
    >>> '10.10.10.10' in INTERNAL_IPS
    True
    >>> '192.168.192.168' in INTERNAL_IPS
    True
    >>> '172.16.0.1' in INTERNAL_IPS
    False
    """
    def __init__ (self, *args):
        self.ips = tuple(map(IpRange, args))
    #end __init__

    def __repr__ (self):
        """
        >>> print(IpRangeList('127.0.0.1', '10/8', '192.168/16'))
        (('127.0.0.1', '127.0.0.1'), ('10.0.0.0', '10.255.255.255'), ('192.168.0.0', '192.168.255.255'))
        """
        return self.ips.__repr__()
    #end __repr__

    def __contains__ (self, item):
        """
        Implements membership test operators `in` and `not in` for the address 
        range.


        >>> r = IpRangeList('127.0.0.1', '10/8', '192.168/16')
        >>> '127.0.0.1' in r
        True

        >>> '10.0.0.1' in r
        True

        >>> 2130706433 in r
        True

        >>> 'invalid' in r
        Traceback (most recent call last):
            ...
        TypeError: expected dotted-quad ip address or 32-bit integer


        Args:
            item: Dotted-quad ip address
        Returns:
            True if address is in range, False otherwise
        """
        for r in self.ips:
            if item in r:
                return True
        return False
    #end __contains__

    def __iter__ (self):
        """
        >>> iter = IpRangeList('127.0.0.1').__iter__()
        >>> next(iter)
        '127.0.0.1'
        >>> next(iter)
        Traceback (most recent call last):
            ...
        StopIteration

        >>> iter = IpRangeList('127.0.0.1', '10/31').__iter__()
        >>> next(iter)
        '127.0.0.1'
        >>> next(iter)
        '10.0.0.0'
        >>> next(iter)
        '10.0.0.1'
        >>> next(iter)
        Traceback (most recent call last):
            ...
        StopIteration
        """
        for r in self.ips:
            for ip in r:
                yield ip
    #end __iter__
#end class IpRangeList

def ipcontrolcid(cid,ip):
    cid = cidr2block(cid)
    cid_start = cid[0].split(".")
    cid_end = cid[1].split(".")
    ipl = ip.split(".")
    if ipl[0] == cid_start[0] and int(ipl[1]) >= int(cid_start[1]) and int(ipl[2]) >= int(cid_start[2]) and int(ipl[3]) >= int(cid_start[3]) and int(ipl[1]) <= int(cid_end[1]) and int(ipl[2]) <= int(cid_end[2]) and int(ipl[3]) <= int(cid_end[3]):
        print cid
        return True
    else:
        return False
    
    

    

def iptools_test ():
    import doctest
    doctest.testmod()
#end iptools_test


IP__LIST = """46.2.0.0/16
46.17.128.0/21
46.20.0.0/20
46.20.144.0/20
46.28.160.0/21
46.28.232.0/21
46.30.176.0/21
46.31.112.0/21
46.31.144.0/21
46.45.128.0/18
46.104.0.0/16
46.106.0.0/16
46.154.0.0/15
46.182.64.0/21
46.254.48.0/21
62.29.0.0/17
62.108.64.0/19
62.244.192.0/18
62.248.0.0/17
77.67.128.0/17
77.72.184.0/21
77.73.216.0/21
77.75.32.0/21
77.75.216.0/21
77.79.64.0/18
77.92.0.0/19
77.92.96.0/19
77.92.128.0/19
77.223.128.0/19
77.245.144.0/20
78.40.224.0/21
78.111.96.0/20
78.135.0.0/17
78.160.0.0/11
79.98.128.0/21
79.99.176.0/21
79.123.128.0/17
79.170.168.0/21
79.171.16.0/21
80.93.208.0/20
80.251.32.0/20
80.253.240.0/20
81.6.64.0/18
81.8.0.0/17
81.21.160.0/20
81.22.96.0/20
81.91.16.0/20
81.91.112.0/20
81.212.0.0/14
82.145.224.0/19
82.150.64.0/19
82.151.128.0/19
82.222.0.0/16
83.66.0.0/16
84.17.64.0/19
84.44.0.0/17
84.51.0.0/18
85.29.0.0/18
85.95.224.0/19
85.96.0.0/12
85.119.32.0/21
85.119.64.0/21
85.153.0.0/16
85.158.96.0/21
85.159.64.0/21
85.159.72.0/21
85.235.64.0/19
86.108.128.0/17
87.251.0.0/19
88.224.0.0/11
89.19.0.0/19
89.106.0.0/19
89.107.224.0/21
89.252.128.0/18
90.158.0.0/15
91.93.0.0/16
91.102.160.0/21
91.142.142.0/24
91.151.80.0/20
91.188.192.0/18
91.191.160.0/20
91.195.138.0/23
91.198.49.0/24
91.198.61.0/24
91.198.124.0/24
91.198.185.0/24
91.198.189.0/24
91.199.73.0/24
91.199.111.0/24
91.199.166.0/24
91.199.191.0/24
91.208.61.0/24
91.208.70.0/24
91.208.199.0/24
91.208.206.0/24
91.212.178.0/24
91.213.1.0/24
91.213.245.0/24
91.213.253.0/24
91.213.254.0/24
91.216.91.0/24
91.216.119.0/24
91.216.148.0/24
91.216.170.0/24
91.216.201.0/24
91.216.223.0/24
91.217.147.0/24
91.217.193.0/24
91.217.238.0/24
91.220.50.0/24
91.220.65.0/24
91.220.182.0/24
91.220.242.0/24
92.42.32.0/21
92.43.80.0/21
92.44.0.0/15
92.61.0.0/20
92.63.0.0/20
93.89.16.0/20
93.89.64.0/20
93.89.224.0/20
93.91.64.0/20
93.93.24.0/21
93.94.192.0/21
93.94.248.0/21
93.95.176.0/21
93.155.0.0/17
93.182.64.0/18
93.184.144.0/20
93.186.112.0/20
93.187.64.0/21
93.187.200.0/21
93.190.120.0/21
93.190.216.0/21
94.54.0.0/15
94.73.128.0/18
94.78.64.0/18
94.79.64.0/18
94.101.80.0/20
94.102.0.0/20
94.102.64.0/20
94.103.32.0/20
94.120.0.0/14
94.138.192.0/19
94.199.32.0/21
94.199.200.0/21
95.0.0.0/12
95.65.128.0/17
95.70.128.0/17
95.128.56.0/21
95.130.168.0/21
95.142.128.0/20
95.173.0.0/19
95.173.160.0/19
95.183.128.0/17
109.232.216.0/21
109.235.248.0/21
178.18.192.0/20
178.22.8.0/21
178.210.160.0/19
178.211.32.0/19
178.211.192.0/19
178.233.0.0/16
178.240.0.0/13
178.250.88.0/21
178.251.40.0/21
188.3.0.0/16
188.38.0.0/16
188.41.0.0/16
188.56.0.0/14
188.64.208.0/21
188.95.144.0/21
188.124.0.0/19
188.125.160.0/19
188.132.128.0/17
193.0.61.0/24
193.23.156.0/24
193.25.124.0/23
193.28.225.0/24
193.34.132.0/23
193.36.0.0/24
193.36.39.0/24
193.36.184.0/24
193.37.135.0/24
193.37.154.0/24
193.41.2.0/23
193.41.225.0/24
193.42.216.0/24
193.58.236.0/24
193.104.13.0/24
193.104.109.0/24
193.104.124.0/24
193.104.130.0/24
193.104.138.0/24
193.104.201.0/24
193.105.78.0/24
193.105.208.0/24
193.105.211.0/24
193.105.234.0/24
193.105.243.0/24
193.108.213.0/24
193.109.134.0/23
193.110.170.0/23
193.110.208.0/21
193.140.0.0/16
193.143.226.0/24
193.150.165.0/24
193.164.9.0/24
193.186.208.0/24
193.188.198.0/23
193.189.142.0/24
193.192.96.0/19
193.200.134.0/24
193.200.170.0/24
193.200.180.0/24
193.200.188.0/24
193.201.128.0/22
193.201.149.192/26
193.201.157.0/25
193.202.18.0/24
193.202.120.0/24
193.218.113.0/24
193.218.200.0/24
193.223.76.0/24
193.243.192.0/19
193.254.228.0/23
193.254.252.0/23
193.255.0.0/16
194.0.130.0/24
194.0.142.0/24
194.0.178.0/24
194.0.202.0/24
194.9.174.0/24
194.24.168.0/23
194.24.224.0/23
194.27.0.0/16
194.29.208.0/21
194.36.160.0/24
194.50.84.0/24
194.50.179.0/24
194.54.32.0/19
194.60.73.0/24
194.69.206.0/24
194.107.22.0/24
194.110.150.0/24
194.110.213.0/24
194.125.232.0/22
194.126.230.0/24
194.140.227.0/24
194.169.253.0/24
194.242.32.0/24
195.8.109.0/24
195.33.192.0/18
195.39.224.0/23
195.46.128.0/19
195.49.216.0/21
195.85.242.0/24
195.85.255.0/24
195.87.0.0/16
195.95.149.0/24
195.95.160.0/24
195.95.179.0/24
195.112.128.0/19
195.114.108.0/23
195.128.32.0/21
195.128.254.0/23
195.137.222.0/23
195.138.222.0/24
195.140.196.0/22
195.142.0.0/16
195.149.85.0/24
195.149.116.0/24
195.155.0.0/16
195.174.0.0/16
195.175.0.0/16
195.177.206.0/23
195.177.230.0/23
195.182.25.0/24
195.182.42.0/24
195.190.20.0/24
195.191.118.0/23
195.200.222.0/24
195.214.128.0/18
195.216.232.0/24
195.226.196.0/24
195.226.221.0/24
195.234.52.0/24
195.234.165.0/24
195.244.32.0/19
195.245.227.0/24
212.2.192.0/19
212.12.128.0/19
212.15.0.0/19
212.29.64.0/18
212.31.0.0/19
212.50.32.0/19
212.57.0.0/19
212.58.0.0/19
212.64.192.0/19
212.65.128.0/19
212.68.32.0/19
212.98.0.0/19
212.98.192.0/18
212.101.96.0/19
212.108.128.0/19
212.109.96.0/19
212.109.224.0/19
212.115.0.0/19
212.125.0.0/19
212.127.96.0/19
212.133.128.0/17
212.146.128.0/17
212.154.0.0/17
212.156.0.0/16
212.174.0.0/16
212.175.0.0/16
212.252.0.0/16
212.253.0.0/16
213.14.0.0/16
213.43.0.0/16
213.74.0.0/16
213.128.64.0/19
213.139.192.0/19
213.139.224.0/19
213.142.128.0/19
213.143.224.0/19
213.144.96.0/19
213.148.64.0/19
213.153.128.0/19
213.153.160.0/19
213.153.192.0/18
213.155.96.0/19
213.161.128.0/19
213.186.128.0/19
213.194.64.0/18
213.211.0.0/19
213.232.0.0/18
213.238.128.0/18
213.243.0.0/19
213.243.32.0/19
213.248.128.0/18
213.254.128.0/19
217.17.144.0/20
217.31.224.0/20
217.31.240.0/20
217.64.208.0/20
217.68.208.0/20
217.78.96.0/20
217.116.192.0/20
217.131.0.0/16
217.169.192.0/20
217.174.32.0/20
217.195.192.0/20"""

def controlIPL(ip):
    for i in   IP__LIST.split("\n"):
        if ipcontrolcid(i,ip):
            return False
    return True



if __name__ == '__main__':
    print controlIPL("212.101.96.3")
