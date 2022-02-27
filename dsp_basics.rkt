#lang racket
(require plot)

;Sampling parameters
;fs = sampling speed
;start-time = when we start sampling
(struct sampling-params (fs start-time T))

;Using a function to assign the last parameter to the sampling-params struct
(define (make-sampling-params fs start-time)
  (sampling-params fs start-time (/ 1.0 fs)))

;Gets the number of samples required for a given duration. Duration is in seconds
;Rounds up to the nearest whole number. Might need to add a window so that we don't clip whatever we're sampling todo
(define (num-samples-for-duration sample-params s)
  (ceiling(/ s (sampling-params-T sample-params))))



;Gets the ith sample for function.
;function-being samples is the...function we're sampling
;start-time if an offset added to teh sampled polint
;

;f = frequency
(define ((sample-func function-being-sampled samp-params f start-time  )  i)
  (if (= i 0) (function-being-sampled (* 2 pi start-time))
      (function-being-sampled (* 2 pi f (+ start-time (* i (sampling-params-T samp-params)))))
  ))

;Applies a sign function to func, which returns 0 for all values <= 0 and 1 otherwise.
;Lets us do things like apply the sign func to sin or cos
(define ((square-func function-being-sampled samp-params f start-time  )  i)
  (define sample-value ((sample-func function-being-sampled samp-params f start-time) i))
  (if (<= sample-value 0) 0 1))

;duration is in seconds
;dividing the duration (in seconds) by the sampling period to get the number of samples needed
;the sample-creation-func argument is a sample-creation function like sample-func and square-func
;every function that's passed to this must follow the ((functame func samp-params f start-time  )  i) parameter name. todo document this
;func is the function we're sampling
;sample-creation-func = the function we're 
(define (create-samples sample-creation-func func samp-params f start-time duration)
  (define samples-needed (num-samples-for-duration samp-params duration))
  (for/list ([x (in-range samples-needed)]) ((sample-creation-func func samp-params f start-time) x) 
  ))
            
  
(define test-sample-params (make-sampling-params  10 1))
(define test-start-time 0)
(define test-stop-time 10)
(define test-duration 1)
(define test-freq 3)


(define num-samps (num-samples-for-duration test-sample-params test-duration))

(define test-samples   (create-samples sample-func sin test-sample-params test-freq test-start-time test-duration))
(define x-axis    (for/list ([i (in-range num-samps)]) i))

(define plot-points (map vector x-axis test-samples))



(plot (points plot-points))

 ;;(create-samples sample-func sin test-sample-params test-freq test-start-time test-duration)
;(define x-ax (for/list ([i (in-range (num-samples-for-duration test-sample-params ))]) i))

#|
(plot (function  (square-func sin test-sample-params 3 0 ) 0 plot-time))
(plot (function  (sample-func sin test-sample-params 3 0 ) 0 plot-time))
(plot (function  (sample-func cos test-sample-params 3 0 ) 0 plot-time))
(plot (function  (sample-func tan test-sample-params 3 0 ) 0 plot-time))
|#

