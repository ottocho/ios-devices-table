# iOS Devices Table

Data source: [https://www.theiphonewiki.com/wiki/Models](https://www.theiphonewiki.com/wiki/Models). Thanks a lot.

This script is written in 2016 to get the table map from [https://www.theiphonewiki.com/wiki/Models](https://www.theiphonewiki.com/wiki/Models) for data cleansing.

>iOS runs on various different models of devices. This page is used to give an overview of the different model numbers (or "M" numbers) used by devices. The model number of your device is located in the Settings app on the "General -> About" screen under "Model".

sample output: [output.json](output.json)

	{
        "iPhone": [
            {
                "Generation": "iPhone XS Max",
                "\"A\" Number": "[5]",
                "Bootrom": "Bootrom 3865.0.0.4.7",
                "FCC ID": "BCG-E3219A",
                "Internal Name": "D331pAP",
                "Identifier": "iPhone11,6",
                "Finish": "Space Gray",
                "Storage": "512 GB",
                "Model": "MT772"
            },
            ....
        ],
        "AirPods": [ ... ]
        ...


