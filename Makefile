TARGETS:=all update push
CONTAINERS:=docker-nrpe-common swedenconnect.se
$(TARGETS): $(CONTAINERS)
$(CONTAINERS):
	$(MAKE) -C $@

.PHONY: $(TARGETS) $(CONTAINERS)
