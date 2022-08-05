divider================
divider=$divider$divider

width=22

export FLASK_APP=main.py
echo $FLASK_APP

export FLASK_ENV=development
echo $FLASK_ENV

printf "%$width.${width}s\n\n" "$divider"
printf "%s\n" "Flask's sets are ready" "(1)To run the server" "(2)To run tests" "Pres any key to DO NOTHING"
read -n1 -s number
case $number in 
    1) flask run --reload ;;
    2) flask test ;;
    *) echo DOING NOTHING ;;
esac