(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s)))

(define (caddr s) (car (cdr (cdr s))))

(define (ascending? asc-lst)
  (cond 
    ((null? (cdr asc-lst))
     #t)
    ((> (car asc-lst) (cadr asc-lst))
     #f)
    (else
     (ascending? (cdr asc-lst)))))

(define (square n) (* n n))

(define (pow base exp)
  (cond 
    ((= base 1)
     1)
    ((= exp 1)
     base)
    ((even? exp)
     (pow (square base) (quotient exp 2)))
    (else
     (* base
        (pow (square base) (quotient (- exp 1) 2))))))
