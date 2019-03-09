push: README.md
	git commit -am update
	git push origin master

README.md: storage.i80.mysql-8.0.15.html
	./README.sh $^ > $@

storage.csv: $(wildcard ~/storage/*/*/*/*)
	./src/storage.py -o $@ $^

storage.i80.mongo-4.1.8.csv: storage.csv
	./src/select.py -i storage.csv -o $@ 'machine==i80' 'engine==mongo 4.1.8'
storage.i80.mongo-4.1.8.html: storage.i80.mongo-4.1.8.csv
	./src/plotly/throughput.py -o $@ storage.i80.mongo-4.1.8.csv

storage.i80.mysql-8.0.15.csv: storage.csv
	./src/select.py -i storage.csv -o $@ 'machine==i80' 'engine==mysql 8.0.15'
storage.i80.mysql-8.0.15.html: storage.i80.mysql-8.0.15.csv
	./src/plotly/throughput.py -o $@ storage.i80.mysql-8.0.15.csv

clean:
	rm -f *.csv
