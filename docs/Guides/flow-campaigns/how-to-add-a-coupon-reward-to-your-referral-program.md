---
title: "How to Add a Coupon Reward to Your Referral Program"
excerpt: "Add coupon rewards and configure reward emails on your referral program\n"
---

💡 Important Note: This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.

![](https://files.readme.io/e6ce7ae11a54341232f15138804fc2698cd4b601182dd5fecf14ae3b494f6161-8657f60a_ed8a5dc3-f68d-4de8-b159-f90155fccbaf.png)

# Overview

This guide walks you through how to create a coupon reward and add it to your referral campaign in Extole, including optional customization for reward emails and reminders.

# **Step 1: Create a Coupon Set**

Before adding a coupon reward to a campaign, you’ll first create a coupon set that contains your coupon codes.

  1. Navigate to Rewards > Coupons

  2. Click + New Reward and create a new coupon with the following information:

     1. **Name** – Use a clear, descriptive name for internal reference.

     2. **Value** – Enter the discount amount or percentage.

     3. **Alert Threshold** – Set a threshold to be notified when coupon inventory runs low.

     4. **Limits** – (Optional) Configure hourly or daily issuance limits.

  3. Upload a CSV file containing your coupon codes.

     1. The file should contain **one column only with no header**.




Once created, this coupon set will be available to use as a reward in your campaigns.

# **Step 2: Add the Coupon Reward to Your Campaign**

  1. **Navigate to the Flow Builder**  
Go to the Programs Page, locate the program and campaign you want to edit, and click the Manage Flow icon.

  2. **Add a Reward**  
In the campaign flow, identify the event you’d like to send a reward on and click the + button.

     1. Choose whether the reward applies to the **Advocate** or the **Friend**.

     2. Select Reward and choose a descriptive name

     3. Once saved, choose the coupon reward from the dropdown




# **Step 3: Adjust Reward Rules (Optional)**

You can customize rules to control when and how the coupon reward is issued.

### **Reward Rules**

Review and update reward eligibility rules. Rewards will only be dispensed if they meet these criteria. Common rules to enable for coupon rewards:

  * **Business Event Quality**

  * **Has Email Address**

  * **Has Not Been Rewarded for Relationship**




Learn more about other reward rules **[here](https://docs.extole.com/docs/how-to-set-up-reward-rules#h_c4a7ccbfc2)**.

# **Step 4: Update the Reward Email and Reminder**

After configuring the reward, set up the email that delivers the coupon to participants.

### **Reward Email Setup**

By default the rewards are set up to support coupon code redemption. Customize the email by going to the Assets section, or by clicking into **Reward Emails** from the Flow page. 

The reward email typically includes:

  * Confirmation that the reward was earned

  * The coupon code

  * Instructions for redemption




### **Update Email Copy and Creative**

You can customize:

  * Email subject line

  * Preview text

  * Headings and body copy

  * Button text

  * Images and branding




### **Set a Custom “Shop Now” Button URL**

If you want the **Shop Now** button to link to a specific page:

  1. In the reward email editor, locate **Reward Redemption Button Destination**.

  2. Enter the full URL you want the button to link to.




Use the email preview to confirm the coupon code displays correctly and the messaging matches your brand.

### Set Up a Reward Reminder Email (Optional)

If you want to remind participants about their reward, you can enable a reminder email.

  1. Under **Reward Delivery** , click **Reward Reminder Email**.

  2. Configure the send timing by updating the Reward Email Reminder Schedule variable.

  3. Customize the reminder email subject, copy, and creative as needed.




The reminder email will include the coupon code using the default configuration.
