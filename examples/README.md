# Example ChIkEn Programs

## hello.chiken
```
have name = "World"
say "Hello, " + name
```

Run with: `chiken hello.chiken`

## factorial.chiken
```
func factorial(n) {
  if (n <= 1) {
    return 1
  } else {
    return n * factorial(n - 1)
  }
}

say "5! = " + factorial(5)
say "10! = " + factorial(10)
```

## fibonacci.chiken
```
func fib(n) {
  if (n <= 1) {
    return n
  } else {
    return fib(n - 1) + fib(n - 2)
  }
}

have i = 0
repeat (i < 10) {
  say fib(i)
  have i = i + 1
}
```

## calculator.chiken
```
func add(a, b) {
  return a + b
}

func multiply(a, b) {
  return a * b
}

func power(base, exp) {
  return base * base
}

say "5 + 3 = " + add(5, 3)
say "5 * 3 = " + multiply(5, 3)
say "5^2 = " + power(5, 2)
```

## is_prime.chiken
```
func is_prime(n) {
  if (n <= 1) {
    return 0
  }
  have i = 2
  repeat (i * i <= n) {
    if (n % i == 0) {
      return 0
    }
    have i = i + 1
  }
  return 1
}

have num = 17
if (is_prime(num) == 1) {
  say num + " is prime"
} else {
  say num + " is not prime"
}
```
