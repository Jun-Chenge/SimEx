""" Convert wpg out to prop out by inserting misc/xFWHM and misc/yFWHM datasets. """

import sys
import shutil
import h5py
from wpg import Wavefront, wpg_uti_wf


def main(wpg_out):

    # Backup
    backup = wpg_out+".backup"
    shutil.copy2(wpg_out, backup)

    # Load wavefront.
    wavefront = Wavefront()
    wavefront.load_hdf5(wpg_out)

    # Get width from intensity profile.
    fwhm = wpg_uti_wf.calculate_fwhm(wavefront)

    # Carefully insert new datasets.
    try:
        with h5py.File(wpg_out, 'a') as h5_handle:
            misc = h5_handle.create_group("misc")
            misc.create_dataset("xFWHM", data=fwhm["fwhm_x"])
            misc.create_dataset("yFWHM", data=fwhm["fwhm_y"])

    # If anything went wrong, restore the original file and raise.
    except:
        shutil.move(backup,wpg_out)
        raise

    # We only reach this point if everything went well, so can safely remove the backup."
    shutil.remove(backup)

if __name__ == "__main__":
    main(sys.argv[1])
