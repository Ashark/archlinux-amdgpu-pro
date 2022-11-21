import os
from debian import deb822

p64 = os.path.expanduser("~/.aptly/public/dists/jammy/proprietary/binary-amd64/Packages")
p32 = os.path.expanduser("~/.aptly/public/dists/jammy/proprietary/binary-i386/Packages")

print("Merging 32 and 64 Packages files", p32, p64)
resulting_list = []

f = open(p32, "r")
# Dropping multi arch packages from 32 bit packages list
for deb_info in deb822.Packages.iter_paragraphs(f):
    if deb_info["Architecture"] == "all":
        print("info: dropping duplicated", deb_info["Package"])
        continue
    resulting_list.append(deb_info)
f.close()

f = open(p64, "r")
# Adding all packages from 64 bit packages list
for deb_info in deb822.Packages.iter_paragraphs(f):
    resulting_list.append(deb_info)
f.close()

# Sorting them
resulting_list.sort(key=lambda x: x["Package"], reverse=False)

with open("Packages-extracted", 'w') as f:
    for deb_info in resulting_list:
        print(deb_info, file=f)
print("Merged")
