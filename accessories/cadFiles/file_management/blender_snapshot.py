import bpy, math, sys, os
from mathutils import Vector
from pathlib import Path

def findCADFiles(parentDir, ignoreExistingFiles=[".png"]): #returns a list of dicts; dir/fileName
    cadFiles = []
    for root, dirs, files in os.walk(parentDir):
        for file in files:
            stem = os.path.splitext(file)[0]

            if not file.endswith(".FCStd"):
                continue
            if any(f"{stem}.{ext}" in files for ext in ignoreExistingFiles):
                continue

            fileInfo = {
                "dir": root,
                "fileName": file
            }
            cadFiles.append(fileInfo)
        
    return cadFiles


def build_illustration(fileInfo, imageSize=1024, outputType=".png")
    fileDir = fileInfo['dir']
    fileName = fileInfo['fileName']

    inputFilePath = os.path.join(fileDir, fileName)
    outputFilePath = os.path.join(fileDir, outPutFileName)
    outputFileName = f"{fileName}{outputType}"

    CAMERA_DISTANCE = 3.0

    # ---------------------------
    # Reset Blender
    # -----------------------------
    bpy.ops.wm.read_factory_settings(use_empty=True)

    #region blender configs
    # -----------------------------
    # Import model
    # -----------------------------
    bpy.ops.import_scene.gltf(filepath=inputFilePath)

    objects = [
        obj for obj in bpy.context.scene.objects
        if obj.type == "MESH"
    ]

    if not objects:
        raise RuntimeError("No mesh objects imported")

    # -----------------------------
    # Join meshes
    # -----------------------------
    bpy.context.view_layer.objects.active = objects[0]

    for obj in objects:
        obj.select_set(True)

    bpy.ops.object.join()

    model = bpy.context.object
    model.name = "Model"

    # -----------------------------
    # Center model
    # -----------------------------
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")

    bbox = [
        model.matrix_world @ Vector(corner)
        for corner in model.bound_box
    ]

    center = sum(bbox, Vector()) / 8
    model.location -= center


    # -----------------------------
    # Camera
    # -----------------------------
    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)

    bpy.context.collection.objects.link(camera)
    bpy.context.scene.camera = camera

    camera.location = (
        CAMERA_DISTANCE,
        -CAMERA_DISTANCE,
        CAMERA_DISTANCE
    )

    direction = Vector((0,0,0)) - camera.location
    camera.rotation_euler = direction.to_track_quat(
        "-Z", "Y"
    ).to_euler()

    camera.data.lens = 50


    # -----------------------------
    # Lighting
    # -----------------------------
    light_data = bpy.data.lights.new(
        name="Studio Light",
        type="AREA"
    )

    light_data.energy = 500
    light_data.size = 5

    light = bpy.data.objects.new(
        "Studio Light",
        light_data
    )

    light.location = (4,-4,6)
    bpy.context.collection.objects.link(light)


    # -----------------------------
    # Ground/background
    # -----------------------------
    world = bpy.context.scene.world
    world.color = (0.95,0.95,0.95)

    # -----------------------------
    # Render settings
    # -----------------------------

    scene = bpy.context.scene

    scene.render.engine = "BLENDER_EEVEE_NEXT"

    scene.render.resolution_x = imageSize
    scene.render.resolution_y = imageSize
    scene.render.resolution_percentage = 100

    scene.render.image_settings.file_format = "PNG"

    scene.render.filepath = OUTPUT_FILE


    # Transparent if desired:
    # scene.render.film_transparent = True

    #endregion


    bpy.ops.render.render(write_still=True)
    print("Saved:", OUTPUT_FILE)


def generateThumbnails(projectRoot, generateFileType=".png")
    CAD_file_candidates = findCADFiles(projectRoot, ignoreExistingFiles=[generateFileType])

    errorCount = 0
    for cad_file_info in CAD_file_candidates:
        fileName = cad_file_info["fileName"]
        buildStatus = build_illustration(cad_file_info, outputType=generateFileType)
        if not buildStatus:
            print(f"Error when building thumbnail for file {fileName}")
            errorCount += 1
    
    print(f"Successfully built {len(CAD_file_candidates) - errorCount}/{len(CAD_file_candidates)} {generateFileType} thumbnails")
