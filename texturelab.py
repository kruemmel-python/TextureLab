import os
import cv2
import numpy as np
from PIL import Image
import gradio as gr
import torch
import random
import multiprocessing

# ---------------------------
# Neuronales Netzwerk-Klassen und Bildverarbeitung
# ---------------------------

class Connection:
    """
    Represents a connection between nodes in a neural network.

    Attributes:
        target_node (Node): The node to which this connection points.
        weight (float): The weight of the connection.
        weight_history (list): A history of the weights for this connection.
    """
    def __init__(self, target_node, weight=None):
        self.target_node = target_node
        self.weight = weight if weight is not None else random.uniform(0.1, 1.0)
        self.weight_history = []

class Node:
    """
    Represents a node in a neural network.

    Attributes:
        label (str): The label of the node.
        connections (list): A list of connections from this node to other nodes.
        activation (float): The current activation level of the node.
        activation_history (list): A history of the activation levels for this node.
    """
    def __init__(self, label):
        self.label = label
        self.connections = []
        self.activation = 0.0
        self.activation_history = []

    def add_connection(self, target_node, weight=None):
        """
        Adds a connection from this node to another node.

        Args:
            target_node (Node): The node to which the connection is made.
            weight (float, optional): The weight of the connection. Defaults to a random value between 0.1 and 1.0.
        """
        self.connections.append(Connection(target_node, weight))

    def propagate_signal(self, input_signal):
        """
        Propagates the input signal through the node and its connections.

        Args:
            input_signal (float): The input signal to the node.
        """
        self.activation = max(0, input_signal)
        self.activation_history.append(self.activation)
        for connection in self.connections:
            connection.target_node.activation += self.activation * connection.weight
            connection.weight_history.append(connection.weight)

class ImageNode(Node):
    """
    Represents a node in a neural network that generates an image.

    Attributes:
        image (torch.Tensor): The generated image.
    """
    def __init__(self, label):
        super().__init__(label)
        self.image = None

    def generate_image(self, category_nodes, original_image):
        """
        Generates an image based on the category nodes and the original image.

        Args:
            category_nodes (list): A list of category nodes.
            original_image (PIL.Image): The original image.
        """
        self.image = self.generate_image_from_categories(category_nodes, original_image)

    def generate_image_from_categories(self, category_nodes, original_image):
        """
        Generates an image from the category nodes and the original image.

        Args:
            category_nodes (list): A list of category nodes.
            original_image (PIL.Image): The original image.

        Returns:
            torch.Tensor: The generated image tensor.
        """
        image_array = np.array(original_image) / 255.0
        image_tensor = torch.tensor(image_array, dtype=torch.float32).permute(2, 0, 1)

        pool = multiprocessing.Pool()
        chunk_size = image_tensor.shape[1] // multiprocessing.cpu_count()
        chunks = [(image_tensor, i, chunk_size, category_nodes) for i in range(0, image_tensor.shape[1], chunk_size)]
        results = pool.map(self.process_chunk, chunks)

        pool.close()
        pool.join()

        for start_row, modified_chunk in results:
            image_tensor[:, start_row:start_row + modified_chunk.shape[1], :] = modified_chunk

        return image_tensor

    def process_chunk(self, args):
        """
        Processes a chunk of the image tensor.

        Args:
            args (tuple): A tuple containing the image tensor, start row, chunk size, and category nodes.

        Returns:
            tuple: A tuple containing the start row and the modified chunk.
        """
        image_tensor, start_row, chunk_size, category_nodes = args
        modified_chunk = image_tensor[:, start_row:start_row + chunk_size, :].clone()
        for x in range(modified_chunk.shape[1]):
            for y in range(modified_chunk.shape[2]):
                pixel = modified_chunk[:, x, y]
                for node in category_nodes:
                    pixel += node.activation * 0.1
                modified_chunk[:, x, y] = torch.clamp(pixel, 0, 1)
        return start_row, modified_chunk

# ---------------------------
# Funktionen zur Texturerzeugung
# ---------------------------

resolutions = {
    "HD": (1280, 720),
    "Full HD": (1920, 1080),
    "2K": (2048, 2048),
    "4K": (5760, 5760),
    "8K": (10670, 10670),
    "Cover": (1024, 1024)
}

