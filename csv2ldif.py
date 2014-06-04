"""
csv2ldif.py

Tested on Python 2.6.6 and 3.4.0 without errors.
For more detail, see readme.md.

Last modified by Keith Shum, 2014-6-3

"""


import csv
from sys import argv


"""Default paramters"""
CSV_DELIMITER = ','
LDAP_ROOT_DN = 'o=acme'
PEOPLE_DN = 'ou=people,o=acme'
GROUPS_DN = 'ou=groups,o=acme'
EOL = "\r\n"


"""Take care the argv and the output file"""
script, i_user, i_group, output = argv
ldif = open(output, 'w')


"""Print some heading info to output"""
heading = """### Headings ###

dn: """+PEOPLE_DN+"""
objectClass: organizationalUnit
objectClass: top
description: Contain entries which describe persons
ou: people

dn: """+GROUPS_DN+"""
objectClass: organizationalUnit
objectClass: top
description: Contains entries which describe groups
ou: groups

### People ###
"""
ldif.write(heading)


"""Got to do some error checking"""
with open(i_user, 'r') as csvfile:
    users = csv.reader(csvfile, delimiter=',')

    miss = []
    i = 1
    for row in users:
        for j in row:
            if j == "":
                miss.append(i)
                break
        i += 1
    if len(miss) != 0:
        ldif.write("\n\n# !!!WARNING: Check the followings lines at "+i_user+", you may get error at loading to LDAP.")
        ldif.write("\n# "+ str(miss))

"""Print each user dn"""
with open(i_user, 'r') as csvfile:
    users = csv.reader(csvfile, delimiter=',')
    """Ready to do work"""
    for row in users:
        person = "\n\ndn: cn="+row[0].lstrip().rstrip()+","+PEOPLE_DN+"\nobjectClass: top\nobjectClass: person\nobjectClass: organizationPerson\nobjectclass: inetOrgPerson\ncn: "+row[0].lstrip().rstrip()+"\ndisplayname: "+row[1].lstrip().rstrip()+"\ngivenname: "+row[2].lstrip().rstrip()+"\nsn: "+row[3].lstrip().rstrip()+"\nuid: "+row[0].lstrip().rstrip()+"\nmail: "+row[4].lstrip().rstrip()+"\nuserpassword: "+row[5].lstrip().rstrip()
        ldif.write(person)

"""Close to trigger the write"""
ldif.close()


"""The followings are appends to the end"""
ldif = open(output, 'a')
ldif.write("### Groups ###")


"""Print each group dn"""
with open(i_group, 'r') as csvfile:
    groups = csv.reader(csvfile, delimiter=',')
    samegroup = 'nothing'
    for row in groups:
        if row[0].lstrip().rstrip() != samegroup:
            group = "\n\ndn: cn="+row[0].lstrip().rstrip()+","+GROUPS_DN+"\nobjectClass: groupOfUniqueNames\nobjectClass: top\ncn: "+row[0].lstrip().rstrip()+"\nuniquemember: cn="+row[1].lstrip().rstrip()+","+PEOPLE_DN
        else:
            group = "\nuniquemember: cn="+row[1].lstrip().rstrip()+","+PEOPLE_DN
        samegroup = row[0]
        ldif.write(group)

"""Close to trigger the write"""
ldif.write("\n\n### End of output.ldif ###")
ldif.close()


"""End of csv2ldif.py"""
