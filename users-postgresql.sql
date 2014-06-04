copy (
SELECT DISTINCT u.lower_user_name,
                u.display_name,
                u.first_name,
                u.last_name,
                u.email_address,
                u.credential
FROM   cwd_user u
       JOIN cwd_membership m
         ON u.id = m.child_id
            AND u.directory_id = m.directory_id
       JOIN schemepermissions sp
         ON Lower(m.parent_name) = Lower(sp.perm_parameter)
       JOIN cwd_directory d
         ON m.directory_id = d.id
WHERE  sp.permission IN ( '0', '1', '44' )
       AND d.active = '1'
       AND u.active = '1'
ORDER  BY lower_user_name )
to '/tmp/users.csv'
with
	delimiter as ','
	null as ''
;
