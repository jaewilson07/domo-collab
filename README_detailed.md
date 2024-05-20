## Introduction

Recently, several high profile projects have gone live with Custom Apps and DDX bricks which bring a whole new set of governance and maintenance questions and concerns, to say nothing of the recent release of App Studio.

We are looking at the option of bringing Noah Finberg to London to conduct workshops and brainstorming / solution design sessions on how we might leverage CodeEngine, Workflows, Custom Apps and App Studio in our environment.

### General Topics of Interest

Custom Apps and DDX bricks
Guidelines and best practices
Guidelines for custom app development in Publish framework
Custom landing pages in distribution center

CodeEngine and Workflows
Custom apps calling Code Engine/workflows
Call “undocumented” APIs from DDX/Custom Apps
Use service account (impersonalization)
AppDB usage for configuration storage

## Tentative Agenda

Notes from Users -

- Before 30th (Jordan Atkins)

**Monday - 27 - Travel Day**
**Tuesday - 28**

- Noah recovery
  - JW + OZ @ SIE - planning
  - Evening - a Cheeky Nandos

**Wednesday - 29**

- Morning

  - JW + JT + JZ
  - Noah @Domo EMEA

- 11:00 - 11:30 - Femi / D2C (support in migrating a dashboard to.

  - https://playstation-d2c.domo.com/page/1424939153 and its subpages)

- Afternoon
  - Session 1: Just CodeEngine
- Evening > Ramen (Tokontsu / Big Daddy)

**Thursday - 30**

- Morning
  - Session 2: Basic Personalization with Apps (landing page)
- Afternoon
  - Session 3: App +CodeEngine
  - Solutioning / Workshops / Office Hours

**Friday - 31**

- Code Review Process (morning)

- Office Hours

- Afternoon
  - Travel home

## Session 1 - Basic CodeEngine (add a user to a Group)

Correct way to handle authentication (in codeengine) // can we SUDO handle modify group membership?

## Session 2 - Basic Personalization with Apps (landing page)

Use Case: “You have access to 100 dashboards, how do you see the ‘most important ones’

- Most important one changes per user
- Most important one can change based on time of year // a new incident

Fun Challenges

- Mapping names to entity_ids that might change (because publish) -- use API > Publish > Subscriber > Details
- Generate Navigation Components (button to a dashboard) in javascript

- Introduces best practices > using other parts of Domo
  - Read a Dataset - PDP vs Filter Query?

https://github.com/jaewilson07/datacrew/tree/main/ddx_bricks/jaewilson07/personalization

Question

- Can you dynamically restructure a dashboard?
- Can you pass filters into an embed link (an dashboard in an iframe)

## Session 3 - Using Apps + CodeEngine (sharing content)

Use Case - build an app that allows content managers to monitor and share content with users

Tutorial Outline

- DDX > consolelog list of pages I am owner of
- construct a Drop down > (actionHandler) > select a page

- Print group membership
- Add an Input (add user) > submit > submitHandler
- Modify group membership // this will require CodeEngine

## Overarching Themes

- How does it deploy with cross-instance(from dev to prod)using (codeegine & appdb )
- What happens if i publish multiple instances of a card that should point to the same appdb collection
- Keep in mind most users are not ‘admins’
