"""Image EXIF & Metadata Forensics with GPS Geolocation & Privacy Stripper."""
import os
try:
    from PIL import Image, ExifTags
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

def _convert_to_degrees(value):
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return None

def analyze_exif(image_path: str) -> dict:
    if not PILLOW_AVAILABLE:
        return {"error": "Pillow is required for image forensics. Install: pip install Pillow"}
    if not os.path.exists(image_path):
        return {"error": f"Image file not found: {image_path}"}
    results = {}
    try:
        with Image.open(image_path) as img:
            results["File Name"] = os.path.basename(image_path)
            results["Image Format"] = str(img.format)
            results["Dimensions"] = f"{img.width} x {img.height} px"
            results["Color Mode"] = str(img.mode)
            exif_data = img._getexif()
            if not exif_data:
                results["EXIF Status"] = "No EXIF metadata found (Likely stripped or screenshot)"
                return results
            results["EXIF Status"] = "Metadata Detected"
            gps_info = {}
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                if tag_name == "Make":
                    results["Camera Manufacturer"] = str(value).strip()
                elif tag_name == "Model":
                    results["Camera / Phone Model"] = str(value).strip()
                elif tag_name == "Software":
                    results["Editing Software / OS"] = str(value).strip()
                elif tag_name == "DateTimeOriginal":
                    results["Date & Time Taken"] = str(value).strip()
                elif tag_name == "DateTime":
                    results["Date & Time Modified"] = str(value).strip()
                elif tag_name == "GPSInfo":
                    gps_info = value
            if gps_info:
                gps_tags = {}
                for key in gps_info.keys():
                    sub_tag = ExifTags.GPSTAGS.get(key, key)
                    gps_tags[sub_tag] = gps_info[key]
                lat_ref = gps_tags.get("GPSLatitudeRef")
                lat = gps_tags.get("GPSLatitude")
                lon_ref = gps_tags.get("GPSLongitudeRef")
                lon = gps_tags.get("GPSLongitude")
                if lat and lon and lat_ref and lon_ref:
                    lat_deg = _convert_to_degrees(lat)
                    lon_deg = _convert_to_degrees(lon)
                    if lat_deg is not None and lon_deg is not None:
                        if lat_ref == "S": lat_deg = -lat_deg
                        if lon_ref == "W": lon_deg = -lon_deg
                        results["GPS Latitude"] = f"{lat_deg:.6f}"
                        results["GPS Longitude"] = f"{lon_deg:.6f}"
                        results["Google Maps Coordinates"] = f"https://www.google.com/maps?q={lat_deg:.6f},{lon_deg:.6f}"
    except Exception as e:
        return {"error": f"Failed to analyze image: {str(e)}"}
    return results

def strip_exif(image_path: str, output_path: str = None) -> dict:
    if not PILLOW_AVAILABLE:
        return {"error": "Pillow is required. Install: pip install Pillow"}
    if not os.path.exists(image_path):
        return {"error": f"Image file not found: {image_path}"}
    try:
        if not output_path:
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_clean{ext}"
        with Image.open(image_path) as img:
            data = list(img.getdata())
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(data)
            clean_img.save(output_path)
        return {
            "Status": "EXIF stripped successfully",
            "Cleaned File Saved At": output_path,
            "Privacy Note": "All camera model, date, software, and GPS tags removed."
        }
    except Exception as e:
        return {"error": f"Failed to strip metadata: {str(e)}"}
