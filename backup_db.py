import shutil

# Define the path to the original database
original_db = 'grievances.db'

# Define the path to the backup database
backup_db = 'grievances_backup.db'

# Create a backup by copying the file
shutil.copyfile(original_db, backup_db)

print("Backup created successfully.")
