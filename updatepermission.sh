#!/bin/bash
echo "delete from auth_permission;delete from django_content_type;" > 1.sql
mysqldump -u weixin -pweixin weixin auth_permission | grep "INSERT INTO" >> 1.sql
mysqldump -u weixin -pweixin weixin django_content_type | grep "INSERT INTO" >> 1.sql
