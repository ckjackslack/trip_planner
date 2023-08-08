rm -rf trip_planner/__pycache__

FILES=('trip_planner.db' 'trip_map.html')
for file in $FILES
do
    if [ -f ${file} ]; then
        echo "Removing ${file}."
        rm $file
    fi
done

find -type f -name "*.pyc" ! -path "./.venv/*" | xargs -I{} rm {}