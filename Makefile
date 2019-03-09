STORAGE=$(wildcard ~/storage/*/*/*/*)
FILES=$(shell find $(STORAGE))

push: README.md
	git commit -am update
	git push origin master

README.md: storage.i80.mysql-8.0.15.html storage.i80.mongo-4.1.8.html storage.i80.mysql-5.7.25.html storage.i44.mongo-v3.6.3.html storage.i44.mysql-5.7.25.html
	./README.sh $^ > $@

storage.csv: $(FILES)
	./src/storage.py -o $@ $(STORAGE)

storage.i80.mongo-4.1.8.csv: storage.csv
	./src/select.py -i storage.csv -o $@ 'machine==i80' 'engine==mongo v4.1.8'
storage.i80.mongo-4.1.8.html: storage.i80.mongo-4.1.8.csv
	./src/plotly/throughput.py -o $@ $<

storage.i80.mysql-8.0.15.csv: storage.csv
	./src/select.py -i storage.csv -o $@ 'machine==i80' 'engine==mysql 8.0.15'
storage.i80.mysql-8.0.15.html: storage.i80.mysql-8.0.15.csv
	./src/plotly/throughput.py -o $@ $<

storage.i80.mysql-5.7.25.csv: storage.csv
	./src/select.py -i storage.csv -o $@ 'machine==i80' 'engine==mysql 5.7.25'
storage.i80.mysql-5.7.25.html: storage.i80.mysql-5.7.25.csv
	./src/plotly/throughput.py -o $@ $<

storage.i44.mongo-v3.6.3.csv: storage.csv
	./src/select.py -i storage.csv -o $@ 'machine==i44' 'engine=mongo v3.6.3'
storage.i44.mongo-v3.6.3.html: storage.i44.mongo-v3.6.3.csv
	./src/plotly/throughput.py -o $@ $<

storage.i44.mysql-5.7.25.csv: storage.csv
	./src/select.py -i storage.csv -o $@ 'machine==i44' 'engine==mysql 5.7.25'
storage.i44.mysql-5.7.25.html: storage.i44.mysql-5.7.25.csv
	./src/plotly/throughput.py -o $@ $<

clean:
	rm -f *.csv
