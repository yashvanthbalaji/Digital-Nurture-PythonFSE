
**Author:** Balaji A
**Program:** Cognizant Digital Nurture 5.0

---

# State Management Comparison

Built the same Student Portal in React+Redux (Hands-On 6/10), Angular
(Hands-On 7), and Vue+Pinia (Hands-On 8). Notes from that experience:

## React + Redux Toolkit
- Most boilerplate of the three, but Redux Toolkit's createSlice and
  createAsyncThunk cut that down a lot compared to "classic" Redux.
- Steepest learning curve up front (actions, reducers, thunks, selectors
  are all separate concepts you have to learn together).
- Excellent DevTools -- every action and state change is inspectable.
- Selectors decouple components from the store's exact shape, which pays
  off once the app grows.

## Angular (services + DI, NgRx concept)
- No separate state library needed for small-to-medium state -- a plain
  @Injectable service with RxJS can hold shared state.
- NgRx (not implemented here, but same Redux pattern under a different
  name: Actions, Reducers, Effects, Selectors) is usually only reached
  for once an app's state gets genuinely complex.
- Angular's DI system means services are automatically shared and easy
  to inject -- less manual wiring than Redux's Provider/store setup.
- Steepest overall framework learning curve (modules vs standalone
  components, RxJS observables, decorators), even before adding NgRx.

## Vue + Pinia
- Fastest to get shared state working -- defineStore() felt like writing
  a normal component with ref()/computed(), no separate boilerplate
  concepts to learn.
- Reactivity "just works" without extra selector functions -- any
  component reading store.enrolledCourses re-renders automatically.
- Smallest amount of code for the same enroll/unenroll/totalCredits
  functionality compared to the Redux slice version.
- Fewer built-in enforced patterns than Redux -- more flexible, but also
  easier to end up with inconsistent patterns across a larger team.

## Summary
All three solve the same problem (shared state reachable from any
component without prop drilling) with different trade-offs: Redux
trades convenience for structure and tooling, Pinia trades structure
for speed and simplicity, and Angular's DI-based services sit in
between -- simple by default, with NgRx available for teams that want
Redux-style strictness.