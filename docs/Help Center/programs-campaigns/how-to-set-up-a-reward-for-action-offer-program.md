---
title: "How to Set Up a Reward for Action Offer Program"
excerpt: "Learn how to set up a simple reward for action program to reward participants for completing a survey, signing up for e-statements and more.\n"
---


# Overview

This guide walks through how to configure a **Reward for Action Program** that issues a reward to a group of users - for example, a $25 Amazon.com gift card to participants who complete a survey.

This setup assumes the survey is hosted outside of Extole and events are sent in via batch upload or the Create Event page.

# Configuration Steps

## Step 1: Add the Offers Program

1. On the programs page, click + New Program
2. Choose the Reward for Action program (talk to your CSM if it’s not available)
3. Choose to add it as a new program or add to an existing program and give it a name.

>

> It’s recommended to create a new program for each campaign audience.

## Step 2: Update the Outcome Event Name and Trigger Rule

> Configure the default Outcome event so it listens for the correct incoming event.  
​

### **Update the event name**

1. In the **Flow** tab, select the **Outcome** event.
2. Update the **Event Name** to match the event that will be sent into Extole.

  - This event name will be used in a **batch file upload**, API request, or the **Create Event** page

### **Using a Different Incoming Event Name (Advanced)**

> By default, event will be triggered based on that event name (ex. **Survey Reward** event name is triggered by the input event of the same name "survey_reward").

>

> If the incoming input event name should **be different than** the Event Name:

1. Click into **Triggered on Input Event**.

  1. If Trigger Rules are not visible, enable **Advanced** and/or **Expert** filters.

2. Navigate to **Trigger Event Names**.
3. Click **Edit**.
4. In **Values**:

  - Remove the default value (for example, survey_reward).
  - Add a **New Value** with the desired incoming event name.

5. Click **Apply**.
6. To avoid confusion, rename the Triggered on Input Event rule to clearly indicate the input event name it is triggered by.

> Example:

- Outcome Event Name: Survey Reward
- Trigger Rule: Triggered on Input Event - changed to Input Event send_reward
- Incoming Event that Triggers Event: `send_reward`

## Step 3: Update the Reward Name & Rules

### **Update the Reward**

1. Select the **Participant** **Reward** in the Flow.
2. Update the **Reward Name** and description to clearly describe the incentive.
3. Update the reward to either a test reward, or your PROD reward. Rewards can be created by following these steps:

  1. **[Gift Card Rewards](doc:how-to-reward-with-tango-gift-cards)**
  2. **[Coupon Rewards](doc:how-to-reward-with-coupons)**
  3. **[Account Credit Rewards](doc:how-to-reward-with-account-credits)**

### **Configure the Reward Rules Behavior**

1. Review **Reward Rules** and keep only those required for a simple survey or welcome offer. Default Rules you *may not* need:

  1. Business Event Quality if there are no other rules on the event itself
  2. Reward Limit
  3. Has Not Been Rewarded  
​

2. Review **Reward Behavior** to choose when to reward a user

  1. **First Action (most common)  
​** Reward is issued only the first time the event occurs.
  2. **Every Action  
​** Reward is issued every time the event occurs.
  3. **Every Unique Action  
​** Reward is issued once per unique value of a specified data parameter.

## Step 4: Configure the Reward Email

1. Follow these instructions to configure the **[Tango Reward Email](doc:how-to-set-up-a-tango-gift-card-reward)**
2. Follow these instructions to configure a **Tremendous Reward Email (coming soon).**

## Step 5: Test Using a CSV Event Upload

### **Create the CSV file**

> Create a CSV with the following column headers:

- event_name
- email
- required_labels

### **Populate values**

- **event_name**: The incoming event name (for example, survey_reward)
- **email**: Recipient’s email address
- **required_labels**: Program label

