README.md: storage.i80.mysql-8.0.15.html
	./README.sh $^ > $@

storage.csv: $(wildcard ~/storage/*/*/*/*)
	./src/storage.py -o $@ $^

storage.i80.mysql-8.0.15.csv: storage.csv
	./src/select.py -i storage.csv -o $@ 'machine==i80' 'engine==mysql 8.0.15'

storage.i80.mysql-8.0.15.html: storage.i80.mysql-8.0.15.csv
	./src/plotly/throughput.py -o $@ storage.i80.mysql-8.0.15.csv

clean:
	rm -f *.csv

push:
	git commit -am update
	git push origin master
