TESTS=$(basename $(sort $(wildcard generated*.expr)))

.PHONY: check $(TESTS)

check: $(TESTS)

$(TESTS): %: %.expr
	cat $@.input | RC_RUNTIME=../../runtime ../../rc -i $< > $@.log && diff $@.log orig/$@.log
	cat $@.input | RC_RUNTIME=../../runtime ../../rc -s $< > $@.log && diff $@.log orig/$@.log
	RC_RUNTIME=../../runtime ../../rc -o  $< && cat $@.input | ./$@ > $@.log && diff $@.log orig/$@.log

clean:
	rm -f *.log *.s *~ $(TESTS)
