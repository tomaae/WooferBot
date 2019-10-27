---
name: Customize speech bubble
anchor: customize-speech-bubble
toc: 
 - name: Styles
   anchor: styles
---
This section explains how to customize color, shape and other properties for a speech bubble.

### Styles
You can use styles to customize a speech bubble.
```
    "Styles": {
        "BackgroundColor": "#fef7ed",
        "BorderColor": "#ffba70",
        "BorderWidth": 4,
        "BorderRadius": 4,
        "BorderStrokeColor": "#ffffff",
        "TextFontFamily": "Fira Sans",
        "TextSize": 22,
        "TextWeight": 900,
        "TextColor": "#ffba70",
        "HighlightTextSize": 24,
        "HighlightTextSpacing": 3,
        "HighlightTextColor": "#ffba70",
        "HighlightTextStrokeColor": "#b16a16",
        "HighlightTextShadowColor": "#ffba70",
        "HighlightTextShadowOffset": 3
    }
```
* <span class="icon settings">BorderRadius</span> Border edge roundness (specify 0 for sharp borders)
* <span class="icon settings">BorderStrokeColor</span> 1 pixel stroke around the border, recommended due to changing colors on stream (enter empty value "" to disable border stroke) 
* <span class="icon settings">TextWeight</span> Text boldness 100 - 900 (in increments by 100). Text "normal", "bold", "bolder" and "lighter" can also be used
* <span class="icon settings">HighlightTextSpacing</span> Specify 0 to disable text spacing
* <span class="icon settings">HighlightTextStrokeColor</span>, <span class="icon settings">HighlightTextShadowColor</span>, <span class="icon settings">HighlightTextShadowOffset</span> - all 3 parameters have to be specified. <span class="icon settings">HighlightTextShadowOffset</span> can be set to 0 to disable shadow.

<span class="icon idea">Note: All colors are defined with hashtag, followed by 6-digit hexidecimal number.
You can use web based <a class="icon website" href="https://www.w3schools.com/colors/colors_picker.asp" target="_blank">color picker</a> to choose or convert colors.</span>
<span class="icon idea">Note: Size, width, radius, spacing and offset are defined in pixels.</span>
