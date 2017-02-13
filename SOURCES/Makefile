# Makefile for mod_remoteip.c (gmake)
APXS=$(shell which apxs || which apxs2) 

default: mod_remoteip.o

mod_remoteip.o: mod_remoteip.c
	$(APXS) -c -n mod_remoteip.so mod_remoteip.c
