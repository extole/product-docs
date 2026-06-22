---
title: "Program Domain Setup"
slug: program-domain-setup
excerpt: "# Adding a Program Domain"
hidden: false
intercom_source_id: 10772065
---

# Adding a Program Domain

Program Domain set up provides a way for you to manage information about your website and program. This information is independent of any individual referral campaign you might be running.

To configure or look up your site's information, navigate to the **[Tech Center](https://my.extole.com/tech-center)** and use the pencil icon to edit your program domain or the + New Domain button to add one.

![Screenshot 2024-08-19 at 10.37.17 AM.png](https://extole-5ef307a0e5b1.intercom-attachments-7.com/i/o/syy27wia/1421733465/6c7e699bf3f79a4f5fe6e1603ecf/32630639450131?expires=1782259200&signature=7f6eb3f8350f0b62e9e88d07f038e35dc9fb097faa198ff32d9056fdf560313a&req=dSQlF859noVZXPMW3nq%2BgfAEdqOjpepy4ltlsn8sF%2BcAKoC316v9uIZzWNom%0AG8f0L0W5Zwu8nGSA%2B%2F1F4YtBdXI%3D%0A)
# Configuration Options

On the creation page, you will see the following configuration options.

![Screenshot 2024-08-22 at 1.27.17 PM.png](https://extole-5ef307a0e5b1.intercom-attachments-7.com/i/o/syy27wia/1421733468/7431f2f7d68d1660a16fda24b2ce/32631147379603?expires=1782259200&signature=404711d0948b0bba3ec45cd95ab4e1514cf4451a516d7323ce2b7ef5be5e3fbe&req=dSQlF859noVZUfMW3nq%2BgW4NejoXoNGf6xWXl2Ab%2BjkVfLDXJmOdgpIiVLN4%0A0tSDx3sHYxSOUiU1mnXr5yQ3T8w%3D%0A)

Configuration

Description

Program Domain Name

This is the name of your program. It can be whatever makes sense to you. Some ideas: US Refer a Friend, Production Refer a Friend, Staging Refer a Friend, etc.

Referral Domain

A Referral Domain is used in sharing URLs and the location where your landing pages are hosted (Promote Links). This URL will start out similar to "yourcompany.extole.io" but should be updated to your domain. The best practice is to use "refer.yourcompany.com" or "share.yourcompany.com". This process is referred to as branding a program URL and can be done using your Client Services Manager.

Production Sites Extole Should Support Requests From

Here you can add all production sites that Extole should be supporting requests from. This should include only your production domains as events coming from sites in this container will be counted in your program analytics. Note: by putting ".companyname.com" Extole will accept requests from all subdomains. This is important as we also use these sites to detect spam - if someone tries to send a share message with a domain not listed in this site field, Extole will not send the message to protect your users.

Testing Sites Extole Should Support Requests From

Here you can add all testing and staging sites that Extole should be supporting requests from, but events coming from these sites should not be counted in analytics. This should include all of your testing and staging domains. Note: by putting ".companyname.com" Extole will accept requests from all subdomains.

Automatically inject a program label onto this domain (toggle)

This allows you to specify a single Extole program for the domain.

Disable program domain and redirect traffic (toggle)

This is a way to forward all traffic. We do not allow you to delete program domains because there might be links in the wild with the domain you are trying to delete. Instead of deleting the domain, and causing those links to fail, we allow you to redirect them to a different program.
# Advanced Configuration

You can open the Advanced menu on the domain configuration screen to access SSL settings.![Screenshot 2024-08-22 at 1.27.30 PM.png](https://extole-5ef307a0e5b1.intercom-attachments-7.com/i/o/syy27wia/1421733469/4f84bd6c392eff762f21d79de10d/32631172463379?expires=1782259200&signature=e3eb23fdcffc1bf33f24c26fc30979790cca8cd62cfea7944d458732265a203f&req=dSQlF859noVZUPMW3nq%2BgVJ74X19UgZcn23RL3knZGx9ZQSerQsOr3MLQiyb%0ABJww28R5tr7ZZYD2n9vTiIhjY1E%3D%0A)

SSL Settings

Private Key

Extole will automatically generate a certificate for your domain using Let's Encrypt.

Public Certificate

Certificate Chain
