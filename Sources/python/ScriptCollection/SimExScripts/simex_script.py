##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from SimEx.Parameters.SingFELPhotonDiffractorParameters import SingFELPhotonDiffractorParameters

import pylab

# Define the input path (location of pmi trajectories.)
pmi_path = "pmi/"

# Give path of beam and geom files.
beam = "s2e.beam" # e.g. s2e.beam
geom = "s2e.geom" # e.g. s2e.geom

parameters= SingFELPhotonDiffractorParameters(
             uniform_rotation=True,                   # Uniform sampling of rotation space.
             calculate_Compton = False,               # Do not calculate Compton scattering
             slice_interval = 100,                    # Take interval of 100 pmi snapshots
             number_of_slices = 100,                  # Take two snapshots from this interval
             pmi_start_ID = 1,                        # Start with this pmi file ID.
             pmi_stop_ID  = 1,                        # Stop after this pmi file ID.
             number_of_diffraction_patterns = 1000,   # Calculate 1000 patterns from each trajectory.
             beam_parameter_file = beam,              # Beam file.
             beam_geometry_file = geom,               # Geometry file (detector).
             cpus_per_task = 1,                       # Do one pattern per CPU (round-robin)
             )

# Construct the calculator.
diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=pmi_path, output_path='diffr')

# Call backengine. This will do the actual calculation and load the results.
status = diffractor.backengine()

# Get reference to data.
data = diffractor.data

# Display a simulated pattern.
pylab.imshow(data[10])