def save_image(image_tensor, filename, resolution):
    """
    Saves an image tensor to a file.

    Args:
        image_tensor (torch.Tensor): The image tensor to save.
        filename (str): The filename to save the image to.
        resolution (str): The resolution of the image.
    """
    width, height = resolutions.get(resolution, (1920, 1080))
    image = Image.fromarray((image_tensor.numpy().transpose(1, 2, 0) * 255).astype(np.uint8))
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image.save(filename, format='PNG')

def generate_texture_with_network(image, category_nodes, resolution):
    """
    Generates a texture using a neural network.

    Args:
        image (PIL.Image): The input image.
        category_nodes (list): A list of category nodes.
        resolution (str): The resolution of the output image.

    Returns:
        torch.Tensor: The generated image tensor.
    """
    width, height = resolutions.get(resolution, (1024, 1024))
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image_array = np.array(image) / 255.0
    image_tensor = torch.tensor(image_array, dtype=torch.float32).permute(2, 0, 1)

    pool = multiprocessing.Pool()
    chunk_size = image_tensor.shape[1] // multiprocessing.cpu_count()
    chunks = [(image_tensor, i, chunk_size, category_nodes) for i in range(0, image_tensor.shape[1], chunk_size)]
    results = pool.map(ImageNode("Temp").process_chunk, chunks)

    pool.close()
    pool.join()

    for start_row, modified_chunk in results:
        image_tensor[:, start_row:start_row + modified_chunk.shape[1], :] = modified_chunk

    return image_tensor

def process_texture(image, strength, scale, invert_specular, blur_radius, metallic_intensity, emission_intensity, opacity_threshold, invert_roughness, resolution):
    """
    Processes the input image to generate various texture maps.

    Args:
        image (PIL.Image): The input image.
        strength (float): The strength of the normal map.
        scale (float): The scale of the height map.
        invert_specular (bool): Whether to invert the specular map.
        blur_radius (int): The blur radius for the ambient occlusion map.
        metallic_intensity (float): The intensity of the metallic map.
        emission_intensity (float): The intensity of the emission map.
        opacity_threshold (int): The threshold for the opacity map.
        invert_roughness (bool): Whether to invert the roughness map.
        resolution (str): The resolution of the output images.

    Returns:
        dict: A dictionary containing the generated texture maps.
    """
    image_array = np.array(image)

    category_nodes = [Node(label) for label in ["Rot", "Grün", "Blau", "Gelb", "Cyan", "Magenta"]]
    for node in category_nodes:
        node.activation = random.uniform(0.2, 1.0)

    # Normal Map Processing
    normal_map_tensor = generate_texture_with_network(image, category_nodes, resolution)
    normal_map = (normal_map_tensor.numpy().transpose(1, 2, 0) * 255).astype(np.uint8)

    # Specular Map
    specular_map_tensor = generate_texture_with_network(image, category_nodes, resolution)
    specular_map = 255 - (specular_map_tensor.numpy().transpose(1, 2, 0) * 255).astype(np.uint8) if invert_specular else (specular_map_tensor.numpy().transpose(1, 2, 0) * 255).astype(np.uint8)

    # Ambient Occlusion Map
    ao_map = cv2.GaussianBlur(normal_map, (blur_radius, blur_radius), 0)

    # Metallic Map
    metallic_map = (normal_map * metallic_intensity).astype(np.uint8)

    # Emission Map
    emission_map = (normal_map * emission_intensity).astype(np.uint8)

    # Opacity Map
    _, opacity_map = cv2.threshold(normal_map, opacity_threshold, 255, cv2.THRESH_BINARY)

    # Roughness Map
    roughness_map = 255 - normal_map if invert_roughness else normal_map

    # Save Textures
    output_dir = "output_textures"
    os.makedirs(output_dir, exist_ok=True)

    cv2.imwrite(os.path.join(output_dir, f"normal_map_{resolution}.png"), normal_map)
    cv2.imwrite(os.path.join(output_dir, f"specular_map_{resolution}.png"), specular_map)
    cv2.imwrite(os.path.join(output_dir, f"ao_map_{resolution}.png"), ao_map)
    cv2.imwrite(os.path.join(output_dir, f"metallic_map_{resolution}.png"), metallic_map)
    cv2.imwrite(os.path.join(output_dir, f"emission_map_{resolution}.png"), emission_map)
    cv2.imwrite(os.path.join(output_dir, f"opacity_map_{resolution}.png"), opacity_map)
    cv2.imwrite(os.path.join(output_dir, f"roughness_map_{resolution}.png"), roughness_map)

    return {
        "Normal Map": normal_map,
        "Specular Map": specular_map,
        "AO Map": ao_map,
        "Metallic Map": metallic_map,
        "Emission Map": emission_map,
        "Opacity Map": opacity_map,
        "Roughness Map": roughness_map
    }

