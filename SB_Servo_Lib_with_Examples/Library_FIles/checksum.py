#!/usr/bin/python3

"""
This file contains the functions to generate the commands for SBS Servo
interface
Developed by - SB Components
http://sb-components.co.uk
"""


class CheckSum:
    @staticmethod
    def sum_params(params):
        """
        Add parameters
        :param params: add the data parameters
        :return: The addition of parameters
        """
        sum_params = 0
        for para in params:
            sum_params += para
        return sum_params

    @staticmethod
    def checksum_cal(_sum):
        """
        Calculate the Checksum
        :param _sum: the parameters required for Checksum, Hex
        :return: Calculated Checksum Value
        """
        #  Calculate the Checksum
        sum_hex = ~_sum
        check_sum = sum_hex & 0xff
        return check_sum

    def check_sum(self, servo_id, instruction, params=[]):
        """
        :param servo_id: ID of Servo Motor, int(hex)
        :param instruction: Instruction type  #  0x01 - 0x06, 0x83
        :param params: Parameters to pass to Servo eg. position and value, List
        :return: Check sum value in hex
        """
        length = len(params) + 2
        parameter_sum = self.sum_params(params)

        _sum = servo_id + length + instruction + parameter_sum

        check_sum = self.checksum_cal(_sum)

        return check_sum, length


if __name__ == "__main__":
    cs = CheckSum()
    c_sum = cs.check_sum(0x01, 0x03, [0x2A, 0x00, 0x08, 0x00, 0x00, 0xE8,
                                      0x03])
    print(c_sum+1)
