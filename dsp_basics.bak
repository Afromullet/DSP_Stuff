#lang racket
(require plot)

#|
A struct representing the parameters we're using to sample a signal
fs = sampling speed
start-time = when we start to sample. This will be applied as an offset to the input. I guess this is just translates the function
Can't be initialized directly. Need to use make-sampling-params so that we can assign the T parameter
|#
(struct sampling-params (fs start-time T))

;Using a function to assign the last parameter to the sampling-params struct
(define (make-sampling-params fs start-time)
  (sampling-params fs start-time (/ 1.0 fs)))

#|
Gets the number of samples required for a given duration. Duration is in seconds
Rounds up to the nearest whole number. Might need to add a window so that we don't clip whatever we're sampling todo
|#
(define (num-samples-for-duration sample-params s)
  (ceiling(/ s (sampling-params-T sample-params))))

#|
Gets the ith sample for a sin wave.
|#
(define ((sin-wave-sample-func samp-params f start-time  )  i)
  (if (= i 0) (sin (* 2 pi start-time))
      (sin (* 2 pi f (+ start-time (* i (sampling-params-T samp-params)))))))

#|
Applies a sign function to the input function which is function-being-converted.
Rreturns 0 for all values <= 0 and 1 otherwise.
|#
(define ((square-func function-being-converted samp-params f start-time  )  i)
  (define sample-value ((function-being-converted samp-params f start-time) i))
  (if (<= sample-value 0) 0 1))


#|
f = frequency
duration = second duration. Equivalent to pulse-width for how the function is being used here. 
dividing the duration (in seconds) by the sampling period to get the number of samples needed
the sample-creation-func argument is a sample-creation function like sample-func and square-func
every function that's passed to this must follow the ((functame samp-params f start-time  )  i) parameter name. todo document this
func is the function we're sampling
sample-creation-func = the function we're
|#
(define (create-samples sample-creation-func samp-params f start-time duration)
  (define samples-needed (num-samples-for-duration samp-params duration))
  (for/list ([x (in-range samples-needed)])
    ((sample-creation-func samp-params f start-time) x)))



;Combines samples together, n number of times, spaced apart t seconds
;pri parameter in microseconds
;pulse-width parameter is in microseconds
;Todo this isn't complete yet
(define (create-pulse-group sample-creation-func samp-params f start-time pulse-width pri n)
  (define pri-in-seconds (* pri 1e-6))
  (define pw-in-seconds (* pulse-width 1e-6))
  (define off-time-samples-needed (exact-ceiling (/ (- pri-in-seconds pw-in-seconds) (sampling-params-T samp-params))))
  (define off-time-samples (build-list off-time-samples-needed (const '0)))
  (define on-time-samples (create-samples sample-creation-func samp-params f start-time pw-in-seconds))

  (build-list n (const '(on-time-samples off-time-samples)))
  )
  
 

;Testing parameters
(define test-sample-params (make-sampling-params  10 1))
(define test-start-time 0)
(define test-stop-time 10)
(define test-duration 3)
(define test-freq 3)
(define num-samps (num-samples-for-duration test-sample-params test-duration))
(define test-pulse-width 0.5)
(define test-pri 500)

;(define test-samples   (create-samples wave-sample-func test-sample-params test-freq test-start-time test-duration))
;(define x-axis    (for/list ([i (in-range num-samps)]) i))

;(define plot-points (map vector x-axis test-samples))


;(plot (points plot-points))

 ;;(create-samples sample-func sin test-sample-params test-freq test-start-time test-duration)
;(define x-ax (for/list ([i (in-range (num-samples-for-duration test-sample-params ))]) i))


;(plot (function  (square-func wave-sample-func test-sample-params 3 0 ) 0 test-duration))
;(plot (function  (wave-sample-func test-sample-params 3 0 ) 0 test-duration))

;(create-pulse-group wave-sample-func test-sample-params num-samps test-start-time test-pulse-width test-pri 5)

(define a (create-samples sin-wave-sample-func test-sample-params test-freq 0 1))