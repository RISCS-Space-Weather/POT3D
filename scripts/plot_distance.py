import h5py
from matplotlib import colors, cm
import matplotlib.pyplot as plt
import numpy as np

view_output = True
output_type ="pfss"

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

  fig, axs = plt.subplots(nrows=3, ncols=1)
  fig.suptitle(f'POT3D info: {output_type}')
  row_i = 0
  images = []
#   axs[row_i].set_title("Input map")
#   input_im = axs[row_i].imshow(np.transpose(data), extent=data_range)
#   axs[row_i].label_outer()
#   fig.colorbar(input_im, ax=axs[0])

  from skimage import measure
  m = sol_br["Data"][:, :, slice_index]
  contours = measure.find_contours(m, 0)
  # print(contours)
  for contour in contours:
    axs[0].plot(contour[:, 0], contour[:, 1], linewidth=2)

  axs[0].set_title("$B_r$")
  br_im = axs[0].imshow(np.transpose(sol_br["Data"][:, :, slice_index]),
    #   extent=data_range_sol,
  )



#   axs[0].axis('image')
 #, colors='white', alpha=0.5)
#   axs[0].plot(contours[0][:,1], contours[0][:,0])

  axs[0].label_outer()
  # fig.colorbar(br_im, ax=axs[0])

  axs[1].set_title("$sign(B_{r})$")
  cmap_iter = iter(cm.get_cmap('tab10').colors)
  sign_cmap = colors.ListedColormap([next(cmap_iter) for i in range(3)])
  br_sign = axs[1].imshow(np.transpose(np.sign(sol_br["Data"][:, :, slice_index])),
      extent=data_range_sol, cmap=sign_cmap, interpolation='none'
  )
  axs[1].label_outer()
  fig.colorbar(br_sign, ax=axs[1], ticks=[-1, 0, 1])

  # from scipy import ndimage
  from skimage import morphology

  # theta = sol_bt["t"][:]
  # phi = sol_bp["p"][:]
  # print(theta.shape, phi.shape, )
  # image = np.transpose(np.sign(sol_br["Data"][:, :, slice_index]))
  image = np.transpose(sol_br["Data"][:, :, slice_index])
  image[image < 0] = 0
  image[image > 0] = 1
  # sobel = ndimage.sobel(image)
  # distance = ndimage.distance_transform_edt(sobel)
  # out, distance = morphology.medial_axis(image, return_distance=True)

  axs[2].set_title("Distance field")
  bp_im = axs[2].imshow(image,
      extent=data_range_sol,
  )
  axs[2].label_outer()
  fig.colorbar(bp_im, ax=axs[2])
else:

  fig, ax = plt.subplots()
  ax.set_title("Input map")
  ax.imshow(np.transpose(data), extent=data_range)

plt.show()

