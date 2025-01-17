# Unreal Engine Plugin Script (`UE_plugin_script.py`)

## **Beschreibung**
Das `UE_plugin_script.py` ermöglicht die einfache Integration von generierten Texturen in ein Unreal Engine Projekt. Es importiert automatisch Texturen aus einem definierten Ordner und erstellt ein grundlegendes Material. Dieses Plugin bietet eine automatisierte Lösung, die den manuellen Aufwand reduziert und den Workflow beschleunigt.

---

## **Inhaltsübersicht**
- [Beschreibung](#beschreibung)
- [Voraussetzungen](#voraussetzungen)
- [Schritt-für-Schritt Anleitung](#schritt-für-schritt-anleitung)
  - [Aktivierung des Python Plugins](#1-aktivierung-des-python-plugins-in-unreal-engine)
  - [Platzierung des Skripts](#2-platzierung-des-skripts)
  - [Ausführen des Skripts](#3-ausführen-des-skripts)
- [Skript-Funktionalitäten](#4-skript-funktionalitäten)
  - [Texturen importieren](#texturen-importieren)
  - [Material erstellen](#material-erstellen)
- [Konfiguration](#konfiguration)
- [Bekannte Probleme](#bekannte-probleme)
- [Vorteile des Skripts](#vorteile-des-skripts)
- [Beispiel für eine Ordnerstruktur](#beispiel-für-eine-ordnerstruktur)
- [FAQ](#faq)
- [Anpassungen und Erweiterungen](#anpassungen-und-erweiterungen)
- [Autor](#autor)

---

## **Voraussetzungen**
1. Unreal Engine (Version 4.26 oder höher empfohlen).
2. Aktiviertes **Python Editor Script Plugin**.
![image](https://github.com/user-attachments/assets/67ba7818-ed8f-429e-a888-800c7aa9ddf0)

3. Python 3.x (für externe Skript-Ausführungen).
4. Ordner mit generierten Texturen (z. B. aus TextureLab).

---

## **Schritt-für-Schritt Anleitung**

### **1. Aktivierung des Python Plugins in Unreal Engine**
- Öffne Unreal Engine.
- Navigiere zu **Edit > Plugins**.

- Suche nach `Python` und aktiviere das **Python Editor Script Plugin**.
- Starte Unreal Engine neu, um die Änderungen zu übernehmen.

![image](https://github.com/user-attachments/assets/4f062248-124b-492e-9a65-fd356a487bdc)

---

### **2. Platzierung des Skripts**
- Kopiere `UE_plugin_script.py` in dein Unreal-Projektverzeichnis oder einen leicht zugänglichen Pfad.

---

### **3. Ausführen des Skripts**
- Gehe zu **Window > Developer Tools > Output Log**, um die Konsole zu öffnen.

![image](https://github.com/user-attachments/assets/128bef23-ee6d-476c-8d0b-c64f3d95a27f)

- Lade das Skript über den Menüpunkt:

![image](https://github.com/user-attachments/assets/5e56fdd2-23f8-4c8f-a0d7-86ee511fd7ee)

---

### **4. Skript-Funktionalitäten**
#### **Texturen importieren**
Das Skript sucht in einem definierten Ordner (`LOCAL_TEXTURE_PATH`) nach folgenden Texturen:
- Normal Map (`normal_map_X.png`)
- Specular Map (`specular_map_X.png`)
- Ambient Occlusion Map (`ao_map_X.png`)
- Metallic Map (`metallic_map_X.png`)
- Emission Map (`emission_map_X.png`)
- Opacity Map (`opacity_map_X.png`)
- Roughness Map (`roughness_map_X.png`)

Die Texturen werden in das Unreal Engine Projekt (`TEXTURE_FOLDER`) importiert.

#### **Material erstellen**
- Das Skript erstellt ein leeres Material namens `GeneratedMaterial` im Unreal Engine Projekt.
- Das Material kann später manuell im Unreal Material Editor angepasst werden.

---

## **Konfiguration**
Im Skript können folgende Parameter angepasst werden:
- **`TEXTURE_FOLDER`**: Zielordner in Unreal Engine, z. B.:
  ```python
  TEXTURE_FOLDER = "/Game/Textures"
  ```
- **`LOCAL_TEXTURE_PATH`**: Lokaler Pfad zum Ordner mit den generierten Texturen:
  ```python
  LOCAL_TEXTURE_PATH = "F:/texturecreator/output_textures/"
  ```
- **`RESOLUTION`**: Die Auflösung der Texturen, z. B. `2K`, `4K` oder `8K`:
  ```python
  RESOLUTION = "2K"
  ```

---

## **Bekannte Probleme**
- **Fehlende Texturen:** Wenn eine Datei nicht im Ordner vorhanden ist, wird diese Textur übersprungen und im Unreal Content Browser nicht importiert.
- **Material bleibt leer:** Das Skript erstellt das Material, fügt jedoch keine Texturen hinzu. Dies ist gewollt, da eine manuelle Anpassung im Unreal Material Editor flexibler ist.

---

## **Vorteile des Skripts**
- Reduziert den manuellen Import von Texturen.
- Bietet eine Grundlage für die Materialerstellung.
- Kompatibel mit verschiedenen Auflösungen und Unreal Engine Versionen.

---

## **Beispiel für eine Ordnerstruktur**
**Lokaler Texturen-Ordner (LOCAL_TEXTURE_PATH):**
```
F:/texturecreator/output_textures/
│
├── normal_map_2K.png
├── specular_map_2K.png
├── ao_map_2K.png
├── metallic_map_2K.png
├── emission_map_2K.png
├── opacity_map_2K.png
└── roughness_map_2K.png
```

**Unreal Engine Projekt-Ordner (TEXTURE_FOLDER):**
```
/Game/Textures/
```

---

### **FAQ**
**Q: Warum wird mein Material nicht automatisch mit Texturen verbunden?**  
A: Das Skript erstellt ein leeres Material. Du kannst die Texturen manuell im Material Editor hinzufügen, um die volle Kontrolle über die Materialgestaltung zu behalten.

**Q: Welche Unreal Engine-Version wird unterstützt?**  
A: Das Skript wurde mit Unreal Engine 4.26+ getestet und sollte mit neueren Versionen kompatibel sein.

**Q: Warum wird eine meiner Texturen nicht importiert?**  
A: Stelle sicher, dass die entsprechenden Dateien im Ordner `LOCAL_TEXTURE_PATH` vorhanden sind. Fehlende Dateien werden im Log vermerkt und übersprungen.

---

## **Anpassungen und Erweiterungen**
Das Skript kann weiterentwickelt werden, um:
- Automatisierte Verbindungen von Texturen in das Material herzustellen.
- Eine UI für die Skriptausführung in Unreal Engine zu bieten.
- Unterstützung für weitere Material-Properties hinzuzufügen.

---

### **Autor**
Ralf Krümmel  
*Innovative Tools für Game-Entwicklung und Texturerstellung.*
