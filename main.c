/*
 * Copyright (C) 2014-2015, 2018 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdio.h>
#include <time.h>
#include "euro_opt.h"
#include "rdtsc.h"

int main(int argc, char * argv[])
{
    int nopt = 1 * 1024;
    tfloat *s0, *x, *t, *vcall_mkl, *vput_mkl, *vcall_compiler, *vput_compiler;

    clock_t t1 = 0, t2 = 0;

    /* Read nopt number of options parameter from command line */
    if (argc < 2)
    {
        printf("Usage: expect nopt input integer parameter, defaulting to %d\n", nopt);
    }
    else
    {
        sscanf(argv[1], "%d", &nopt);
    }

    int i, j;
    for(i = 0; i < 18; i++) {
    
        /* Allocate arrays, generate input data */
        InitData( nopt, &s0, &x, &t, &vcall_compiler, &vput_compiler, &vcall_mkl, &vput_mkl );

        /* Warm up cycle */
        for(j = 0; j < 10; j++) {
            BlackScholesFormula_Compiler( nopt, RISK_FREE, VOLATILITY, s0, x, t, vcall_compiler, vput_compiler );
        }

        /* Compute call and put prices using compiler math libraries */
        printf("ERF: Native-C-SVML: Size: %d MOPS: ", nopt);
        t1 = timer_rdtsc();
        for(j = 0; j < 100; j++) {
            BlackScholesFormula_Compiler( nopt, RISK_FREE, VOLATILITY, s0, x, t, vcall_compiler, vput_compiler );
        }
        t2 = timer_rdtsc();
        printf("%.6lf\n", (2.0 * nopt * 100 / 1e6)/((double) (t2 - t1) / getHz()));

        /* Compute call and put prices using MKL VML functions */
#ifdef MKL
        printf("ERF: Native-C-VML: Size: %d MOPS: ", nopt);
        t1 = timer_rdtsc();
        for(j = 0; j < 100; j++) {
             BlackScholesFormula_MKL( nopt, RISK_FREE, VOLATILITY, s0, x, t, vcall_mkl, vput_mkl );
        }
        t2 = timer_rdtsc();
        printf("%.6lf\n", (2.0 * nopt * 100 / 1e6)/((double) (t2 - t1) / getHz()));
#endif
        fflush(stdout);

        /* Deallocate arrays */
        FreeData( s0, x, t, vcall_compiler, vput_compiler, vcall_mkl, vput_mkl );

        nopt = nopt * 2;
    }

    /* Display a few computed values */
    // printf("call_compiler[0/%d]= %g\n", nopt, (double)(vcall_compiler[10]) );
    // printf("put_compiler[0/%d]= %g\n", nopt, (double)(vput_compiler[10]) );
    // printf("call_mkl[0/%d]= %g\n", nopt, (double)(vcall_mkl[10]) );
    // printf("put_mkl[0/%d]= %g\n", nopt, (double)(vput_mkl[10]) );

    return 0;
}
