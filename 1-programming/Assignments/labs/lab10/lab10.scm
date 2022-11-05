(define (over-or-under num1 num2)
  (cond 
    ((< num1 num2) -1)
    ((> num1 num2) 1)
    (else          0)))

(define (make-adder num) (lambda (i) (+ num i)))

(define (composed f g) (lambda (x) (f(g x)))) 

(define lst `((1) 2 (3 4) 5))

(define (duplicate lst) 
  (if (null? lst) 
    ()
    (cons (car lst) (cons (car lst) (duplicate (cdr lst))))
  )   
)

