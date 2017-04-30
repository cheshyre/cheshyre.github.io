---
layout: default
title: Testing Features
---

~~~ruby
require "gem"

string = "base16"
symbol = :base16
fixnum = 0
float  = 0.00
array  = Array.new
array  = ['chris', 85]
hash   = {"test" => "test"}
regexp = /[abc]/

# This is a comment
class Person

  attr_accessor :name

  def initialize(attributes = {})
    @name = attributes[:name]
  end

  def self.greet
    "hello"
  end
end

person1 = Person.new(:name => "Chris")
print Person::greet, " ", person1.name, "\n"
puts "another #{Person::greet} #{person1.name}"
~~~

### A *Test* Italic

~~~java
package foo;

import java.util.Iterator;

/**
 * the fibonacci series implemented as an Iterable.
 */
public final class Fibonacci implements Iterable<Integer> {
  /** the next and previous members of the series. */
  private int a = 1, b = 1;

  @Override
  public Iterator<Integer> iterator() {
    return new Iterator<Integer>() {
      /** the series is infinite. */
      public boolean hasNext() { return true; }
      public Integer next() {
        int tmp = a;
        a *= b;
        b = tmp;
        return a;
      }
      public void remove() { throw new UnsupportedOperationException(); }
    };
  }

  /**
   * the n<sup>th</sup> element of the given series.
   * @throws NoSuchElementException if there are less than n elements in the
   *   given Iterable's {@link Iterable#iterator iterator}.
   */
  public static <T>
  T nth(int n, Iterable<T> iterable) {
    Iterator<? extends T> it = iterable.iterator();
    while (--n > 0) {
      it.next();
    }
    return it.next();
  }

  public static void main(String[] args) {
    System.out.print(nth(10, new Fibonacci()));
  }
}
~~~
