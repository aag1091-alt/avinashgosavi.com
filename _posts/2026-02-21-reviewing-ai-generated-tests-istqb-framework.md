---
layout: post
title: "Are These AI-Generated Tests Good?"
permalink: /post/reviewing-ai-generated-tests-istqb-framework/
read_time: 8
---

I use AI to generate a lot of tests now. It saves time, but fast output can create false confidence.

Even if AI-generated code is 99% accurate, we still need tests for the same reason as always: **catching regressions before users do.**

From experience, I can usually spot missing cases during review. But while writing this down, I wanted more than instinct — I wanted a framework that is easy to explain and repeat. [ISTQB](https://istqb-glossary.page/) definitions align well with how I already think, so I use them as the foundation.

---

## Test Level vs Test Type

**ISTQB defines *test level* as:**

> "A group of test activities that are organized and managed together."

**ISTQB defines *test type* as:**

> "A group of test activities aimed at testing specific characteristics."

That gives me a clear way to evaluate AI-generated tests: classify by level, classify by type, then check coverage and signal.

---

## Running Example

**Feature:** password reset

**Expected behavior:**

- User requests reset link
- Email is sent with token
- Token expires
- Token is single-use
- Password updates
- Old password no longer works

---

## Low Signal vs High Signal

**Low-signal test:**

```ruby
it "returns success" do
  post :create, params: { email: user.email }
  expect(response).to have_http_status(:ok)
end
```

**Higher-signal test:**

```ruby
it "creates a single-use token and sends reset email" do
  expect {
    post :create, params: { email: user.email }
  }.to change(PasswordResetToken, :count).by(1)

  token = PasswordResetToken.last

  expect(token.used_at).to be_nil
  expect(ActionMailer::Base.deliveries.last.to).to include(user.email)
end
```

The second test asserts *what* changed — token count, token state, email delivery — instead of only that the controller returned 200. That distinction matters when reviewing AI output: AI tends to generate the first kind because it is easier to write and harder to fail.

---

## Actionable Review Algorithm

When I review a PR with AI-generated tests, I run through this sequence:

1. **Collect** all new and changed tests in the PR.
2. **Classify** each test by ISTQB test level.
3. **Classify** each test by ISTQB test type.
4. **Map** tests to Jira acceptance criteria.
5. **Cross-check** requirement docs for edge cases and failure paths.
6. **Check external impact coverage:**
   - API contracts
   - Downstream consumers
   - DB side effects
   - Jobs and events
   - Third-party boundaries
7. **Weight confidence:**
   - *Highest:* system + acceptance + functional
   - *Medium:* integration + change-related regression
   - *Lower:* component-only checks
   - *Lowest:* smoke/startup/load-only checks
8. **Publish** a short gap summary in the PR.

---

## Scoring Example

PR contains:

- 2 component functional tests
- 1 component integration test
- 1 system functional test
- 1 acceptance regression test
- 2 smoke checks

**Initial result:** Decent baseline, but incomplete if no system integration test validates the email provider failure path.

**Action:** Add one integration contract test and re-score.

---

## AI Test Quality Checklist

Use this when reviewing a PR that includes AI-generated tests:

- [ ] Tests classified by **level** (Component, Component Integration, System, System Integration, Acceptance)
- [ ] Tests classified by **type** (Functional, Non-functional, Black-box, White-box, Change-related)
- [ ] Jira acceptance criteria mapped to explicit assertions
- [ ] Requirement doc edge cases and failure paths covered
- [ ] External impact covered (API contracts, downstream consumers, jobs/events, side effects)
- [ ] Regression protection added for changed behavior
- [ ] High-signal vs low-signal mix summarized
- [ ] Known gaps documented with a follow-up plan

---

AI helps me generate tests faster. This framework helps me trust what I ship.

**Sources:**

- [ISTQB Glossary: Test Level](https://istqb-glossary.page/test-level/)
- [ISTQB Glossary: Test Type](https://istqb-glossary.page/test-type/)
- [ASTQB: Test Levels and Test Types](https://astqb.org/2-2-test-levels-and-test-types/)
