---
title: "Reward Bank Redemption Experience"
excerpt: "Understand the user experience when implementing Extole's Reward Bank\n"
---


This guide walks through what your users will see and do when redeeming rewards inside the Extole Reward Bank. For more information on the [Reward Bank](https://docs.extole.com/docs/reward-bank) or [Reward Bank Configuration](https://docs.extole.com/docs/reward-bank-configuration-guide), check out dev.extole.com.

# **Overview**

The Reward Bank is a place where advocates can track and redeem multiple referral rewards in one place. The experience is designed to be simple and self-serve, with email notifications guiding them along the way.

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112720696/cee3d3d65cfc392da12bfe4e4b72/c9d0aadf-6c03-453c-a3e2-0e8bcad2f44c?expires=1778306400&signature=653f20b8a4374b646ce6d78f359391bf9665fde2a48a751bf7a2bed843cd8e79&req=diEmFM58nYdWX%2FMW3nq%2BgTF4eWC4wBx5zh51oo%2FBAGnsqscGQRvJUnQ77pfu%0A%2FdbUHPH5YDa7vKn0ub6mWGqo5Mo%3D%0A)

# **Redemption Flow Step-By-Step**

## **1. User Receives a Reward Email**

When a user earns a reward, they’ll receive an email notification letting them know a reward is available. In the Extole editor, this is the Advocate or Friend Reward Email within a given campaign and includes a link that sends participants to the Reward Bank experience.

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112720695/d8e23874820fabf327ab42f479c7/a1de26f7-1796-49d3-9bc5-a0318ed8a9a4?expires=1778306400&signature=64ec07dbd6dc22abc6e2d723ea24a362f6f291067aa03aaccfb1256592b61b92&req=diEmFM58nYdWXPMW3nq%2BgapBaDOGMQ1Z30z2uX%2BoPgCea%2F6H7XbdMNctrJTn%0AquvvP2gWAVQ776jtC4Z55%2Bqgo%2F0%3D%0A)

## **2. User Accesses the Reward Bank**

After clicking the link in the email, the user is brought to the Reward Bank Experience. By default, this is an Extole hosted microsite that pulls in that user's data when clicking from a Reward Email.

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112720697/c35a8020a23ab4039a7c607c3c27/49c5353e-cf3b-4072-9faa-bd89e225cdf0?expires=1778306400&signature=26fb96a010826d1bb23d9833c24d014d935ad52c05997fdb2b6160a25e6e6460&req=diEmFM58nYdWXvMW3nq%2BgSuaFCqFTkBB2FhljAF%2FmKM3wP5dK5s%2BSFnxJfsM%0AAdqx2r0Vyj7bp%2BBFA4oyg%2Baf0JY%3D%0A)

### **Optional Login Experience:**

If the Reward Bank is embedded within your logged in site, users are asked to sign in before accessing their rewards.

- If you’re interested in embedding the Reward Bank on your site, reach out to your Implementation Manager (IM) or Customer Success Manager (CSM).
- Note, if your user has the URL saved and doesn’t go through an email and there is no login, the Reward Bank will show up as empty.

## **3. User Views their Earned Rewards**

Inside the Reward Bank, users can see all rewards that have been earned, the date they were earned, and any past redeemed rewards. This gives them a clear history of their past reward activity.

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112720698/672f5fd808c1436f9e330666b006/6c4ac8fa-f730-4035-b24f-86d66984686a?expires=1778306400&signature=959f33132cf7d34840eb6bc21d3d93da0607fe59b2274787457b3323b95ff554&req=diEmFM58nYdWUfMW3nq%2BgdofrMAZB8VidXQGeeqplnHL2XsrOX%2Fpb2e91mlg%0AVzJVsKnvpR3dMoSlV4QIIalExa8%3D%0A)

## **4. User Selects Rewards to Redeem**

Users can choose to redeem all eligible rewards at once, or only redeem specific rewards. You can enable different limits in your Reward Bank configuration if users should only be able to redeem up to a certain amount, for example some gift card issuers only allow up to $1,000 per card. The user will then click Redeem.

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112720700/02c1bda5cce8596ecfd9a4356208/68bba3e0-c60c-42eb-82c2-57a6ed45d4f6?expires=1778306400&signature=a9e2d2d230f142a38eab922755f90be21a441322d6a82b058efd4dc2e5312706&req=diEmFM58nYZfWfMW3nq%2BgXzvWVNNTQ9IvoffZE9Crd%2FePs6GNR04rYtdKDwI%0AY8QMrfLBNyO5ewH5iPf55g31eFw%3D%0A)

## **5. Redeemed Rewards Appear in the “Redeemed” Section**

After redeeming, users will see a success notification and those rewards will appear in the **Redeemed** section.This helps users easily track what they’ve already claimed and what is still available to redeem in the future.

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112720699/65b07fd51ed8e3af68d2496fd8f8/66623f91-c2db-4701-9cd9-1c4f9c5c1e9b?expires=1778306400&signature=b4c8e681cc5c91f1df457aaa4f447fc8ef02850ced19937bbceaad981edcece2&req=diEmFM58nYdWUPMW3nq%2BgauDmePE4%2Ftf2EdSmIX8liGaFX8nkRKpzZN5LsyD%0Aq3bUVEStrzlq9rkqkkQPQc01lMI%3D%0A)

## **6. User Receives the Reward or Redemption Email**

Based on the type of reward, the user will receive an email with the details on how to access or use their reward. This would be the link to their electronic gift card, a coupon, etc. This email is configured within the [Reward Bank configuration section](https://docs.extole.com/docs/reward-bank-configuration-guide).

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112720701/e15c6d83c30209ae30a36396efef/829427e8-31b2-4a95-899a-d8e03a7a0b2e?expires=1778306400&signature=82f028d277854e0c30031a6687fc5555de336bb16c27fc182391acdb472673a5&req=diEmFM58nYZfWPMW3nq%2BgZp2kbq0d%2FbaUVTdUS2N7Fw9C5cMTPpZkrURwcPB%0Ad9T5Lk3hTsthxiDl%2Bn58NdhVfdw%3D%0A)

## **Need Help?**

If you’d like to adjust the Reward Bank experience or have questions about reward eligibility and redemption rules, contact your IM or CSM for support.
