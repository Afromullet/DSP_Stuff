#lang racket
(require plot)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Utility functions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Converts a microsecond pulse width to seconds
(define (pw-in-seconds pw-micro) (* pw-micro 1e-6))

;Converts a microsecond pri to seconds
(define (pri-in-seconds pri-micro) (* pri-micro 1e-6))

;Apparently racket does not have a cotangent, so this calculates the cot
(define (cot x) (/ (sin x) (cos x)))

;;;Gets the number of samples required for a given duration. Duration is in seconds
;;;Rounds up to the nearest whole number. Might need to add a window so that we don't clip whatever we're sampling todo
(define (num-samples-for-duration sample-params s)
  (ceiling(/ s (sampling-params-T sample-params))))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Plotting related utility functions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;;Returns the x axis required for plotting the samples
;;;Need the sample params because we use the sampling period to determine the x-axis points
;;i.e, x(0) = sampling-period * 0, x(5) = sampling-period * 5, and so on
(define (get-sample-x-axis num-of-samples samp-params)
  (for/list ([i (in-range num-of-samples)])
    (* (sampling-params-T samp-params )i)
  ))



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Types
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;;A struct representing the parameters we're using to sample a signal
;;;fs = sampling speed
;;;start-time = when we start to sample. This will be applied as an offset to the input. I guess this is just translates the function
;;;Can't be initialized directly. Need to use make-sampling-params so that we can assign the T parameter
(struct sampling-params (fs start-time T))

;;;Using a function to assign the last parameter to the sampling-params struct
(define (make-sampling-params fs start-time)
  (sampling-params fs start-time (/ 1.0 fs)))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Function based sample creation
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;Creates the samples for a sin wave
(define ((sin-wave-sample-func samp-params f start-time  )  x)
  (if (= x 0) (sin (* 2 pi start-time))
      (sin (* 2 pi f (+ start-time (* x (sampling-params-T samp-params)))))))


;;;Uses the sawtooth function of the form y(x) = - 2a/pi * arctan (cot (pi*x/f))
;;;Not using amplitude at the moment
;;;cotan-arg is the cotangent part that's the input to the arctan
(define ((sawtooth-sample-func samp-params f start-time )x)
  (let ([cotan-arg (cot (/ (* pi x) f))])
    (* (/ 2 pi) (atan cotan-arg))))
  
  
;;;Applies a sign function to the input function which is function-being-converted.
;;;Rreturns 0 for all values <= 0 and 1 otherwise.
(define ((square-func function-being-converted samp-params f start-time  )  x)
  (define sample-value ((function-being-converted samp-params f start-time) x))
  (if (<= sample-value 0) 0 1))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Sample-period bnased sample creation
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;f = frequency
;;;duration = second duration. Equivalent to pulse-width for how the function is being used here. 
;;dividing the duration (in seconds) by the sampling period to get the number of samples needed
;;the sample-creation-func argument is a sample-creation function like sample-func and square-func
;;;every function that's passed to this must follow the ((functame samp-params f start-time  )  i) parameter name. todo document this
;;;func is the function we're sampling
;;sample-creation-func = the function we're getting the samples of
(define (create-samples sample-creation-func samp-params f start-time duration)
  (define samples-needed (num-samples-for-duration samp-params duration))
  (for/list ([x (in-range samples-needed)])
    ((sample-creation-func samp-params f start-time) x)))

;Creates a single pulse of a certain pulse width
(define (create-pulse  sample-creation-func samp-params f start-time pulse-width)
  (define pw (pw-in-seconds pulse-width))
  (create-samples sample-creation-func samp-params f start-time pw))

;Calculates the off-time between pulses for a given pri and pulse width
;todo make the off time samples into a let to make it more clear
(define (calculate-pulse-off-time samp-params pri-micro pw-micro)
  (define off-time-samples-needed (exact-ceiling (/ (- (pri-in-seconds pri-micro) (pw-in-seconds pw-micro) (sampling-params-T samp-params)))))
   (build-list off-time-samples-needed (const '0)))

;Combines samples together, n number of times, spaced apart t seconds
;pri parameter in microseconds
;pulse-width parameter is in microseconds
;Todo this isn't complete yet, I don't think it does what I want it to do
;todo make sure that we just use one pulse width rather than the converted and non converted version
(define (create-pulse-train sample-creation-func samp-params f start-time pri pulse-width n)
  (define pulse (create-pulse sample-creation-func samp-params f start-time pulse-width))
  (define off-time (calculate-pulse-off-time samp-params pri pulse-width))
  (flatten (make-list n (cons pulse off-time))))



 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Declarations of values used for testing
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;Testing parameters
(define test-sample-params (make-sampling-params  576000 1))
(define test-start-time 0)
(define test-stop-time 10)
(define test-duration 0.1)
(define test-freq 5000)
(define num-samps (num-samples-for-duration test-sample-params test-duration))
(define test-pulse-width 100) 
(define test-pri 1000)
(define test-micro-pw (pw-in-seconds test-pulse-width))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Plotting things. This is basically the main section of the script
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define pulse-group-samples (create-pulse-train sin-wave-sample-func test-sample-params test-freq test-start-time test-pri test-pulse-width  3))
(define pulse-group-x-axis (get-sample-x-axis (length pulse-group-samples) test-sample-params))
(define pulse-group-plot-points (map vector pulse-group-x-axis pulse-group-samples))
(plot (lines pulse-group-plot-points))

(define sawtooth-samples (create-samples sawtooth-sample-func test-sample-params test-freq test-start-time test-duration))
(define sawtooth-x-axis (get-sample-x-axis (length sawtooth-samples) test-sample-params))
(define sawtooth-plot-points (map vector sawtooth-x-axis sawtooth-samples))
(plot (lines sawtooth-plot-points))



