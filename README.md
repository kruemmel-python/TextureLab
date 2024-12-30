# TextureLab

**TextureLab** ist ein innovatives Python-Programm zur Erstellung von hochauflösenden PBR-Texturen (Physically Based Rendering) mit der Unterstützung von neuronalen Netzwerken. Es ermöglicht die Erzeugung von Normal-, Specular-, Ambient Occlusion- und anderen Texturkarten für 3D-Modelle. Die intuitive Gradio-Oberfläche bietet eine einfache Möglichkeit, Texturen anzupassen und zu exportieren.

---

## Funktionen

- **Neuronale Netzwerk-Unterstützung**: Simulierte neuronale Netzwerke verbessern die Qualität der generierten Texturen.
- **PBR-Texturkarten**: Automatische Generierung von Normal-, Specular-, AO-, Metallic-, Emission-, Opacity- und Roughness-Maps.
- **Flexible Auflösungen**: Unterstützt Auflösungen von HD (1280x720) bis 8K (10670x10670).
- **Anpassbare Parameter**: Passen Sie jede Textur mit intuitiven Reglern an (z. B. Metallic-Intensität, Opacity-Schwellenwert).
- **Gradio-Oberfläche**: Benutzerfreundliches Interface für Textur-Vorschau und Anpassung.

---

## Anforderungen

### Abhängigkeiten
Installieren Sie die benötigten Bibliotheken mit `pip`:

```bash
pip install numpy pillow gradio torch opencv-python
```

### Systemanforderungen
- **Python-Version**: 3.9 oder höher
- **Hardware**: Eine GPU wird empfohlen, insbesondere bei hohen Auflösungen (4K und 8K), um die Verarbeitungsgeschwindigkeit zu verbessern.

---

## Installation

1. **Klonen Sie das Repository:**
   ```bash
   git clone https://github.com/kruemmel-python/TextureLab.git
   cd TextureLab
   ```

2. **Installieren Sie die Abhängigkeiten:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Starten Sie das Programm:**
   ```bash
   python texturelab.py
   ```

---

## Verwendung

1. **Starten Sie das Programm:**
   Nach dem Start öffnet sich die Gradio-Oberfläche im Browser.

2. **Laden Sie ein Bild hoch:**
   - Ziehen Sie eine Textur in das Upload-Feld oder wählen Sie eine Datei aus.

3. **Passen Sie die Parameter an:**
   - Nutzen Sie die Schieberegler und Checkboxen, um die gewünschten Texturparameter einzustellen (z. B. Normal Map Stärke, Metallic-Intensität).

4. **Generieren Sie die Texturen:**
   - Klicken Sie auf `Texturen generieren`, um die Karten zu erstellen. Die Ergebnisse können direkt in der Vorschau angezeigt oder als PNG-Dateien gespeichert werden.

5. **Ergebnisse speichern:**
   - Die generierten Texturen werden im Ordner `output_textures` gespeichert.

---

## Unterstützte Texturkarten

- **Normal Map**: Verleiht 3D-Modellen Struktur und Tiefe.
- **Specular Map**: Kontrolliert die Lichtreflexion auf Oberflächen.
- **Ambient Occlusion Map**: Simuliert Schatten in Vertiefungen und Ecken.
- **Metallic Map**: Bestimmt die metallische Erscheinung.
- **Emission Map**: Fügt leuchtende Bereiche hinzu.
- **Opacity Map**: Bestimmt transparente Bereiche.
- **Roughness Map**: Kontrolliert die Glätte der Oberfläche.

---

## Beispiele

### Vorher (Original):
![image](https://github.com/user-attachments/assets/e9ad4a5b-40af-429d-8cca-06fc1d03cca8)


### Nachher (Generierte Texturen):
![image](https://github.com/user-attachments/assets/481fc52c-fd0c-4fe8-a5ff-178dce4054df)


---

## Architektur

### Hauptmodule:

1. **Neuronale Netzwerke:**
   - Simulation von Knoten und Verbindungen zur Texturverarbeitung.

2. **Textur-Generierung:**
   - Verarbeitung von Bildern in Texturkarten mittels Multiprocessing und Torch.

3. **Gradio-Oberfläche:**
   - Benutzeroberfläche für einfache Bedienung und Vorschau.

### Unterstützte Auflösungen:
| Name     | Auflösung       |
|----------|-----------------|
| HD       | 1280x720        |
| Full HD  | 1920x1080       |
| 2K       | 2048x2048       |
| 4K       | 5760x5760       |
| 8K       | 10670x10670     |
| Cover    | 1024x1024       |


---

## Mitwirken

Beiträge sind willkommen! Bitte erstellen Sie ein Issue oder senden Sie einen Pull-Request.

1. **Forken Sie das Repository**
2. **Erstellen Sie einen neuen Branch:**
   ```bash
   git checkout -b feature-name
   ```
3. **Nehmen Sie Änderungen vor und committen Sie:**
   ```bash
   git commit -m "Beschreibung der Änderungen"
   ```
4. **Erstellen Sie einen Pull-Request**

---

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen finden Sie in der Datei `LICENSE`.

---

## Kontakt

Wenn Sie Fragen oder Vorschläge haben, können Sie mich gerne kontaktieren:
- **GitHub:** [Ralf Krümmel](https://github.com/kruemmel-python)

