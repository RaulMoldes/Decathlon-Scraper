from bs4 import BeautifulSoup
import json
import os


def extract_meta_data(soup: BeautifulSoup):
    meta_data = {}
    for meta_tag in soup.find_all("meta"):
        property_value = meta_tag.get("property", None)
        content_value = meta_tag.get("content", None)
        if property_value and content_value:
            meta_data[property_value] = content_value
    print(f"Total meta tags found: {len(meta_data)}")
    return meta_data


def extract_images(soup: BeautifulSoup, base_url: str):
    images = []
    for img_tag in soup.find_all("img"):
        img_src = img_tag.get("src", None)
        if img_src:
            if not img_src.startswith("http"):
                images.append(f"{base_url}{img_src}")
            else:
                images.append(img_src)
        # Handle srcset if present
        elif img_tag.has_attr("srcset"):
            print("Detected srcset attribute in image.")

    print(f"Total images found: {len(images)}")
    return images


def extract_all_links(soup: BeautifulSoup, website_domain: str, base_url: str):
    categorized_links = {"telephone": [], "email": [], "internal": [], "external": []}
    for anchor_tag in soup.find_all("a"):
        href_value = anchor_tag.get("href", None)
        if href_value:
            cleaned_href = href_value.split("#")[0]  # Remove anchor portion
            if cleaned_href.startswith("mailto"):
                categorized_links["email"].append(cleaned_href)
            elif cleaned_href.startswith("tel"):
                categorized_links["telephone"].append(cleaned_href)
            # Handle relative paths
            elif cleaned_href.startswith("/"):
                categorized_links["internal"].append(f"{base_url}{cleaned_href}")
            # Same-site links (internal)
            elif cleaned_href.startswith(website_domain) or cleaned_href.startswith(base_url):
                categorized_links["internal"].append(cleaned_href)
            # Handle relative internal links
            elif not cleaned_href.startswith("http"):
                categorized_links["internal"].append(f"{base_url}/{cleaned_href}")
            # External links
            elif cleaned_href.startswith("http"):
                categorized_links["external"].append(cleaned_href)

    # Remove duplicates by converting lists to sets and back to lists
    return {
        "telephone": list(set(categorized_links["telephone"])),
        "email": list(set(categorized_links["email"])),
        "internal": list(set(categorized_links["internal"])),
        "external": list(set(categorized_links["external"])),
    }

