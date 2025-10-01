import json

# 1. Load the JSON files
with open("verse_arabic.json", "r", encoding="utf-8") as f:
    #this opens the file versse_arabic.json and reads it thats teh "r" part using utf-8
    #  encoding as f means file
    arabic = json.load(f)
    #this loads the json data from the file into a python dictionary called arabic

with open("verse_english.json", "r", encoding="utf-8") as f:
    #this opens the file verse_english.json and reads it thats teh "r" part using utf-8

    english = json.load(f)
    #this loads the json data from the file into a python dictionary called english
    

with open("tafsir.json", "r", encoding="utf-8") as f:
    # this opens the file tafsir.json and reads it thats teh "r" part using utf-8
    tafsir = json.load(f)
    #this loads the json data from the file into a python dictionary called tafsir

# 2. Merge them
merged = {}
# starts an empty dictionary called merged
for key in arabic:
    merged[key] = {
        "arabic": arabic[key].get("text") or arabic[key].get("t"),
        "english": english.get(key, {}).get("t", ""),
        "tafsir": tafsir.get(key, "")
    }
    #this loops through each key in the arabic dictionary
    #for each key it creates a new entry in the merged dictionary
    #the new entry contains three sub-entries: arabic, english, and tafsir
    #it uses the get method to safely access the values which is the text inside the key in the original dictionaries

# 3. Save to a new file
with open("merged_quran.json", "w", encoding="utf-8") as f:
    #this opens a new file called merged_quran.json in write mode using utf-8 encoding
    json.dump(merged, f, ensure_ascii=False, indent=2)
    #this dumps the merged dictionary into the new file as a formatted json
print("Merged JSON created successfully as 'merged_quran.json'.")
