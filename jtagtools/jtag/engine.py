# Copyright (c) 2010-2024, Emmanuel Blot <emmanuel.blot@free.fr>
# Copyright (c) 2016, Emmanuel Bouaziz <ebouaziz@free.fr>
# All rights reserved.
#
# SPDX-License-Identifier: Apache2

"""JTAG engine."""

from logging import getLogger

from ..bits import BitSequence
from .controller import JtagController
from .machine import JtagStateMachine


class JtagEngine:
    """High-level JTAG engine."""

    def __init__(self, ctrl: 'JtagController'):
        self._ctrl = ctrl
        self._log = getLogger('jtag.eng')
        self._fsm = JtagStateMachine()
        self._tr_cache: dict[tuple[str,  # from state
                                   str],  # to state
                             BitSequence] = {}  # TMS sequence
        self._seq = bytearray()

    @property
    def fsm(self) -> JtagStateMachine:
        """Return the state machine."""
        return self._fsm

    @property
    def controller(self) -> 'JtagController':
        """Return the JTAG controller."""
        return self._ctrl

    def reset(self) -> None:
        """Reset the attached TAP controller"""
        self._ctrl.reset()
        self._fsm.reset()

    def get_available_statenames(self):
        """Return a list of supported state name"""
        return [str(s) for s in self._fsm.states]

    def change_state(self, statename) -> BitSequence:
        """Advance the TAP controller to the defined state"""
        transition = (self._fsm.state.name, statename)
        if transition not in self._tr_cache:
            # find the state machine path to move to the new instruction
            path = self._fsm.find_path(statename)
            self._log.debug('new path: %s',
                            ', '.join((str(s).upper() for s in path[1:])))
            # convert the path into an event sequence
            events = self._fsm.get_events(path)
            self._tr_cache[transition] = events
        else:
            # transition already in cache
            events = self._tr_cache[transition]
        # update the remote device tap controller (write TMS consumes the seq)
        bseq = self._ctrl.write_tms(events.copy())
        self._log.debug('change state to %s: %s', statename, bseq)
        # update the current state machine's state
        self._fsm.handle_events(events.copy())
        return bseq

    def go_idle(self) -> None:
        """Change the current TAP controller to the IDLE state"""
        self.change_state('run_test_idle')

    def run(self) -> None:
        """Change the current TAP controller to the IDLE state"""
        self.change_state('run_test_idle')

    def capture_ir(self) -> None:
        """Capture the current instruction from the TAP controller"""
        self.change_state('capture_ir')

    def write_ir(self, instruction: BitSequence) -> None:
        """Change the current instruction of the TAP controller"""
        self.change_state('shift_ir')
        self._ctrl.write(instruction)
        self.change_state('update_ir')

    def capture_dr(self) -> None:
        """Capture the current data register from the TAP controller"""
        self.change_state('capture_dr')

    def write_dr(self, data: BitSequence) -> None:
        """Change the data register of the TAP controller"""
        self.change_state('shift_dr')
        self._ctrl.write(data)
        self.change_state('update_dr')

    def read_dr(self, length: int) -> BitSequence:
        """Read the data register from the TAP controller"""
        self.change_state('shift_dr')
        data = self._ctrl.read(length-1)
        bseq = self.change_state('update_dr')
        data.push_left(bseq.pop_right(1))
        return data

    def exchange_dr(self, data: BitSequence) -> BitSequence:
        """Change the data register of the TAP controller and retrieve
           previous DR content."""
        self.change_state('shift_dr')
        data = self._ctrl.exchange(data)
        self.change_state('update_dr')
        return data