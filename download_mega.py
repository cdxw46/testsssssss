#!/usr/bin/env python3
from mega import Mega

mega = Mega()

# Download the file
file_url = "https://mega.nz/file/h2MBnJQC#EIWGEq80Zlu8z9uXi8H3y74t13jkidKZTKGAWEi94L4"
m = mega.login()
m.download_url(file_url, dest_filename='rauth_challenge.zip')
print("File downloaded successfully!")