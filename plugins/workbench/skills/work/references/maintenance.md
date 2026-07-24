# Maintenance and Simplification

Use this reference both for cleanup embedded in delivery and for standalone
cleanup, simplification, refactor, or technical-debt outcomes.

For embedded maintenance, include only cohesive behavior-preserving cleanup
exposed by the current delivery. Park broader opportunities.

For standalone maintenance, create an ordinary feature or story with a bounded
surface, reason the current structure is costly or unsafe, invariants to
preserve, observable completion evidence, and rollback or migration concerns
where relevant. Tag it `cleanup` or `refactor`; use an epic only when several
independently verifiable subsystems need durable coordination. Separate or
explicitly gather requirements for intended behavior changes rather than
hiding them inside a purportedly behavior-preserving refactor.

Then:

1. Eliminate obsolete concepts, code, configuration, and compatibility before
   adding new machinery.
2. Follow demonstrated repository patterns where they remain sound.
3. Improve boundaries when the current change exposes a real responsibility or
   contract problem.
4. Include cohesive behavior-preserving cleanup that makes the delivery safer
   or simpler.
5. Park valuable broader findings instead of expanding the current scope.

Treat roughly three genuine occurrences as a useful recurrence signal, not a
quota. Promote a reusable project pattern only when it has concrete consumers
and reduces future ambiguity. Do not harvest aesthetic coincidence or churn
unrelated code into conformity.
