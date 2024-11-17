def process_preserve_ids():
    # Open the cloudshop_ids.txt for reading
    with open("cloudshop_ids.txt", "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    # Open preserve.txt for writing the first ids
    with open("preserve.txt", "w", encoding="utf-8") as outfile:
        for line in lines:
            # Split the line by commas to get the cloudshop_ids
            cloudshop_ids = line.strip().split(", ")

            # Write only the first cloudshop_id to preserve.txt
            if cloudshop_ids:  # Ensure there is at least one id in the line
                outfile.write(cloudshop_ids[0] + "\n")

    print("Generated 'preserve.txt' with the first cloudshop_ids.")

if __name__ == "__main__":
    process_preserve_ids()
