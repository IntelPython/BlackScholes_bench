# Copyright (C) 2014-2015, 2018 Intel Corporation
#
# SPDX-License-Identifier: MIT
#
# ==============================================================================
# Makefile for GNU make

# ==============================================================================
#  Content:
#      Black-Scholes formula example makefile
# ==============================================================================
#
#    Parameters of this makefile:
#    ----------------------------
#
#      TARGET_ARCH= SSE, AVX <default>, AVX2, MIC
#
#      PREC= s (float) <default>, d (double)
#
#      ACC=ha, la, ep <default> : meaning math function accuracy level
# ==============================================================================

SRC:=                      \
       data_gen.c          \
       main.c


# ==============================================================================
# ############## Configure CFLAGS  #############################################
# ==============================================================================
CC          := icc
QOPT        :=
FQOPT       :=f
EQCOLON     :="="
TARGET		:= black_scholes

CFLAGS      += -g -O3
CFLAGS      += -qopt-report
CFLAGS      += -qopt-report-phase$(EQCOLON)vec
CFLAGS      += -$(QOPT)restrict
CFLAGS      += -qopenmp
CFLAGS      += -I./

PREC ?= d
ifeq ($(PREC),d)
else
    CFLAGS += -D__DO_FLOAT__
endif

TARGET_ARCH ?= auto

ifeq ($(TARGET_ARCH),SSE)
    CFLAGS += -$(QOPT)xSSE4.2
endif
ifeq ($(TARGET_ARCH),AVX)
    CFLAGS += -$(QOPT)xAVX
endif
ifeq ($(TARGET_ARCH),AVX2)
    CFLAGS += -$(QOPT)xCORE_AVX2
endif
ifeq ($(TARGET_ARCH),MIC)
    CFLAGS += -mmic -opt-streaming-stores always
endif
ifeq ($(TARGET_ARCH),host)
    CFLAGS += -xhost
endif
ifeq ($(TARGET_ARCH),auto)
    CFLAGS += -xCORE-AVX2 -axCOMMON-AVX512
endif

ACC ?= ep
ifeq ($(ACC),ha)
    CFLAGS += -$(FQOPT)imf-precision$(EQCOLON)high -D_VML_ACCURACY_HA_
    CFLAGS += -fp-model precise
endif
ifeq ($(ACC),la)
    CFLAGS += -$(FQOPT)imf-precision$(EQCOLON)medium -D_VML_ACCURACY_LA_
endif
ifeq ($(ACC),ep)
    CFLAGS += -$(FQOPT)imf-precision$(EQCOLON)low -$(FQOPT)imf-domain-exclusion$(EQCOLON)31 -D_VML_ACCURACY_EP_
endif

# ==============================================================================
# ############## Define make rules #############################################
# ==============================================================================

all: nomkl mkl

mkl: $(TARGET)_mkl
	./$(TARGET)_mkl

nomkl: $(TARGET)
	./$(TARGET)

$(TARGET): $(SRC) black-scholes.c
	$(CC) $(CPPFLAGS) $(CFLAGS) $^ -o $(TARGET)

$(TARGET)_mkl: $(SRC) black-scholes_mkl.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -mkl -DBLACK_SCHOLES_MKL $^ -o $(TARGET)_mkl

clean:
	rm -rf *.o *.out *.optrpt $(TARGET) $(TARGET)_mkl

.PHONY: all clean mkl nomkl
