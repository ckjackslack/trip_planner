TABLE_NAME=`echo ".tables" | sqlite3 trip_planner.db`
sqlite3 trip_planner.db << EOF
select * from ${TABLE_NAME};
EOF
pkill sqlite3
ps -aux | grep "sqlite3"