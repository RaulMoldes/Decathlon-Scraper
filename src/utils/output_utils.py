import os
import json

def save_to_files(meta_data, images, links,text, output_dir):
    # Asegurarse de que el directorio de salida existe, si no, crearlo
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory {output_dir} created.")

    # Guardar Meta Data en archivo JSON
    with open(os.path.join(output_dir, "meta_data.json"), "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=4, ensure_ascii=False)
    
    # Guardar Meta Data en archivo JSON
    with open(os.path.join(output_dir, "images.json"), "w", encoding="utf-8") as f:
        json.dump(images, f, indent=4, ensure_ascii=False)

    # Guardar Links en archivo JSON
    with open(os.path.join(output_dir, "links.json"), "w", encoding="utf-8") as f:
        json.dump(links, f, indent=4, ensure_ascii=False)

    # Guardar Links en archivo JSON
    with open(os.path.join(output_dir, "text.json"), "w", encoding="utf-8") as f:
        json.dump(text, f, indent=4, ensure_ascii=False)

    print(f"Data saved successfully to {output_dir}")

