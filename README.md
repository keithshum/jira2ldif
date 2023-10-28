# jira2ldif

## Introduction

This project is to pull a list of users and groups from Jira User Server in csv, then transform it to ldif format and import to LDAP server.


## Motivation

Working on a new project which is to setup a brand new LDAP server. Inspired by Georchestra at [github]( https://github.com/georchestra/LDAP ), but every company requires different setup, and mine here is to be able to talk to Atlassian JIRA afterwards. So, I decided to write my own tool to pull data from JIRA's Postgresql DB and load it into Apache Directory Server.

## Steps to take

1. Pull data from Jira server into .csv
2. Run csv2ldif.py to create .ldif
3. Load into your LDAP

### 1. Pull data from Jira server into .csv

In the project directory, you will see `users-postgresql.sql` and 
`groups-postgresql.sql`, as you can see, they are for Postgres database.

The original queries are pulled from:
https://confluence.atlassian.com/display/JIRAKB/How+to+Get+a+List+of+Active+Users+Counting+Towards+the+JIRA+License

You will need to modify the way other DB works on output files.

So, after you run both queries, you should have 2 output files:
```
/tmp/users.csv
/tmp/groups.csv
```

`users.csv` should have the following format:

```
lower_user_name,display_name,first_name,last_name,email_address,credential
ckent,Clark Kent,Clark,Kent,clarkkent@acme.company,{PKCS5S2}abcdefghijklmnopqrstuvwxyz
pparker,Peter Parker,Peter,Parker,peterparker@acme.company,{PKCS5S2}abcdefghijklmnopqrstuvwxyz
bwayne,Bruce Wayne,Bruce,Wayne,brucewayne@acme.company,{PKCS5S2}abcdefghijklmnopqrstuvwxyz
```

`groups.csv` should have the following format:

```
lower_parent_name,lower_user_name
jira-administrators,ckent
jira-developer,pparker
jira-developer,bwayne
```


### 2. Run csv2ldif.py to create .ldif

To start, run

```
$ python csv2ldif.py users.csv groups.csv output.ldif
```

It will generates output.ldif and my schema is simple liked:

```
o=acme
|__ou=people
|   |__uid=ckent
|   |    |__cn=Clark Kent
|   |    |__givenname=Clark
|   |    |__sn=Kent
|   |    |__uid=ckent
|   |    |__mail=clarkkent@acme.company
|   |    |__userpassword={PKCS5S2}abcdefghijklmnopqrstuvwxyz
|   |__uid=pparker
|   |    |__...
|   |__uid=bwayne
|        |__...
|
|__ou=groups
    |__cn=jira-administrators
    |__cn=jira-developer
```


### 3. Load into your LDAP

During the loading time, I noticed the LDAP server returns quite some errors for missing row elements at users.csv. So I added some simple checking at csv2ldif.py before converting. 

The check is to return a warning before the users dn that will tell which lines in the csv has missing data, so you can go fix it.
