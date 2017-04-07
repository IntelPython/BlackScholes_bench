# Copyright (c) 2017, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import base_bs_erf
import numexpr as ne

def black_scholes ( nopt, price, strike, t, rate, vol ):
	mr = -rate
	sig_sig_two = vol * vol * 2
	
	P = price
	S = strike
	T = t
	
	a = ne.evaluate("log(P / S) ")
	b = ne.evaluate("T * mr ")
	
	z = ne.evaluate("T * sig_sig_two ")
	c = ne.evaluate("0.25 * z ")
	y = ne.evaluate("1/sqrt(z) ")
	
	w1 = ne.evaluate("(a - b + c) * y ")
	w2 = ne.evaluate("(a - b - c) * y ")
	
	d1 = ne.evaluate("0.5 + 0.5 * erf(w1) ")
	d2 = ne.evaluate("0.5 + 0.5 * erf(w2) ")
	
	Se = ne.evaluate("exp(b) * S ")
	
	call = ne.evaluate("P * d1 - Se * d2 ")
	put = ne.evaluate("call - P + Se ")
	
	return call, put
	
ne.set_num_threads(ne.detect_number_of_cores())
ne.set_vml_accuracy_mode('high')
base_bs_erf.run("Numexpr", black_scholes)
