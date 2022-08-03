divider================
divider=$divider$divider

width=22

export FLASK_APP=main.py
echo $FLASK_APP

export FLASK_ENV=development
echo $FLASK_ENV

printf "%$width.${width}s\n\n" "$divider"
printf "%s\n" "Flask's sets are ready" "use   flask run --reload  to run the server"