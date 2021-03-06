# coding:utf-8
import unittest
from datadiff.tools import assert_equal

import vyattaconfparser as vparser


class TestBackupOspfRoutesEdgemax(unittest.TestCase):
    def test_basic_parse_works_a1(self, dos_line_endings=False):
        s = """
        interfaces {
             ethernet eth0 {
                 address 192.168.0.2/24
                 address 192.168.1.2/24
                 description eth0-upstream
                 duplex auto
                 speed auto
                 disable
             }
             ethernet eth1 {
                 address 192.168.2.2/24
                 description eth1-other
                 duplex auto
                 speed auto
             }
        }"""
        if dos_line_endings:
            s = s.replace('\n', '\r\n')
        correct = {
            'interfaces': {
                'ethernet': {
                    'eth0': {
                        'address': {'192.168.0.2/24': {}, '192.168.1.2/24': {}},
                        'description': 'eth0-upstream',
                        'duplex': 'auto',
                        'speed': 'auto',
                        'disable': 'disable'
                    },
                    'eth1': {
                        'address': '192.168.2.2/24',
                        'description': 'eth1-other',
                        'duplex': 'auto',
                        'speed': 'auto'
                    }
                }
            }
        }
        rv = vparser.parse_conf(s)
        assert isinstance(rv, dict)
        assert_equal(correct, rv)

    def test_basic_parse_works_a1_dos_endings(self):
        self.test_basic_parse_works_a1(dos_line_endings=True)

    def test_parsing_quoted_config_vals(self):
        s = """
        interfaces {
             ethernet eth0 {
                 description "eth0-upstream 302.5-19a"
                 duplex auto
                 speed auto
             }
        }"""
        correct = {
            'interfaces': {
                'ethernet': {
                    'eth0': {
                        'description': 'eth0-upstream 302.5-19a',
                        'duplex': 'auto',
                        'speed': 'auto'
                    }
                }
            }
        }
        rv = vparser.parse_conf(s)
        assert isinstance(rv, dict)
        assert_equal(rv, correct)

    def test_parsing_quoted_config_vals_special_chars(self):
        s = """
        interfaces {
             ethernet eth0 {
                 description "eth0-upstream #302.5-19a (temp path)"
                 duplex auto
                 speed auto
             }
        }"""
        correct = {
            'interfaces': {
                'ethernet': {
                    'eth0': {
                        'description': 'eth0-upstream #302.5-19a (temp path)',
                        'duplex': 'auto',
                        'speed': 'auto'
                    }
                }
            }
        }
        rv = vparser.parse_conf(s)
        assert isinstance(rv, dict)
        assert_equal(rv, correct)

    def test_parsing_bgp_ipv6_works(self):
        s = """
        protocols {
            bgp 1 {
                address-family {
                    ipv6-unicast {
                        network 2001:2000:6000::/40 {
                        }
                        network 2001:2060::/32 {
                        }
                    }
                }
                neighbor 10.10.1.2 {
                    remote-as 2
                }
                network 192.168.1.0/24 {
                }
            }
        }"""
        correct = {
            'protocols': {
                'bgp': {
                    '1': {
                        'address-family': {
                            'ipv6-unicast': {
                                'network': {
                                    '2001:2000:6000::/40': {},
                                    '2001:2060::/32': {}
                                }
                            }
                        },
                        'neighbor': {
                            '10.10.1.2': {
                                'remote-as': '2'
                            }
                        },
                        'network': {
                            '192.168.1.0/24': {}
                        }
                    }
                }
            }
        }
        rv = vparser.parse_conf(s)
        assert isinstance(rv, dict)
        assert_equal(correct, rv)

    def test_parsing_new_style_config(self):
        s = """
        system {
            ntp {
                server 0.vyatta.pool.ntp.org
                server 1.vyatta.pool.ntp.org
                server us.pool.ntp.org {
                    prefer {
                    }
                }
                server 2.vyatta.pool.ntp.org
            }
            time-zone Europe/Moscow
            name-server 10.10.2.2
        }"""
        correct = {
            'system': {
                'ntp': {
                    'server': {
                        '0.vyatta.pool.ntp.org': {},
                        '1.vyatta.pool.ntp.org': {},
                        'us.pool.ntp.org': {
                            'prefer': {}
                        },
                        '2.vyatta.pool.ntp.org': {},
                    }
                },
                'time-zone': 'Europe/Moscow',
                'name-server': '10.10.2.2'
            }
        }
        rv = vparser.parse_conf(s)
        assert isinstance(rv, dict)
        assert_equal(correct, rv)

    def test_multiple_values_with_same_key(self):
        s = """
        service {
            ssh {
                address 0.0.0.0 {
                    port 22
                }
                cipher aes128-cbc
                cipher aes192-cbc
                cipher aes256-cbc
                hmac hmac-md5
                hmac hmac-md5-96
                hmac hmac-sha1
                hmac hmac-sha1-96
                key-exchange-algo diffie-hellman-group-exchange-sha1
                key-exchange-algo diffie-hellman-group-exchange-sha256
            }
        }
        """
        correct = {
            'service': {
                'ssh': {
                    'address': {
                        '0.0.0.0': {
                            'port': '22',
                        }
                    },
                    'cipher': {
                        'aes128-cbc': {},
                        'aes192-cbc': {},
                        'aes256-cbc': {},
                    },
                    'hmac': {
                        'hmac-md5': {},
                        'hmac-md5-96': {},
                        'hmac-sha1': {},
                        'hmac-sha1-96': {},
                    },
                    'key-exchange-algo': {
                        'diffie-hellman-group-exchange-sha1': {},
                        'diffie-hellman-group-exchange-sha256': {},
                    }
                }
            }
        }
        rv = vparser.parse_conf(s)
        assert isinstance(rv, dict)
        assert_equal(correct, rv)

if __name__ == "__main__":
    unittest.main()
