import os
import json
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta

input_dir = "data/processed"  # Folder with cropped face images
output_file = "data/metadata/persons_metadata.json"

fake = Faker(['en_IN', 'hi_IN']) #Devanagari script

INDIAN_CITIES = [
    "New Delhi", "Mumbai", "Bangalore", "Hyderabad",
    "Ahmedabad", "Chennai", "Kolkata", "Pune",
    "Jaipur", "Lucknow"
]

CLOTHING = [
    "wearing blue jeans and white t-shirt",
    "wearing red salwar kameez",
    "wearing black kurta and white pajama",
    "wearing grey hoodie and track pants",
    "wearing formal shirt and trousers"
]

FEATURES = [
    "has a scar on left cheek",
    "has a mole on right forehead",
    "wears glasses",
    "has a tattoo on left arm",
    "has short curly hair",
    "has long straight hair"
]

def generate_metadata(fname, index):
    gender = random.choice(['Male', 'Female'])
    name = fake.name_male() if gender == "Male" else fake.name_female()

    last_seen_date = datetime.now() - timedelta(days=random.randint(1, 730)) ## Creating a random time duration subtracting from todays date November 2025

    metadata = {
        "id": str(uuid.uuid4()),
        "image_filename": fname,
        "name": name,
        "age": random.randint(18, 70),
        "gender": gender,
        "last_seen_date": last_seen_date.strftime("%Y-%m-%d"),
        "last_seen_location": random.choice(INDIAN_CITIES),
        "last_seen_time": f"{random.randint(0,23):02d}:{random.randint(0,59):02d}",
        "contact_info": f"+91-{random.randint(7000000000, 9999999999)}",
        "height": f"{random.randint(5,6)}'{random.randint(0,11)}\"",
        "additional_details": f"{random.choice(CLOTHING)}. {random.choice(FEATURES)}.",
        "case_id": f"MP2024{index:04d}",
        "case_status": random.choices(["active", "found"], weights=[0.75, 0.25])[0],
        "reported_by": random.choice(["Family Member", "Friend", "NGO Worker", "Police"]),
        "reporter_contact": f"+91-{random.randint(7000000000, 9999999999)}",
        "created_at": last_seen_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "is_synthetic": True
    }
    return metadata

def main():
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] ## opening the file and storing the images in files list
    metadata_list = []

    for idx, fname in enumerate(files, 1): #- The 1 means indexing starts at 1 instead of 0. It is assigning an index and the file name together
        metadata = generate_metadata(fname, idx)
        metadata_list.append(metadata)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, indent=4)

    print(f"✓ Generated metadata for {len(metadata_list)} images.")
    print(f"Metadata saved to {output_file}")

if __name__ == "__main__":
    main()
