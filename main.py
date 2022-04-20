from ast import Try
from os import walk, path, remove
import csv
import json
import eml_parser
import sys

files = []
print("Opening Directory")
print("Loading EML files...")
for (dirpath, dirname, filename) in walk(sys.argv[1]):
    
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K") 
    files.extend(filename)
    break

print("EML files loaded.")

if path.exists(sys.argv[1]+'/'+"mails.csv"):
    remove(sys.argv[1]+'/'+"mails.csv")

print("Creating CSV file...")
with open(sys.argv[1]+'/'+'mails.csv', 'a+') as m:
    write = csv.writer(m)
    write.writerow(["Date", "From", "To", "Subject"])
print("CSV file created...")
print("Extracting mail IDs from EML files... ")
c = 0
eml_count = len(files)
for f in files:
    
    try:
        with open(sys.argv[1]+'/'+f, 'rb') as mail:
            raw_email = mail.read()

            ep = eml_parser.EmlParser(include_raw_body=True)
            parsed_eml = ep.decode_email_bytes(raw_email)
            mail_header = parsed_eml["header"] 
            row = [mail_header["date"], mail_header.get("from", " "), mail_header["to"][0], mail_header["subject"]]
            with open(sys.argv[1]+'/'+'mails.csv', 'a+') as m:
                write = csv.writer(m)
                write.writerow(row)
    except Exception as e:
        print(e)
    
    c += 1
    print(c, "of", eml_count,"Mail IDs Extracted")
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K") 
print(c, "of", eml_count,"Mail IDs Extracted")

    
