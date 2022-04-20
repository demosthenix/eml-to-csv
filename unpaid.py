from os import walk, path, remove
import csv
import eml_parser
import sys
import re

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
    write.writerow(["Email"])
print("CSV file created...")
print("Extracting mail IDs from EML files... ")
c = 0
eml_count = len(files)
mail_set = set()
for f in files:
    
    try:
        with open(sys.argv[1]+'/'+f, 'rb') as mail:
            raw_email = mail.read()
            ep = eml_parser.EmlParser(include_raw_body=True)
            parsed_eml = ep.decode_email_bytes(raw_email)
            mail_id = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', parsed_eml['body'][0]['content']).group(0)
            mail_set.add(mail_id)
    except Exception as e:
        print(e, "=> While extracting", sys.argv[1]+'/'+f)
    
    c += 1
    print(c, "of", eml_count,"Mail IDs Extracted")
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K") 
print(c, "of", eml_count,"Mail IDs Extracted")

print("Adding Mail IDs into csv file ...")
rows = list(map(lambda el:[el], mail_set))
with open(sys.argv[1]+'/'+'mails.csv', 'w+') as m:
    write = csv.writer(m)
    write.writerows(rows)