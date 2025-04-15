import requests
import os
import json
import time
import zipfile

class OpenStreetMapClient:
    BASE_URL = "http://printmaps-osm.de:8282/api/beta2/maps"

    def __init__(self):
        pass

    def create_map_metadata(self, attributes: dict):
        """
        Creates metadata for the map request.

        Parameters:
        attributes (dict): Map settings including scale, format, style, etc.

        Returns:
        dict: JSON response containing the map ID.
        """
        url = f"{self.BASE_URL}/metadata"

        post_data = {
            "Data": {
                "Type": "maps",
                "ID": "",
                "Attributes": attributes
            }
        }

        response = requests.post(url, headers=self._headers(), data=json.dumps(post_data))
        self._handle_response(response, "Error: Bad Request while creating map metadata.")
        
        print(f"Metadata successfully created.")
        return response.json()

    def order_map(self, map_id: str):
        """
        Orders the map for rendering.

        Parameters:
        map_id (str): ID of the created map.

        Returns:
        dict: JSON response confirming order acceptance.
        """
        url = f"{self.BASE_URL}/mapfile"

        post_data = {"Data": {"Type": "maps", "ID": map_id}}

        response = requests.post(url, headers=self._headers(), data=json.dumps(post_data))
        self._handle_response(response, "Error: Bad Request while creating an order.")

        print(f"Order successfully accepted.")
        return response.json()

    def fetch_map_state(self, map_id: str):
        """
        Fetches the status of the map build.

        Parameters:
        map_id (str): ID of the map being processed.

        Returns:
        dict: JSON response with the build status.
        """
        url = f"{self.BASE_URL}/mapstate/{map_id}"
        response = requests.get(url, headers=self._headers(), allow_redirects=False)
        self._handle_response(response, "Error: Bad Request while fetching the status.")

        print(f"State successfully fetched.")
        return response.json()

    def download_map(self, map_id: str, output_dir: str = "."):
        """
        Downloads and extracts the generated map.

        Parameters:
        map_id (str): ID of the completed map.
        output_dir (str): Directory to save the downloaded map.

        Returns:
        None
        """
        url = f"{self.BASE_URL}/mapfile/{map_id}"
        response = requests.get(url, headers=self._headers())
        self._handle_response(response, "Error: Bad Request while downloading the map.")

        print(f"Map successfully downloaded.")

        # Save response headers
        headers_filepath = os.path.join(output_dir, "response-header.txt")
        with open(headers_filepath, "w") as f:
            for key, value in response.headers.items():
                f.write(f"{key}: {value}\n")

        # Save map file
        output_filepath = os.path.join(output_dir, "printmap.zip")
        with open(output_filepath, "wb") as f:
            f.write(response.content)

        print(f"Map downloaded. Headers saved to {headers_filepath}, map saved to {output_filepath}")

        # Extracting and cleaning up the zip file
        with zipfile.ZipFile(output_filepath, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

        os.remove(output_filepath)
        print(f"Extracted to {output_dir} and removed zip file.")

    def _headers(self):
        """
        Returns the common headers for API requests.

        Returns:
        dict: Headers dictionary.
        """
        return {
            "Content-Type": "application/vnd.api+json; charset=utf-8",
            "Accept": "application/vnd.api+json; charset=utf-8",
        }

    def _handle_response(self, response, error_message):
        """
        Handles API responses, raising errors for unsuccessful status codes.

        Parameters:
        response (requests.Response): The HTTP response object.
        error_message (str): Error message to print on failure.

        Returns:
        None
        """
        if response.status_code == 400:
            print(error_message)
            response.raise_for_status()
        response.raise_for_status()
