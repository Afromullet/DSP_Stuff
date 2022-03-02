#lang racket
(require plot)


;;;A struct representing the parameters we're using to sample a signal
;;;fs = sampling speed
;;;start-time = when we start to sample. This will be applied as an offset to the input. I guess this is just translates the function
;;;Can't be initialized directly. Need to use make-sampling-params so that we can assign the T parameter
(struct sampling-params (fs start-time T))

;;;Using a function to assign the last parameter to the sampling-params struct
(define (make-sampling-params fs start-time)
  (sampling-params fs start-time (/ 1.0 fs)))

;;;Gets the number of samples required for a given duration. Duration is in seconds
;;;Rounds up to the nearest whole number. Might need to add a window so that we don't clip whatever we're sampling todo
(define (num-samples-for-duration sample-params s)
  (ceiling(/ s (sampling-params-T sample-params))))

;;;Creates the samples for a sin wave
(define ((sin-wave-sample-func samp-params f start-time  )  i)
  (if (= i 0) (sin (* 2 pi start-time))
      (sin (* 2 pi f (+ start-time (* i (sampling-params-T samp-params)))))))

;;;Applies a sign function to the input function which is function-being-converted.
;;;Rreturns 0 for all values <= 0 and 1 otherwise.
(define ((square-func function-being-converted samp-params f start-time  )  i)
  (define sample-value ((function-being-converted samp-params f start-time) i))
  (if (<= sample-value 0) 0 1))

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

;Combines samples together, n number of times, spaced apart t seconds
;pri parameter in microseconds
;pulse-width parameter is in microseconds
;Todo this isn't complete yet
(define (create-pulse-group sample-creation-func samp-params f start-time pulse-width pri n)
  (define pri-in-seconds (* pri 1e-6))
  (define pw-in-seconds (* pulse-width 1e-6))
  (define off-time-samples-needed (exact-ceiling (/ (+ pri-in-seconds pw-in-seconds) (sampling-params-T samp-params))))
  (define off-time-samples (build-list off-time-samples-needed (const '0)))
  (define on-time-samples (create-samples sample-creation-func samp-params f start-time pw-in-seconds))
  (define combined-samples (for/list ([i (in-range n)]) ( cons on-time-samples off-time-samples )))
  (flatten combined-samples)
  )
  
;;;Returns the x axis required for plotting the samples
;;;Need the sample params because we use the sampling period to determine the x-axis points
;;i.e, x(0) = sampling-period * 0, x(5) = sampling-period * 5, and so on
(define (get-sample-x-axis num-of-samples samp-params)
  (for/list ([i (in-range num-of-samples)])
    i)
  )


;Testing parameters
(define test-sample-params (make-sampling-params  44100 1))
(define test-start-time 0)
(define test-stop-time 10)
(define test-duration 3)
(define test-freq 300)
(define num-samps (num-samples-for-duration test-sample-params test-duration))
(define test-pulse-width 10000)
(define test-pri 10000)

(define test-samples   (create-samples sin-wave-sample-func test-sample-params test-freq test-start-time test-duration))
(define test-samples-x-axis    (for/list ([i (in-range (length test-samples))]) i))
(define test-samples-plot-points (map vector test-samples-x-axis test-samples))
(plot (lines test-samples-plot-points))

(define pulse-group-samples (create-pulse-group sin-wave-sample-func test-sample-params test-freq test-start-time test-pulse-width test-pri 5))
(define pulse-group-x-axis (get-sample-x-axis (length pulse-group-samples) test-sample-params))


;(define pulse-group-x-axis    (for/list ([i (in-range (length pulse-group-samples))]) i))
(define pulse-group-plot-points (map vector pulse-group-x-axis pulse-group-samples));
(plot (lines pulse-group-plot-points))

