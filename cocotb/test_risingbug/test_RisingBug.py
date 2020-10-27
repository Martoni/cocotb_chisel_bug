#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  27/10/2020
#-----------------------------------------------------------------------------
#  Copyright (2020)  Armadeus Systems
#-----------------------------------------------------------------------------
""" test_RisingBug
"""

import sys
import cocotb
import logging
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.result import raise_error
from cocotb.result import TestFailure
from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge
from cocotb.triggers import ClockCycles


class TestRisingBug(object):
    CLK_PER = (40, "ns") #25Mhz

    def __init__(self, dut):
        self._dut = dut
        self.log = dut._log
        self.clk = dut.clock
        self.rstn = dut.resetn
        self._clock_thread = cocotb.fork(
                Clock(self.clk, *self.CLK_PER).start())
        self._td = cocotb.fork(
                self.time_display(step=(10, "us")))

    async def time_display(self, step=(1, "us")):
        dtime = 0
        while True:
            self.log.info("t {} {}".format(dtime*step[0], step[1]))
            await Timer(*step)
            dtime += 1

    async def reset(self):
        self.rstn <= 0
        self._dut.pulse <= 0
        await Timer(100, units="ns")
        self.rstn <= 1
        await RisingEdge(self.clk)


@cocotb.test()
async def rising_test(dut):
    trb = TestRisingBug(dut)
    trb.log.info("Begin of test")
    await trb.reset()
    await Timer(340, units="ns")
    dut.pulse <= 1
    await Timer(1499, units="ns")
    dut.pulse <= 0
    await Timer(932, units="ns")
    dut.pulse <= 1
    await Timer(1, units="us")
    dut.pulse <= 0
    await Timer(1, units="us")
    trb.log.info("End of test")
