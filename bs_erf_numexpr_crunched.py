import base_bs_erf
import numexpr as ne

def black_scholes ( nopt, price, strike, t, rate, vol ):
    mr = -rate
    sig_sig_two = vol * vol * 2
    
    P = price
    S = strike
    T = t

    call = ne.evaluate("P * (0.5 + 0.5 * erf((log(P / S) - T * mr + 0.25 * T * sig_sig_two) * 1/sqrt(T * sig_sig_two))) - S * exp(T * mr) * (0.5 + 0.5 * erf((log(P / S) - T * mr - 0.25 * T * sig_sig_two) * 1/sqrt(T * sig_sig_two))) ")
    put = ne.evaluate("call - P + S * exp(T * mr) ")
    
    return call, put
        
#ne.set_vml_num_threads(ne.detect_number_of_cores())
ne.set_num_threads(ne.detect_number_of_cores())
ne.set_vml_accuracy_mode('high')
base_bs_erf.run("Numexpr-opt", black_scholes)
