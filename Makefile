testprog:
	g++ -o testprog demo/atiktest.cpp -I./demo -I./include -latikccd -lusb-1.0 -lcfitsio

clib:
	g++ src/atikccd.cpp -fPIC -shared -o /usr/local/lib/libatik.so -latikccd -lusb-1.0

flight:
	$(pwd)
	g++ src/flightcam_v2.cpp -o cam -DPIC_TIME_GAP=15 -DRPI -DPIX_BIN=1 -std=c++11 -I./include/ -lusb-1.0 -latikccd -lm -fopenmp -lboost_system -lboost_filesystem -lcfitsio -lpigpio -lrt -lpthread -DDATAVIS -lmcp9808 -lads1115 -DENABLE_POWEROFF -DENABLE_REBOOT
	cp cam data/
	
clean:
	sudo rm -rf data/*
	rm cam
