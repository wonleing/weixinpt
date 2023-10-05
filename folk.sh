#!/bin/bash
[ $# != 4 ] && echo "Usage: $0 <tname> <Tname> <pname> <Pname>" && exit 1
cp -r $1 $3
rm -rf $3/.svn
sed -i "s/$1/$3/g;s/$2/$4/g" $3/*.py
sed -i "s/# END_OF_APP/'$3',\n    # END_OF_APP/" weixin/settings.py
sed -i "s;# END_OF_URL;url(r'^$3/\$', '$3.views.handleRequest', name='$3_index'),\n    url(r'^$3/(?P<pageid>\\\d+)/\$', '$3.views.subpage', name='$3_subpage'),\n    # END_OF_URL;" weixin/urls.py
exit
./manage.py syncdb
svn add $3
svn ci -m "add new platform: $3"
echo "Please import create db in mysql and run updatepermission.sh"
