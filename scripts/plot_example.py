import h5py
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np

view_output = True
output_type ="cs"

output_map = { "pfss" : {"dn" : "potential_field_source_surface",
                         "in" : "br_input.h5"},
               "cs" : {"dn" : "potential_field_current_sheet",
                         "in" : "br_rss.h5"}
}

f = h5py.File(f'../examples/{output_map[output_type]["dn"]}/{output_map[output_type]["in"]}', 'r')

data = f["Data"]

# theta, phi = np.meshgrid(f["dim1"], f["dim2"])
data_range = (
    f["dim2"][:].min(),
    f["dim2"][:].max(),
    f["dim1"][:].max(),
    f["dim1"][:].min(),
)


if view_output:
  sol_br = h5py.File(f'../examples/{output_map[output_type]["dn"]}/br_{output_type}.h5', 'r')
  sol_bp = h5py.File(f'../examples/{output_map[output_type]["dn"]}/bp_{output_type}.h5', 'r')
  sol_bt = h5py.File(f'../examples/{output_map[output_type]["dn"]}/bt_{output_type}.h5', 'r')

  data_range_sol = (
      sol_br["dim3"][:].min(),
      sol_br["dim3"][:].max(),
      sol_br["dim2"][:].max(),
      sol_br["dim2"][:].min(),
  )

  slice_index = 131

  # theta, phi = np.meshgrid(f["dim1"], f["dim2"])

  fig, axs = plt.subplots(nrows=4, ncols=1)
  fig.suptitle(f'POT3D info: {output_type}')
  row_i = 0
  images = []
  axs[row_i].set_title("Input map")
  input_im = axs[row_i].imshow(np.transpose(data), extent=data_range)
  axs[row_i].label_outer()
  fig.colorbar(input_im, ax=axs[0])

  axs[1].set_title("$B_r$")
  br_im = axs[1].imshow(np.transpose(sol_br["Data"][:, :, slice_index]),
      extent=data_range_sol,
  )
  axs[1].label_outer()
  fig.colorbar(br_im, ax=axs[1])

  axs[2].set_title("$B_{\\theta}$")
  bt_im = axs[2].imshow(np.transpose(sol_bt["Data"][:, :, slice_index]),
      extent=data_range_sol,
  )
  axs[2].label_outer()
  fig.colorbar(bt_im, ax=axs[2])

  axs[3].set_title("$B_{\\phi}$")
  bp_im = axs[3].imshow(np.transpose(sol_bp["Data"][:, :, slice_index]),
      extent=data_range_sol,
  )
  axs[3].label_outer()
  fig.colorbar(bp_im, ax=axs[3])

else:

  fig, ax = plt.subplots()
  ax.set_title("Input map")
  ax.imshow(np.transpose(data), extent=data_range)

plt.show()

