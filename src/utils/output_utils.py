import os
import json

def save_to_files(meta_data, images, links, output_dir):
    # Asegurarse de que el directorio de salida existe, si no, crearlo
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory {output_dir} created.")

    # Guardar Meta Data en archivo JSON
    with open(os.path.join(output_dir, "meta_data.json"), "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=4, ensure_ascii=False)
    
    # Guardar Imágenes en archivo de texto
    with open(os.path.join(output_dir, "images.txt"), "w", encoding="utf-8") as f:
        for img in images:
            f.write(img + "\n")

    # Guardar Links en archivo JSON
    with open(os.path.join(output_dir, "links.json"), "w", encoding="utf-8") as f:
        json.dump(links, f, indent=4, ensure_ascii=False)
    
    # Guardar Links en archivo de texto legible
    with open(os.path.join(output_dir, "links.txt"), "w", encoding="utf-8") as f:
        f.write("Telephone Links:\n")
        for tel in links["telephone"]:
            f.write(tel + "\n")
        
        f.write("\nEmail Links:\n")
        for email in links["email"]:
            f.write(email + "\n")

        f.write("\nInternal Links:\n")
        for internal in links["internal"]:
            f.write(internal + "\n")

        f.write("\nExternal Links:\n")
        for external in links["external"]:
            f.write(external + "\n")

    print(f"Data saved successfully to {output_dir}")
