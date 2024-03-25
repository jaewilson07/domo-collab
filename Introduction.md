# Intro to Jupyter Workspaces

Presented by [Jae Wilson](https://www.linkedin.com/in/jaewor/) and [Riley Stahura](https://www.linkedin.com/in/riley-stahura-022128121) @ [Domopalooza 24](https://www.domo.com/domopalooza)

### Audience

Domo Data Specialists with Intermediate to advanced Python coding experience

### Prerequisite Domo University Courses

- Working with DataSets in Domo
- Transforming Data in Domo

You can enroll in these courses at any time though Domo University.

### Description

Jupyter Workspaces in Domo is a web-based interactive development environment for Jupyter notebooks, code, and data. In this course, you’ll learn how to integrate Jupyter into your Domo data connection and transformation pipeline.

## 🥅 Learning Objectives

---

Upon completing this course learners should be able to:

- Create and run a Jupyter Workspace DataFlow in Domo
- Integrate input and output DataSets with Jupyter Workspaces
- Create accounts in Domo for secure programmatic credential access
- Setup scheduling/triggering for Jupyter Workspaces DataFlows

## 📋 Agenda

---

### Welcome and Introduction to Jupyter

#### 1300 - Introduction & Workspaces Setup

- Introductions & Objectives
- Jupyter and Domo
- Where is Jupyter located in Domo?
- Workspace Configuration
- Optional Configuration Steps

  - Input Datasets
  - Output Datasets
  - Accounts
  - File Share
    <br>

**Jupyter Workspaces Setup**

- ▶️Login at [domo-training-jupyter](https://domo-training-jupyter.domo.com) OR [domo-community](http://domo-community.domo.com)

  - if you need to be domo'ed to the community instance let the TAs know.

- for training-jupyter:

  - username <youremailprefix>@domosftware.net
  - password Training!

- ▶️ Spin up a Jupyter Workspace
- ▶️ Clone [GitHub repo](https://github.com/jaewilson07/domopalooza-24.git) via terminal

  ```
  git clone https://github.com/jaewilson07/domopalooza-24.git
  ```

  <br>

#### Tutorial 1 - Authentication in Domo

- API request basics
- token-based authentication
- network monitoring for API discovery

### 1400 - Workspace Management

- Changing Workspace Ownership
- Enabling Sharing and Sharing a Workspace
  <br>
- ▶️ Create a "DomoAccessToken" and "Abstract Credentials Store" account containing userame & password. Share w. JupyerWorkspace
- ▶️ Add an Output Dataset - "AccountList" to JupyterWorkspace
  <br>
- Creating a Jupyter Notebook
- Left-hand navigation - Files, Input/Output Datasets, Accounts
- Domo Jupyter Library
  - Reading and Writing to a Dataset
  - Getting Account Credentials

#### Tutorial 2 & Break - Workspace Management, Working with Accounts & Domo Integration

- Read Account Objects in Jupyter Workspaces
- Export a dataframe to a Domo Dataset

### 1500 - Using DomoJupyter for Automation

- Trigger from Dataset
- Trigger on Schedule

#### Tutorial 3 - Generate a DomoStats style dataset

- Get Accounts from DomoAccounts and format as a dataset
- Merging API requests in a dataset

#### Tutorial 4 - (EXTRA) Access Token Authentication and updating Domo via API

- generate an access_token and update an Account Object in Domo

### 1545 - Q&A Wrapup

- Common Use Cases
- Q&A
- [End of course Survey Link](https://domo.az1.qualtrics.com/jfe/form/SV_6QjzvNqLHyuDcai)
