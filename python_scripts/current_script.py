from bpy import ops, context, data
import numpy as np


# UTILS
def randomize_light(x, y, z, undo_random=False):
    x = x * 15
    y = y * 15
    z = z * 10
    if undo_random:
        x = -x
        y = -y
        z = -z

    light_object = data.objects["Luz"]
    light_object.select_set(True)
    context.view_layer.objects.active = light_object
    ops.transform.translate(value=(x, y, z), orient_type='GLOBAL',
                            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True,
                            use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1,
                            use_proportional_connected=False, use_proportional_projected=False)

    light_object.select_set(False)


def randomize_object_of_interest(x, y, rot, undo_random=False):
    rot = rot * 5
    x = x * 1e-1
    y = y * 1e-1

    if undo_random:
        rot = -rot
        x = -x
        y = -y

    pcb_collection = data.collections.get("Placa")
    for obj in pcb_collection.objects:
        obj.select_set(True)

        ops.transform.rotate(value=rot, orient_axis='Z', orient_type='GLOBAL',
                             orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                             orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True,
                             use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1,
                             use_proportional_connected=False, use_proportional_projected=False)

        ops.transform.translate(value=(x, y, 0), orient_type='GLOBAL',
                                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=True,
                                use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1,
                                use_proportional_connected=False, use_proportional_projected=False)

        obj.select_set(False)


blend_file = "camera_tracking.blend"
blend_folder = "/home/ribeiro-desktop/blender_experiments/blend_files/"
render_folder = "/home/ribeiro-desktop/blender_experiments/render_results/"
ops.wm.open_mainfile(filepath=blend_folder + blend_file)

# Set camera
context.scene.camera = data.objects["Camera"]

for i in range(5):
    context.scene.render.filepath = render_folder + str(i) + "_labeled_"
    r = np.random.random(6)
    # r = np.asarray([i] * 6)
    r = r - 0.5
    # Change light position
    randomize_light(r[0], r[1], r[2])

    # Rotate PCB
    randomize_object_of_interest(r[3], r[4], r[5])

    # Nodes and renders
    nodes = data.scenes[0].node_tree.nodes
    file_output_node = nodes["File Output"]
    file_output_node.file_slots[0].path = str(i) + "_original"
    ops.render.render(write_still=True, use_viewport=True)

    # Move everything back to where they were
    randomize_light(r[0], r[1], r[2], undo_random=True)
    randomize_object_of_interest(r[3], r[4], r[5], undo_random=True)