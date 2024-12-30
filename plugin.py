import unreal
import os
import time

"""
Diese Werte müssen manuell geändert werden:

TEXTURE_FOLDER: Der Pfad im Unreal Engine Projektordner, in den die Texturen importiert werden sollen.
LOCAL_TEXTURE_PATH: Der lokale Pfad, in dem die von TextureLab (texturelab.py) generierten Texturen gespeichert werden.
RESOLUTION: Die Auflösung der Texturen, die importiert werden sollen.
"""

# Unreal Engine-konforme Pfade
TEXTURE_FOLDER = "/Game/Textures"  # Unreal Engine Zielordner
LOCAL_TEXTURE_PATH = "F:/texturecreator/output_textures/"  # Lokaler Output-Ordner
RESOLUTION = "2K"  # Ändere je nach Auflösung

def import_textures():
    """
    Importiert Texturen aus dem lokalen Output-Ordner in den Unreal Engine Projektordner.

    Der Unreal Engine Projektordner ist der Ordner, in dem alle Assets und Ressourcen für ein Unreal Engine Projekt gespeichert werden.
    Der Texture Output Ordner ist der lokale Ordner, in dem die von TextureLab (texturelab.py) generierten Texturen gespeichert werden.
    """
    print("Starte Import der Texturen...")

    # Definiert die Dateinamen der Texturen basierend auf der Auflösung
    texture_files = {
        "normal": "normal_map_{}.png".format(RESOLUTION),
        "specular": "specular_map_{}.png".format(RESOLUTION),
        "ao": "ao_map_{}.png".format(RESOLUTION),
        "metallic": "metallic_map_{}.png".format(RESOLUTION),
        "emission": "emission_map_{}.png".format(RESOLUTION),
        "opacity": "opacity_map_{}.png".format(RESOLUTION),
        "roughness": "roughness_map_{}.png".format(RESOLUTION),
    }

    tasks = []
    for texture_type, filename in texture_files.items():
        # Erstellt den vollständigen Pfad zur Texturdatei
        full_path = os.path.join(LOCAL_TEXTURE_PATH, filename).replace("\\", "/")
        if not os.path.exists(full_path):
            print("Datei fehlt: {}".format(full_path))
            continue

        try:
            # Erstellt einen Import-Task für die Texturdatei
            task = unreal.AssetImportTask()
            task.filename = full_path
            task.destination_path = TEXTURE_FOLDER
            task.automated = True
            task.replace_existing = True
            tasks.append(task)
            print("Task erstellt für: {}".format(full_path))
        except Exception as e:
            print("Fehler beim Erstellen des Tasks: {}".format(e))

    if tasks:
        try:
            # Importiert die Texturen in Unreal Engine
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
            print("Texturen wurden importiert!")

            # Debug-Ausgabe: Überprüfe, ob die Texturen geladen werden können
            for texture_type, filename in texture_files.items():
                asset_name = filename.split(".")[0]  # Entfernt .png
                asset_path = "/Game/Textures/{}".format(asset_name)
                if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
                    print("Textur erfolgreich importiert: {}".format(asset_path))
                else:
                    print("Textur nicht gefunden: {}".format(asset_path))

        except Exception as e:
            print("Fehler beim Importieren der Texturen: {}".format(e))
    else:
        print("Keine gültigen Texturen gefunden.")

def create_material():
    """
    Erstellt ein neues Material in Unreal Engine und fügt die importierten Texturen hinzu.
    """
    print("Erstelle Material...")

    try:
        # Neues Material erstellen
        material_factory = unreal.MaterialFactoryNew()

        # Erstellt einen eindeutigen Namen für das Material basierend auf der aktuellen Zeit
        material_name = "GeneratedMaterial_{}".format(int(time.time()))

        # Definiert den Pfad für das neue Material
        material_path = TEXTURE_FOLDER + "/" + material_name
        material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(material_name, TEXTURE_FOLDER, None, material_factory)

        if not material:
            print("Material konnte nicht erstellt werden!")
            return

        print("Material erstellt: {}".format(material.get_path_name()))

        # Material laden und bearbeiten
        editor_asset_lib = unreal.EditorAssetLibrary()
        material = editor_asset_lib.load_asset(material_path)

        if not material:
            print("Material konnte nicht geladen werden!")
            return

        print("Material erfolgreich geladen.")

        # Normal Map hinzufügen
        normal_map = editor_asset_lib.load_asset(TEXTURE_FOLDER + "/normal_map_{}.png".format(RESOLUTION))
        if not normal_map:
            print("Normal Map nicht gefunden: {}/normal_map_{}.png".format(TEXTURE_FOLDER, RESOLUTION))
            return

        # Erstellt einen Material-Expression für die Normal Map
        normal_expression = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionTextureSample, -400, 0)
        normal_expression.texture = normal_map
        unreal.MaterialEditingLibrary.connect_material_property(normal_expression, "RGB", unreal.MaterialProperty.MP_NORMAL)

        print("Normal Map erfolgreich hinzugefügt.")

        # Specular Map hinzufügen (Beispiel für weitere Texturen)
        specular_map = editor_asset_lib.load_asset(TEXTURE_FOLDER + "/specular_map_{}.png".format(RESOLUTION))
        if specular_map:
            # Erstellt einen Material-Expression für die Specular Map
            specular_expression = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionTextureSample, -400, -200)
            specular_expression.texture = specular_map
            unreal.MaterialEditingLibrary.connect_material_property(specular_expression, "RGB", unreal.MaterialProperty.MP_SPECULAR)
            print("Specular Map erfolgreich hinzugefügt.")

        # Speichern
        unreal.EditorAssetLibrary.save_loaded_asset(material)
        print("Material wurde gespeichert: {}".format(material.get_path_name()))

    except Exception as e:
        print("Fehler beim Erstellen des Materials: {}".format(e))

# Ausführen
print("Starte Textur-Import...")
import_textures()

print("Erstelle Material...")
create_material()
