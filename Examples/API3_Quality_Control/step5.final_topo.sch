step 5: -c all 1.0 0 -C all 1.0 24 -r -S 300 -w
step 6: -sys 'ws qchk volute.grd 11 10000 0.8 120'
step 7: -sys 'python Quality.py step5.final_topo.sch'
write -f volute.grd
