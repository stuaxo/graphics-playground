for file in *.png
do
 convert "$file" "${file/.png}.gif"
done
