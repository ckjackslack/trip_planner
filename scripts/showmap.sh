PREFIX="file://"
MAP_PATH=`realpath trip_map.html`
FULL_PATH="${PREFIX}${MAP_PATH}"
echo "Opening: ${FULL_PATH}"
python -m webbrowser -n -t $FULL_PATH