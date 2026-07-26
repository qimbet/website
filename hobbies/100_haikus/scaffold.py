i, functionemport json

def generateScaffold(numEntries=101):
    defaultTheme = "default.css"
    defaultLines = [
        "", 
        "",
        ""
    ]


    entries = [
            {
                "id": i, 
                "lines": defaultLines,
                "theme": defaultTheme
            }
            for i in range(1, numEntries)
        ]

    with open("haikus.json", "w") as f: 
        json.dump(entries, f, indent=2)

        
if __name__=="__main__":
    generateScaffold()
