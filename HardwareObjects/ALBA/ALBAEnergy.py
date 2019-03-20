#  Project: MXCuBE
#  https://github.com/mxcube.
#
#  This file is part of MXCuBE software.
#
#  MXCuBE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  MXCuBE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

"""
[Name] ALBAEnergy

[Description]
HwObj used to configure the beamline energy.

[Signals]
- energyChanged
"""

from __future__ import print_function

import logging

from HardwareRepository.BaseHardwareObjects import Device

__credits__ = ["ALBA Synchrotron"]
__version__ = "2.3"
__category__ = "General"


class ALBAEnergy(Device):

    energy_change_threshold = 0.0002

    def __init__(self, *args):
        Device.__init__(self, *args)

        self.energy_hwobj = None
        self.wavelength_hwobj = None

        self.energy_position = None
        self.wavelength_position = None

    def init(self):
        self.energy_hwobj = self.getObjectByRole("energy")
        self.wavelength_hwobj = self.getObjectByRole("wavelength")

        self.energy_hwobj.connect("positionChanged", self.energy_position_changed)
        self.wavelength_hwobj.connect(
            "positionChanged",
            self.wavelength_position_changed)

    def isReady(self):
        return True

    def can_move_energy(self):
        return True

    def get_energy(self):
        if self.energy_position is None:
            self.energy_position = self.energy_hwobj.getPosition()
        return self.energy_position

    getCurrentEnergy = get_energy

    def get_wavelength(self):
        if self.wavelength_position is None:
            self.wavelength_position = self.wavelength_hwobj.getPosition()
        return self.wavelength_position

    def update_values(self):
        self.energy_hwobj.update_values()

    def energy_position_changed(self, value):
        self.energy_position = value
        if None not in [self.energy_position, self.wavelength_position]:
            self.emit('energyChanged', self.energy_position, self.wavelength_position)

    def wavelength_position_changed(self, value):
        self.wavelength_position = value
        if None not in [self.energy_position, self.wavelength_position]:
            self.emit('energyChanged', self.energy_position, self.wavelength_position)

    def move_energy(self, value):
        current_egy = self.get_energy()

        logging.getLogger("HWR").debug(
            "moving energy to %s. now is %s" %
            (value, current_egy))
        if abs(value-current_egy) > self.energy_change_threshold:
            self.energy_hwobj.move(value)
        else:     
            self.logger.debug("Change below threshold. not moved")

    def wait_move_energy_done(self):
        self.energy_hwobj.wait_end_of_move()

    def move_wavelength(self, value):
        self.wavelength_hwobj.move(value)

    def get_energy_limits(self):
        return self.energy_hwobj.getLimits()

    def getEnergyLimits(self):
        return self.get_energy_limits()

    def get_wavelength_limits(self):
        return self.wavelength_hwobj.getLimits()


def test_hwo(hwo):
    print("Energy is: ", hwo.get_energy())
    print("Wavelength is: ", hwo.get_wavelength())
    print("Energy limits are: ", hwo.get_energy_limits())
    print("Wavelength limits are: ", hwo.get_wavelength_limits())
