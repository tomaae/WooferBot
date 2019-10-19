---
name: Customize subscription and bit notifications
anchor: customize-subscription-and-bit-notifications
toc: 
 - name: Create special notification ranges
   anchor: create-special-notification-notification
---
This section explains how to further customize notification for subscription and bits.

### Create special notification ranges
You can define separate notification for specific amount or ranges.

* <span class="icon settings">CustomBits</span> Array of bit notification ranges
* <span class="icon settings">CustomSubs</span> Array of subscription notification ranges

*Example:*
```
    "CustomBits": [
        {
            "Name": "bits100",
            "From": 100,
            "To": 999
        },
        {
            "Name": "bits1000",
            "From": 1000,
            "To": 1000
        }
    ],
    "CustomSubs": [
        {
            "Name": "sub12",
            "Tier": "",
            "From": 12,
            "To": 12
        }
    ]
```
**List of parameters**
* <span class="icon settings">Name</span> Name used for custom messages and pose mapping (Not shown on stream)
* <span class="icon settings">From</span> Minimum amount of bits
* <span class="icon settings">To</span> Maximum amount of bits
* <span class="icon settings">Tier</span> (Subscription only) Limit this notification to a subscription tier:
  * "" - All tiers
  * "prime" - Twitch Prime
  * "1" - Tier 1
  * "2" - Tier 2
  * "3" - Tier 3


<br><span class="icon idea">Note: You do not have to create a custom message for CustomBits/CustomSubs range. In that case, default bit message will be used.</span>
<br><span class="icon info">To add text messages to custom bit range, see <a class="icon doc" href="{{ site.github.url }}/documentation#customize-notifications-and-commands">Customize notifications and commands</a>.</span>
