set xdata time
set timefmt "%Y-%m-%d-%H:%M:%S"
set output "lang1.png"
set terminal png
plot "./stats.txt" using 1:2:3 with filledcurve
set output "lang2.png"
set terminal png
plot "./stats.txt" using 1:4:5 with filledcurve
set output "lang3.png"
set terminal png
plot "./stats.txt" using 1:6:7 with filledcurve
set output "lang4.png"
set terminal png
plot "./stats.txt" using 1:3 with lines, "./stats.txt" using 1:5 with lines, "./stats.txt" using 1:7 with lines
set output "lang5.png"
set terminal png
plot "./stats.txt" using 1:2 with lines, "./stats.txt" using 1:4 with lines, "./stats.txt" using 1:6 with lines
