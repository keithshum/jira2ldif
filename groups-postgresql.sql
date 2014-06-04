copy (
SELECT DISTINCT m.lower_parent_name,
						u.lower_user_name
FROM   cwd_user u
       JOIN cwd_membership m
         ON u.id = m.child_id
            AND u.directory_id = m.directory_id
       JOIN cwd_directory d
         ON m.directory_id = d.id
WHERE  d.active = 1
       AND u.active = '1'
ORDER  BY m.lower_parent_name,
          lower_user_name )
to '/tmp/groups.csv'
with
	delimiter as ','
	null as ''
;	 