# ---------------------------
# Gradio Interface
# ---------------------------

def process_and_display(image, resolution, strength, scale, invert_specular, blur_radius, metallic_intensity, emission_intensity, opacity_threshold, invert_roughness):
    """
    Processes the input image and displays the generated texture maps.

    Args:
        image (PIL.Image): The input image.
        resolution (str): The resolution of the output images.
        strength (float): The strength of the normal map.
        scale (float): The scale of the height map.
        invert_specular (bool): Whether to invert the specular map.
        blur_radius (int): The blur radius for the ambient occlusion map.
        metallic_intensity (float): The intensity of the metallic map.
        emission_intensity (float): The intensity of the emission map.
        opacity_threshold (int): The threshold for the opacity map.
        invert_roughness (bool): Whether to invert the roughness map.

    Returns:
        tuple: A tuple containing the generated texture maps as PIL images.
    """
    textures = process_texture(image, strength, scale, invert_specular, blur_radius, metallic_intensity, emission_intensity, opacity_threshold, invert_roughness, resolution)
    output_dir = "output_textures"
    return (Image.fromarray(textures["Normal Map"]),
            Image.fromarray(textures["Specular Map"]),
            Image.fromarray(textures["AO Map"]),
            Image.fromarray(textures["Metallic Map"]),
            Image.fromarray(textures["Emission Map"]),
            Image.fromarray(textures["Opacity Map"]),
            Image.fromarray(textures["Roughness Map"]))

with gr.Blocks() as demo:
    gr.Markdown("### Textur-Generator mit neuronaler Netzwerk-Verarbeitung")

    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Input Texture", type="pil")
            resolution_dropdown = gr.Dropdown(label="Auflösung", choices=list(resolutions.keys()), value="Full HD")
            strength_slider = gr.Slider(label="Normal Map Strength", minimum=1, maximum=10, step=1, value=5)
            scale_slider = gr.Slider(label="Height Map Scale", minimum=0.1, maximum=3.0, step=0.1, value=1.0)
            invert_specular_checkbox = gr.Checkbox(label="Invert Specular Map", value=False)
            blur_radius_slider = gr.Slider(label="Ambient Occlusion Blur Radius", minimum=1, maximum=31, step=2, value=5)
            metallic_slider = gr.Slider(label="Metallic Intensity", minimum=0.1, maximum=3.0, step=0.1, value=1.0)
            emission_slider = gr.Slider(label="Emission Intensity", minimum=0.1, maximum=3.0, step=0.1, value=1.0)
            opacity_slider = gr.Slider(label="Opacity Threshold", minimum=0, maximum=255, step=1, value=128)
            invert_roughness_checkbox = gr.Checkbox(label="Invert Roughness Map", value=False)

        with gr.Column():
            normal_preview = gr.Image(label="Normal Map")
            specular_preview = gr.Image(label="Specular Map")
            ao_preview = gr.Image(label="Ambient Occlusion Map")
            metallic_preview = gr.Image(label="Metallic Map")
            emission_preview = gr.Image(label="Emission Map")
            opacity_preview = gr.Image(label="Opacity Map")
            roughness_preview = gr.Image(label="Roughness Map")

    process_button = gr.Button("Texturen generieren")

    process_button.click(
        process_and_display,
        inputs=[input_image, resolution_dropdown, strength_slider, scale_slider, invert_specular_checkbox, blur_radius_slider, metallic_slider, emission_slider, opacity_slider, invert_roughness_checkbox],
        outputs=[normal_preview, specular_preview, ao_preview, metallic_preview, emission_preview, opacity_preview, roughness_preview]
    )

if __name__ == "__main__":
    demo.launch(share=True)
