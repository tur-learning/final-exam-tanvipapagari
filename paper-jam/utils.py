import requests

def get_wikipedia_preview_image(page_title, thumbnail_size=500):
    """
    Returns the URL for the preview (thumbnail) image of a Wikipedia page.
    :param page_title: The title of the Wikipedia page (e.g., 'Colosseum')
    :param thumbnail_size: Desired width of the returned image thumbnail in pixels
    :return: URL of the image (string) or None if not found
    """
    # Endpoint for Wikipedia's MediaWiki API:
    endpoint = "https://en.wikipedia.org/w/api.php"

    # Set up query parameters to get pageimages (thumbnail) for the given page
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": page_title,
        "pithumbsize": thumbnail_size
    }

    # Query the API
    response = requests.get(endpoint, params=params)
    data = response.json()

    # The structure of the response is data['query']['pages'][PAGEID]...
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return None

    # The page ID is an unknown numeric key, so get it by iteration
    for page_id, page_info in pages.items():
        # If there's a thumbnail key, extract the 'source' field
        thumbnail = page_info.get("thumbnail", {})
        source_url = thumbnail.get("source")
        if source_url:
            return source_url

    return None

# Example usage:
if __name__ == "__main__":
    page_name = "Colosseum"
    preview_image_url = get_wikipedia_preview_image(page_name, thumbnail_size=500)
    if preview_image_url:
        print(f"Preview image URL for '{page_name}':\n{preview_image_url}")
    else:
        print(f"No preview image found for '{page_name}'.")
