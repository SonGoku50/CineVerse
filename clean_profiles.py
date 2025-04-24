import json
import django
django.setup()

from myproject.models import UserProfile

# IDs aus der DB
existing_ids = set(UserProfile.objects.values_list("user_id", flat=True))

with open("all_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned = []

for entry in data:
    if entry["model"] == "myproject.userprofile":
        if entry["fields"]["user"] in existing_ids:
            print(f"Überspringe UserProfile für User-ID {entry['fields']['user']}")
            continue
    cleaned.append(entry)

with open("all_data_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2)

print("✅ Fertig – Datei 'all_data_cleaned.json' ist bereit")

