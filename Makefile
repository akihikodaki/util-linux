# Makefile for source rpm: util-linux
# $Id$
NAME := util-linux
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
