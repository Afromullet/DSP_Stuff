#lang racket
(require plot)



;Sampling parameters
;fs = sampling speed
;start-time = when we start sampling
(struct sampling-params (fs start-time T))

;Using a function to assign the last parameter
(define (make-sampling-params fs start-time)
  (sampling-params fs start-time (/ 1 fs)))

;Gets the number of samples required for a given duration. Duration is in seconds
(define (num-samples-for-duration sample-params s) (/ s (sampling-params-T sample-params)))

;Creates the time for the ith sample. Just multiplies the index by the sampling period
;If the input is 0 (the first point, it's just the starting time
(define (create-sample-point samp-params start-time  i)
  (if (= i 0) start-time
      (+ start-time (* i (sampling-params-T samp-params)))
  ))


;Gets a sample for func
;The func argument must be a function
;f = frequency
(define ((sample-a-func func samp-params f start-time  )  i)
  (if (= i 0) (func (* 2 pi start-time))
      (func (* 2 pi f (+ start-time (* i (sampling-params-T samp-params)))))
  ))

;Returns a sample for a sin wave of a particular frequency. 
(define ((sin-sample-point samp-params f start-time  )  i)
  (if (= i 0) (sin (* 2 pi start-time))
      (sin (* 2 pi f (+ start-time (* i (sampling-params-T samp-params)))))
  ))


;Returns a sample for a sin wave of a particular frequency. 
(define ((square-sample-point samp-params f start-time  )  i)

  (define sample-value
  (if (= i 0) (sin (* 2 pi start-time))
      (sin (* 2 pi f (+ start-time (* i (sampling-params-T samp-params)))))))
  (if (<= sample-value 0) 0 1)
  )



  



(define test-sample-params (make-sampling-params  10 1))

(define test-start-time 0)
(define test-stop-time 10)

(define plot-time (num-samples-for-duration test-sample-params 1))




(plot (function  (sin-sample-point test-sample-params 3 0 ) 0 plot-time))

(plot (function  (square-sample-point test-sample-params 3 0 ) 0 plot-time))


(plot (function  (sample-a-func sin test-sample-params 3 0 ) 0 plot-time))
