import bpy

scene = bpy.context.scene

def pass_index_children(obj):
    id=obj.pass_index
    for child in obj.children:
        child.pass_index=id
        pass_index_children(child)

foo_objs = [obj for obj in scene.objects]
id=0
# Set all ids to 0
for obj in foo_objs:
    obj.pass_index=id

# Set only the ids of the objects in Arduino collection and not in Texto
# TODO: Text must be with the same index of PCB? 
id=1
for obj in bpy.data.collections['Arduino'].all_objects:
    if obj.users_collection[0].name != 'Texto':
        obj.pass_index=id
        id+=1

# Set same id to children
for obj in bpy.data.collections['Arduino'].all_objects:
    if obj.users_collection[0].name != 'Texto':
        if len(obj.children)>0:
            pass_index_children(obj)
# TODO: Check if number of IDS is compatible with number of components
