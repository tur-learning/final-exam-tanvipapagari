# 🗺️ Hands-On: Generating Custom Maps with OpenStreetMap API  

## **📌 Overview**  
In this hands-on session, you will work with **OpenStreetMap (OSM) API** to **generate high-quality map images** using Python.  
We have refactored the code into two modules:  

- **`osm_client.py`** → A client to interact with the OSM API (handles map creation, ordering, downloading).  
- **`main.py`** → Executes the workflow to create and retrieve a map image.  

### **🎯 Your Goal**  
🔹 Understand how to request and download a **custom map** from OSM.  
🔹 Explore the **OSM PrintMaps API** to customize your map.  
🔹 Try adding **your own styles, markers, or annotations** to enhance the map.  

---

## **📝 How It Works**  

### **1️⃣ Setup & Run the Script**  
To generate a map, simply run:  
```bash
python main.py
```  
This will:  
✅ Create map metadata (resolution, scale, styles)  
✅ Send a request to generate the map  
✅ Wait for processing to complete  
✅ Download and extract the map image  

### **2️⃣ Understanding the Code Structure**  

📂 **`osm_client.py`** → The API client that manages OSM interactions.  
- `create_map_metadata()` → Defines the map settings.  
- `order_map()` → Requests OSM to render the map.  
- `fetch_map_state()` → Checks if the map is ready.  
- `download_map()` → Retrieves and extracts the final image.  

📂 **`main.py`** → Controls the map generation workflow.  
- Defines **map attributes** (size, scale, style).  
- Calls `osm_client.py` functions to **create, order, and download** the map.  
- Uses a **waiting loop** to check when the map is ready.  

---

## **🎨 Customizing Your Map**  
Now, let’s make it **more appealing!**  
Explore the **[OSM PrintMaps API Docs](http://printmaps-osm.de/en/index.html)** to find customization options.  

### **🔧 Things You Can Modify:**  
✅ **Change the map style** → e.g., `"Style": "osm-bright"` instead of `"osm-carto"`.  
✅ **Adjust the resolution & scale** → Higher values for a more detailed map.  
✅ **Add custom annotations** (e.g., roads, points of interest, buildings).  
✅ **Modify the bounding box** → Center the map on a different location.  
✅ **Use different projections** → Play with `"Projection": "3857"` vs `"4326"`.  
✅ **Experiment with `UserObjects`** → Add text, lines, or markers.  

📌 **Example: Adding a Custom Marker (Pin)**
```python
"UserObjects": [
    {
        "Style": "<PointSymbolizer file='pin_red.svg' width='10' height='10' />",
        "WellKnownText": "POINT(300.0 300.0)"
    }
]
```
This places a **red pin** at the center of the map. Try using different colors and icons! 🎯  

---

## **🚀 Next Steps**  
🔹 **Run the script** and see how the default map looks.  
🔹 **Modify `attributes` in `main.py`** to test different styles.  
🔹 **Check the API documentation** to add **custom markers, labels, and annotations**.  
🔹 **Experiment & compare** your generated maps with different settings!  

💡 **Pro Tip:** Once you create a great-looking map, **share a screenshot** with the group! 📸🌍  

---  

## **💡 Why This Matters?**  
✔ Learn how to **interact with external APIs using Python**.  
✔ Understand **geospatial visualization** and map customization.  
✔ Gain experience working with **OSM-based mapping services**.  

Now, go ahead and **print your custom map!** 🗺️✨  

