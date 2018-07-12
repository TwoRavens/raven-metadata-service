import os
import tempfile

def dashes(): print('-' * 40)
def msgt(amsg): dashes(); print(amsg); dashes()

# ---------------------------
# Create the temp file object
# ---------------------------
named_temp_file = tempfile.NamedTemporaryFile(delete=False)

# ---------------------------
# Retrieve its path
# ---------------------------
temp_file_path = named_temp_file.name
msgt('(1) create file')
print('temp_file_path', temp_file_path)
print('filesize: ', os.path.getsize(temp_file_path))

# ---------------------------
# Write to it
# ---------------------------
msgt('(2) add data to file')

some_json_str = b'{"animal": "dolphin", "color": "grey"}'
named_temp_file.write(some_json_str)
named_temp_file.close()
print('file written')
print('does file exist?', os.path.isfile(temp_file_path))
print('filesize: ', os.path.getsize(temp_file_path))

# ---------------------------
# Do something (like send it to Dataverse)
# ---------------------------
msgt('(3) show file contents')
print(open(temp_file_path, 'r').read())

# ---------------------------
# Delete the temp file
# ---------------------------
msgt('(4) delete the file')
os.unlink(temp_file_path)
print('does file exist?', os.path.isfile(temp_file_path))
dashes()


# ---------------------------
# --- Other notes ----
# ---------------------------
"""
# If reading a large file, which may be doing from Mongo,
# then would use something like:
for block in request.iter_content(1024 * 8):
    # If blocks, then stop
    if not block:
        break
    # Write image block to temporary file
    named_temp_file.write(block)
"""
