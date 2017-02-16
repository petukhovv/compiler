TESTS=001 002 
EXPRTESTS=$(addprefix expr, $(TESTS))
CTESTS=$(addprefix c, $(TESTS))

.PHONY: check $(EXPRTESTS) $(CTESTS) $(CTESTSO)

check: prepare $(EXPRTESTS) $(CTESTS) $(CTESTSO) complete

complete:
	paste -d'\t' names.data o0.data expr.data expr-so.data o3.data >> data.gnuplot && gnuplot script.gnuplot

prepare: 
	rm -rf *.data && for i in $(TESTS) ; do echo $$i >> names.data ; done && echo "Test\tgcc-O0\texpr\texpr-so\tgcc-O3" > data.gnuplot

$(CTESTS): %: %.c 
	gcc -o $@-O0 -m32 -O0 $< && /usr/bin/time -o o0.data --append -f '%U' ./$@-O0 > $@.log && diff $@.log orig/`echo $@.log | sed 's/^c/expr/'` 
	gcc -o $@-O3 -m32 -O3 $< && /usr/bin/time -o o3.data --append -f '%U' ./$@-O3 > $@.log && diff $@.log orig/`echo $@.log | sed 's/^c/expr/'` 

$(EXPRTESTS): %: %.expr
	RC_RUNTIME=../../runtime ../../rc.native -o  $< && /usr/bin/time -o expr.data    --append -f '%U' ./$@ > $@.log | tr -d '\n' >> data.gnuplot && diff $@.log orig/$@.log

clean:
	rm -f *.log *.s *~ $(TESTS)
