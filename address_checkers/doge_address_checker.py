import json
import requests
from time import sleep
from address_checkers.abs_address_checker import AbsAddressChecker


class DogeAddressChecker(AbsAddressChecker):
    CHAINSO = 'https://chain.so/api/v2/is_address_valid/DOGE/'
    STATUS = 'status'
    SUCCESS = 'success'
    DATA = 'data'
    ISVALID = 'is_valid'

    def address_search(self, addr):
        '''Use chain.so API to check if an address is valid'''
        r = requests.get(DogeAddressChecker.CHAINSO + addr)
        # WARNING: chain.so API give 5request/sec for free
        sleep(0.2)
        resp = r.text
        try:
            jsonResp = json.loads(resp)
            if (jsonResp[DogeAddressChecker.STATUS] ==
                    DogeAddressChecker.SUCCESS):
                return (jsonResp[DogeAddressChecker.DATA]
                        [DogeAddressChecker.ISVALID])
            else:
                return False
        except ValueError:
            return False
        return True

    def address_valid(self, addr):
        return ((len(addr) == 33) and (addr.startswith('D')))

    def address_check(self, addr):
        '''Check if a Doge address is valid'''
        if (self.address_valid(addr)):
            return self.address_search(addr)
        return False
