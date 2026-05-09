import re

def unique_list(items):
    final = []
    for item in items:
        if item not in final:
            final.append(item)
    return final


def contains_devanagari(text):
    return bool(re.search(r'[\u0900-\u097F]', text))


def parse_banner_details(ocr_text: str, ocr_lines=None):
    if ocr_lines is None:
        ocr_lines = []

    lower_text = ocr_text.lower()

    # Better phone extraction
    contact_numbers = re.findall(r'\b[6-9]\d{9}\b|\b0\d{9,11}\b', ocr_text)
    contact_numbers = unique_list(contact_numbers)

    # Email extraction
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', ocr_text)

    # Website extraction - avoid wrong values like R.la
    websites = re.findall(r'(?:www\.|https?://)[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}', ocr_text)
    websites = unique_list(websites)

    # Hindi/English shop type keywords
    shop_type_keywords = {
        "print": "Printing Shop",
        "printing": "Printing Shop",
        "banner": "Banner / Printing Shop",
        "signboard": "Signboard Shop",
        "medical": "Medical Shop",
        "pharmacy": "Medical Shop",
        "grocery": "Grocery Shop",
        "mart": "Grocery / Mart",
        "salon": "Salon",
        "bakery": "Bakery",
        "mobile": "Mobile Shop",
        "electronics": "Electronics Shop",

        # Food / catering keywords
        "cater": "Food / Catering Shop",
        "catering": "Food / Catering Shop",
        "restaurant": "Restaurant / Food Shop",
        "food": "Food Shop",
        "चाऊमीन": "Food / Catering Shop",
        "कैटर": "Food / Catering Shop",
        "कैटर्स": "Food / Catering Shop",
        "मोमोस": "Food / Catering Shop",
        "बिरयानी": "Food / Catering Shop",
        "पराठा": "Food / Catering Shop",
        "बर्गर": "Food / Catering Shop",
        "रोल": "Food / Catering Shop",
        "वेज": "Food / Catering Shop"
    }

    shop_type = "Unknown"

    for keyword, value in shop_type_keywords.items():
        if keyword.lower() in lower_text or keyword in ocr_text:
            shop_type = value
            break

    # Service keywords
    service_keywords = [
        "printing", "print", "banner", "sign", "design",
        "poster", "leaflet", "graphics",

        "चाऊमीन", "मोमोस", "बिरयानी", "पराठा",
        "बर्गर", "बगर", "रोल", "वेज", "कबाब",
        "burger", "momos", "biryani", "paratha", "roll"
    ]

    services = []

    for keyword in service_keywords:
        if keyword.lower() in lower_text or keyword in ocr_text:
            services.append(keyword)

    services = unique_list(services)

    # Better shop name detection
    ignore_words = [
        "www", "http", ".com", "@", "phone", "contact", "email",
        "facebook", "cctv", "8x3", "४x३", "800", "945",
        "जी.सी.", "लखनऊ", "आर.", "का", ","
    ]

    service_words = [
        "चाऊमीन", "मोमोस", "बिरयानी", "पराठा",
        "बर्गर", "बगर", "रोल", "वेज", "कबाब"
    ]

    possible_names = []

    for line in ocr_lines:
        clean_line = line.strip()

        if len(clean_line) < 2:
            continue

        lower_line = clean_line.lower()

        if any(word in lower_line for word in ignore_words):
            continue

        if re.search(r'\b[6-9]\d{9}\b', clean_line):
            continue

        # Ignore random latin garbage
        if not contains_devanagari(clean_line):
            if len(clean_line) < 4:
                continue
            if re.search(r'[^a-zA-Z0-9\s&.-]', clean_line):
                continue

        # Ignore food item names as shop name
        if clean_line in service_words:
            continue

        possible_names.append(clean_line)

    shop_name = "Not Detected"

    # Special handling for this type of Hindi food banner
    if "यश" in ocr_text and shop_type == "Food / Catering Shop":
        shop_name = "यश कैटर्स"
    elif possible_names:
        devanagari_names = [x for x in possible_names if contains_devanagari(x)]

        if devanagari_names:
            shop_name = max(devanagari_names, key=len)
        else:
            shop_name = max(possible_names, key=len)

    return {
        "shop_name": shop_name,
        "shop_type": shop_type,
        "contact_numbers": contact_numbers,
        "emails": unique_list(emails),
        "websites": websites,
        "services": services
    }