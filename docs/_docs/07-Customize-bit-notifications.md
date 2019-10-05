---
name: Customize bit notifications
anchor: customize-bit-notifications
toc: 
 - name: Create special notifications for bit ranges
   anchor: create-special-notifications-for-bit-ranges
---
This section explains how to further customize notification for bits.

### Create special notifications for bit ranges
You can define separate notification for specific amount or range of bits.

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
    ]
```
**List of parameters**
* <span class="icon settings">Name</span> Name used for custom messages and pose mapping (Not shown on stream)
* <span class="icon settings">From</span> Minimum amount of bits
* <span class="icon settings">To</span> Maximum amount of bits

<br><span class="icon idea">Note: You do not have to create a custom message for CustomBits range. In that case, default bit message will be used.</span>
