import csv
import requests

def reverse_geocode(lat, lng):
    url = f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lng}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'address' in data:
            address = data['address']
            formatted_address = ', '.join(filter(None, [address.get('road'), address.get('city'), address.get('state'), address.get('country')]))
            return formatted_address
    return None

def find_addresses(csv_file):
    counter=0
    addresses = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row
        header.append('Address')  # Add 'Address' column to the header
        addresses.append(header)  # Store the header row in the addresses list
        for row in reader:
            lat, lng = float(row[-1]), float(row[-2])  # Assuming the last two columns are centroid coordinates
            address = reverse_geocode(lat, lng)
            row.append(address)  # Add the address to the current row
            addresses.append(row)  # Store the row with the address
            counter+=1
            print(f"{counter}/1048575")
    return addresses

def save_addresses_to_csv(addresses, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(addresses)

csv_file = 'TN_Building_Footprints.csv'
addresses = find_addresses(csv_file)
output_file = 'TN_Building_Footprints.csv'
save_addresses_to_csv(addresses, output_file)
print(f"Addresses saved to {output_file}")