> Find the program label by clicking the view button on the Programs Page.

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2024153388/0e665bbdc9ca27d55c1ac7533591/f6dee104-13cd-4350-b67a-dd903df2f0ca?expires=1778306400&signature=de114d1e0f1b24acfb6c50d114153df1a2fb7cc806146691dee8c660f826ef9a&req=diAlEsh7noJXUfMW3nq%2BgRYdnAS02HL78qg20LVm6Kp%2FvhyqiELzGumkBGK7%0AoSITsz2Sx8aAl3epEpcoQTF3CHo%3D%0A)

>

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2024153390/b2897df4a1d8b020414a8b78b3da/79f741af-a29c-4a0e-95de-c82c4bcf72c2?expires=1778306400&signature=0a2fbfa2e894f4617be0d3c85ef10149fbee1c4f6945abc2f147accef54da3ab&req=diAlEsh7noJWWfMW3nq%2BgRB3eVh5BxSr08jt%2B2dwjJ3yrOtpB%2BL%2BzBvzcUbk%0A7LsMY%2BEdrZC2MKAXGE1KkCKQXLg%3D%0A)

>

## Step 6: Test, Validate, and Launch the Offer

### **Test the program**

1. Set the **campaign to Live**.
2. Navigate to **Tech Center → Batch Jobs**.
3. Upload the CSV file using the format above with a test email address and click Save
4. After the events have processed:

  - Go to User Support and search for the user.
  - Confirm the **test reward** is sent as expected and that you received the reward email. 
  - Verify reward behavior (for example, only rewarded once)

### **Move to production**

1. Replace the test reward with the **PROD reward**.
2. Save and apply changes.
3. **Publish the campaign**.

### **Send production rewards**

- Use the **same CSV format**
- Upload the recipient list through **Batch Jobs** to issue rewards

# Common Customizations to Reward for Action Campaigns

## Send Multiple Reward Values

> In many cases, you may have some participants earning either a $50 reward or a $100 reward. If you want to upload them in one file, you will need to add a column for reward_value and make the following changes:

>

### Step 1: Add Reward Value Data to Event

1. Click into the outcome step (example Survey Reward) and click + New Data
2. Choose **Business Event Data** from the list
3. Rename it to Reward Value

### Step 2: Configure the First Reward

1. Click into the **reward** and under Trigger Rules click **+ New Reward Rule**
2. Select Reward Data Comparison and rename it Reward Value is $XXX
3. For the **Journey Parameter**, you want to use the name of the Business Event data with underscores instead of spaces and then choose Equals and enter the value.

![](https://downloads.intercomcdn.com/i/o/syy27wia/2024261521/c78878b7feb25f75b64c6deb1718/image.png?expires=1778306400&signature=5a203271abbbcaefb1c1843bbd7553d01fda76ebd6167dace553adc1b78aae62&req=diAlEst4nIRdWPMW3nq%2Bgb8Sibd86mc%2FJrogGR7EwLz1PplJNJaaWaEFCUkf%0ABAcDSmOwvQt1IHXXT2LBpVEST94%3D%0A)

>

> This trigger rule is indicating it should only trigger the reward, if the `reward_value` is `200`.

## Step 3: Add and Configure the Second Reward

1. On the flow page, find the step you want to send a reward on and click the + button
2. Choose Add Reward and Participant  
​![](https://downloads.intercomcdn.com/i/o/syy27wia/2024273874/5610a20b46ed8a3a17d3f77844b2/image.png?expires=1778306400&signature=d4047113d3f28417f57ec50b65718f6be4a44d0588278b989122c724b37385a5&req=diAlEst5nolYXfMW3nq%2Bgf92hDAH9j9abE%2BZ%2BCuDlsQtuf71PCXA3OWAl69W%0A5ap%2Btgm4CQ9RwiMl72GE8dFwHT8%3D%0A)
3. Rename this Reward so it is differentiated from the first reward
4. Repeat Step 2 to configure this new reward for the additional reward values.
