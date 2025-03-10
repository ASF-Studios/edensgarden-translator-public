#Made by Alette (@ThisIsSomeone on GitHub)
#
#
#

#Settings

#True = Enable Unicode translations into \u format
#False = Disable
unicodeEnabled = False

import os
import csv
from pathlib import Path
from glob import glob

#Searches for a file in a directory
def find_file(name, path):
    filesGlob = []
    start_dir = path
    pattern = "*/" + name
    for dir,_,_ in os.walk(start_dir):
        filesGlob.extend(glob(os.path.join(dir,pattern), recursive=True))
    return filesGlob

def translateDialogue(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if " Text: " in translateThis[x] or "      " in translateThis[x]:
            #Skip the line if it includes a continuation
            if "      " in translateThis[x]:
                if skipLine == True:
                    continue
                else:
                    translated.write(translateThis[x])
                    continue

            skipLine = True #We have read text, so we can skip the next lines involving whitespaces

            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if " Text: " in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #If yes, search for the next x that has a similar symbol
            #Then if it contains no other symbols, delete that line, and if it does, leave it be
            #then go back to original x

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if True:
                #…
                #while "…" in temp:
                #    index = temp.index("…")
                #    temp[index] = "\\u2026"
                
                #...
                #while "..." in translating:
                #    correct = False
                #    #Ensures end of line periods are skipped
                #    while correct == False:
                #        index = temp.index(".")
                #        if temp[index+1] == ".":
                #            if temp[index+2] == ".":
                #                correct = True
                #            else:
                #                #Sets end-of-line period to a seperate character
                #                temp[index] = "&&"
                #        else:
                #            #Sets end-of-line period to a seperate character
                #            temp[index] = "&&"
                #    
                #    #Turn our correct elipses into the corresponding symbol
                #    temp[index] = "\\u2026"
                #    temp[index+1] = ""
                #    temp[index+2] = ""
                #
                #    #We have found our correct ellipses, now we fix the end of line dots
                #    while "&&" in temp:
                #        index = temp.index("&&")
                #        temp[index] = "."
                #    
                #    #We update our translating variable so that we may break out of the loop
                #    translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

                while "\"" in temp:
                    index = temp.index("\"")

                    #Matching set of ""
                    if temp.count("\"") > 1:
                        temp[index] = "\\u201C"
                        index = temp.index("\"")
                        temp[index] = "\\u201D"

                    #Only Starting "
                    if index == 0:
                        temp[index] = "\\u201C"

                    #Only Ending "
                    if index == temp.index(temp[-2]):
                        temp[index] = "\\u201D"

                    #If we come here, it means the " is in the middle
                    temp[index] = "\\u201D"

                while "\'" in temp:
                    index = temp.index("\'")

                    #We assume all remaining apostrophes are in the middle of a word
                    temp[index] = "\\u2019"


            #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file
            #TODO: Make the line break based on the length by adding \n and spaces
            translated.write("    Text: ")

            #Fix for apostrophes at the start of the line
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            if "VoiceSFX: " in translateThis[x]:
                skipLine = False
            translated.write(translateThis[x])

def translateNSD(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    isPathos = False
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if " Text: " in translateThis[x] or " text: " in translateThis[x] or "      " in translateThis[x] or " PanelText: " in translateThis[x]:
            isPanel = False
            if " PanelText: " in translateThis[x]:
                isPanel = True
            else:
                #Pathos text format is different
                if " text: " in translateThis[x]:
                    isPathos = True
            #Skip the line if it includes a continuation
            if "      " in translateThis[x]:
                if skipLine == True:
                    continue
                else:
                    translated.write(translateThis[x])
                    continue

            skipLine = True #We have read text, so we can skip the next lines involving whitespaces

            #Set the line to translate to
            translating = transing[counter]

            #Debug Messages for Pathos statements
            #print("--------------")
            #print("Line:     ",translating)
            #print("Loop:     ",counter)
            #print("isPathos: ",isPathos)
            #print("isPanel:  ",isPanel)
            
            if isPathos:
                counter = counter + 1

            #Checks if the translation has the same amount of spaces as the original.
            #If it does not, replace x spaces with >, where x is the difference in spaces
            testSpaces = -4 #Starts at minus 4 cause every "   Text: " standard has 4 spaces in it

            #However if it's a pathos statement, "    - text: " has more spaces, namely 6
            if isPathos:
                testSpaces = -6
            testAgainst = 0
            for letter in translateThis[x]:
                if letter == " ":
                    testSpaces = testSpaces + 1
            for letter in translating:
                if letter == " ":
                    testAgainst = testAgainst + 1
            #More spaces in the translated sentence
            if testSpaces < testAgainst:
                while testSpaces != testAgainst:
                    temp = list(translating)
                    index = temp.index(" ")
                    temp[index] = ">"
                    translating = ''.join(map(str,temp))
                    testAgainst = testAgainst - 1
            else:
                #Form a solution on if testSpaces > testAgainst, which is probably just adding spaces to the end
                if testSpaces > testAgainst:
                    while testSpaces != testAgainst:
                        print("testyy")
                        print(testSpaces)
                        print(testAgainst)
                        temp = list(translating)
                        temp.insert(0,"  ")
                        temp.insert(-2,"  ")
                        translating = ''.join(map(str, temp))
                        testAgainst = testAgainst + 1
            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Checks for setting flags
            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if " Text: " in translateThis[x] or " text: " in translateThis[x] or " PanelText: " in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"


            #>
            while ">" in temp:
                index = temp.index(">")
                temp[index] = " "

                        #while "\"" in temp:
            #        index = temp.index("\"")
            #
                    #Matching set of ""
            #        if temp.count("\"") > 1:
            #            temp[index] = "ʹʹ"
            #            index = temp.index("\"")
            #            temp[index] = "ʹʹ"
            #
            #        #Only Starting "
            #        if index == 0:
            #            temp[index] = "ʹʹ"
            #
                    #Only Ending "
            #        if index == temp.index(temp[-2]):
            #            temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
            #        temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"
            
            if unicodeEnabled:

                #@ | Delete all @
                while "@" in temp:
                    index = temp.index("@")
                    temp[index] = ""
                
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                    
                    #We update our translating variable so that we may break out of the loop
                    translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

            while "\"" in temp:
                index = temp.index("\"")

                #Matching set of ""
                if temp.count("\"") > 1:
                    temp[index] = "ʹʹ"
                    index = temp.index("\"")
                    temp[index] = "ʹʹ"

                #Only Starting "
                if index == 0:
                    temp[index] = "ʹʹ"

                #Only Ending "
                if index == temp.index(temp[-2]):
                    temp[index] = "ʹʹ"

                #If we come here, it means the " is in the middle
                temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file

            if not isPanel:
                if not isPathos:
                    translated.write("    Text: ")
                else:
                    translated.write("    - text: ")
                    isPathos = False
                    #This ensures that pathos statements can only last one line
                    #If pathos statements span multiple lines, thsi code needs to be adjusted
                    #Problem lies on 217 if statement relying on the amount of spaces which with pathos is always more
                    #So it skips a bunch of lines
                    #Manual check for the next line being size with an if and then making the rest an else if would work
                    skipLine = False
                #Increment counter when a line has been translated BUT ONLY WHEN WE TRANSLATE TEXT
            else:
                translated.write("    PanelText: ")
                counter = counter + 1

            #Fix for apostrophes at the start of the line
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

        else:
            if " VoiceSFX: " in translateThis[x]:
                skipLine = False
            if " PhraseGroup:" in translateThis[x]:
                skipLine = False
            if "      size:" in translateThis[x]:
                skipLine = False
            translated.write(translateThis[x])

#Translates truth bullets.
#Translation key always must be in the form of Title\nDescription
def translateTruthBullets(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if "  Description: " in translateThis[x] or "    " in translateThis[x] or "  Title: " in translateThis[x]:
            #Skip the line if it includes a continuation
            if "    " in translateThis[x]:
                continue

            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Checks for setting flags | Off because not relevant in truth bullets and causes issues, therefore commented out
            #Needs to check if they are actually at the start of a line
            #if "\'" in translateThis[x]:
            #    if translateThis[x].index()
            #    startsWithAp = True
            #if "\"" in translateThis[x]:
            #    startsWithDAp = True

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

                        #while "\"" in temp:
            #        index = temp.index("\"")
            #
                    #Matching set of ""
            #        if temp.count("\"") > 1:
            #            temp[index] = "ʹʹ"
            #            index = temp.index("\"")
            #            temp[index] = "ʹʹ"
            #
            #        #Only Starting "
            #        if index == 0:
            #            temp[index] = "ʹʹ"
            #
                    #Only Ending "
            #        if index == temp.index(temp[-2]):
            #            temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
            #        temp[index] = "ʹʹ"
                
            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if unicodeEnabled:
                #@
                while "@" in temp:
                    index = temp.index("@")
                    temp[index] = '<gradient=\"HitText\">'
                    index = temp.index("@")
                    temp[index] = '</gradient>'
                
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                
                #We update our translating variable so that we may break out of the loop
                translating = ''.join(map(str,temp))
            
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

            while "\"" in temp:
                index = temp.index("\"")

                #Matching set of ""
                if temp.count("\"") > 1:
                    temp[index] = "ʹʹ"
                    index = temp.index("\"")
                    temp[index] = "ʹʹ"

                #Only Starting "
                if index == 0:
                    temp[index] = "ʹʹ"

                #Only Ending "
                if index == temp.index(temp[-2]):
                    temp[index] = "ʹʹ"

                #If we come here, it means the " is in the middle
                temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            char_limit = 384 #Minimum character limits. Adjust for Truth Bullet.
            line_limit = 80 #Variable that can be adjusted based on line limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n    ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n    "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file
            #TODO: Make the line break based on the length by adding \n and spaces

            #Print the correct header depending on input
            if "  Description: " in translateThis[x]:
                translated.write("  Description: ")
            if "  Title: " in translateThis[x]:
                translated.write("  Title: ")

            #Fix for apostrophes at the start of the line
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            translated.write(translateThis[x])

def translateSettingsPrinter(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if "  m_text: " in translateThis[x] or "          m_StringArgument: " in translateThis[x]:
            #Skip the line if it includes a continuation
            isStringArg = False
            if not "          m_StringArgument: " in translateThis[x]:
                if "      " in translateThis[x]:
                    if skipLine == True:
                        continue
                    else:
                        translated.write(translateThis[x])
                        continue
            else:
                isStringArg = True

            skipLine = True #We have read text, so we can skip the next lines involving whitespaces

            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Checks for setting flags
            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if "  m_text: " in translateThis[x] or "          m_StringArgument: " in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

                        #while "\"" in temp:
            #        index = temp.index("\"")
            #
                    #Matching set of ""
            #        if temp.count("\"") > 1:
            #            temp[index] = "ʹʹ"
            #            index = temp.index("\"")
            #            temp[index] = "ʹʹ"
            #
            #        #Only Starting "
            #        if index == 0:
            #            temp[index] = "ʹʹ"
            #
                    #Only Ending "
            #        if index == temp.index(temp[-2]):
            #            temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
            #        temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if unicodeEnabled:
                #@
                #while "@" in temp:
                #    index = temp.index("@")
                #    temp[index] = '<gradient=\\"HitText\\">'
                #    index = temp.index("@")
                #    temp[index] = '</gradient>'
                
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                
                #We update our translating variable so that we may break out of the loop
                translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

                while "\"" in temp:
                    index = temp.index("\"")

                    #Matching set of ""
                    if temp.count("\"") > 1:
                        temp[index] = "ʹʹ"
                        index = temp.index("\"")
                        temp[index] = "ʹʹ"

                    #Only Starting "
                    if index == 0:
                        temp[index] = "ʹʹ"

                    #Only Ending "
                    if index == temp.index(temp[-2]):
                        temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
                    temp[index] = "ʹ"

                while "\'" in temp:
                    index = temp.index("\'")

                    #We assume all remaining apostrophes are in the middle of a word
                    temp[index] = "ʹ"

            #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file
            #TODO: Make the line break based on the length by adding \n and spaces
            postthis = str(translateThis[x])
            if isStringArg == False:
                #translated.write("  m_text: ")
                postthis = postthis.replace("  m_text: ","")
            else:
                postthis = postthis.replace("          m_StringArgument: ","")
                #translated.write("          m_StringArgument: ")

            #Fix for apostrophes at the start of the line
            #if startsWithAp == True:
            #    translated.write("\'")
            #if startsWithDAp == True:
            #    translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(postthis)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            if "m_isRightToLeft:" in translateThis[x]:
                skipLine = False
            if "m_BoolArgument:" in translateThis[x]:
                skipLine = False

def translateSettings(toTranslate, transKey, translated): 
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if "  m_text: " in translateThis[x] or "          m_StringArgument: " in translateThis[x]:
            #Skip the line if it includes a continuation
            isStringArg = False
            if not "          m_StringArgument: " in translateThis[x]:
                if "      " in translateThis[x]:
                    if skipLine == True:
                        continue
                    else:
                        translated.write(translateThis[x])
                        continue
            else:
                isStringArg = True

            skipLine = True #We have read text, so we can skip the next lines involving whitespaces

            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Checks for setting flags
            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if "  m_text: " in translateThis[x] or "          m_StringArgument: " in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

                        #while "\"" in temp:
            #        index = temp.index("\"")
            #
                    #Matching set of ""
            #        if temp.count("\"") > 1:
            #            temp[index] = "ʹʹ"
            #            index = temp.index("\"")
            #            temp[index] = "ʹʹ"
            #
            #        #Only Starting "
            #        if index == 0:
            #            temp[index] = "ʹʹ"
            #
                    #Only Ending "
            #        if index == temp.index(temp[-2]):
            #            temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
            #        temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if unicodeEnabled:
                #@
                #while "@" in temp:
                #    index = temp.index("@")
                #    temp[index] = '<gradient=\\"HitText\\">'
                #    index = temp.index("@")
                #    temp[index] = '</gradient>'
                
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                
                #We update our translating variable so that we may break out of the loop
                translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

                while "\"" in temp:
                    index = temp.index("\"")

                    #Matching set of ""
                    if temp.count("\"") > 1:
                        temp[index] = "ʹʹ"
                        index = temp.index("\"")
                        temp[index] = "ʹʹ"

                    #Only Starting "
                    if index == 0:
                        temp[index] = "ʹʹ"

                    #Only Ending "
                    if index == temp.index(temp[-2]):
                        temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
                    temp[index] = "ʹ"

                while "\'" in temp:
                    index = temp.index("\'")

                    #We assume all remaining apostrophes are in the middle of a word
                    temp[index] = "ʹ"

            #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file
            #TODO: Make the line break based on the length by adding \n and spaces
            if isStringArg == False:
                translated.write("  m_text: ")
            else:
                translated.write("          m_StringArgument: ")

            #Fix for apostrophes at the start of the line
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            if "m_isRightToLeft:" in translateThis[x]:
                skipLine = False
            if "m_BoolArgument:" in translateThis[x]:
                skipLine = False
            translated.write(translateThis[x])

def translateSpot(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if "  question:" in translateThis[x] or "      " in translateThis[x]:
            #Skip the line if it includes a continuation
            if "      " in translateThis[x]:
                if skipLine == True:
                    continue
                else:
                    translated.write(translateThis[x])
                    continue

            skipLine = True #We have read text, so we can skip the next lines involving whitespaces

            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Checks for setting flags
            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if "  question:" in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

            #while "\"" in temp:
            #        index = temp.index("\"")
            #
                    #Matching set of ""
            #        if temp.count("\"") > 1:
            #            temp[index] = "ʹʹ"
            #            index = temp.index("\"")
            #            temp[index] = "ʹʹ"
            #
            #        #Only Starting "
            #        if index == 0:
            #            temp[index] = "ʹʹ"
            #
                    #Only Ending "
            #        if index == temp.index(temp[-2]):
            #            temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
            #        temp[index] = "ʹʹ"
            
            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if unicodeEnabled:
                #@
                #while "@" in temp:
                #    index = temp.index("@")
                #    temp[index] = '<gradient=\\"HitText\\">'
                #    index = temp.index("@")
                #    temp[index] = '</gradient>'
                
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                    
                    #We update our translating variable so that we may break out of the loop
                    translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

            while "\"" in temp:
                index = temp.index("\"")

                #Matching set of ""
                if temp.count("\"") > 1:
                    temp[index] = "ʹʹ"
                    index = temp.index("\"")
                    temp[index] = "ʹʹ"

                #Only Starting "
                if index == 0:
                    temp[index] = "ʹʹ"

                #Only Ending "
                if index == temp.index(temp[-2]):
                    temp[index] = "ʹʹ"

                #If we come here, it means the " is in the middle
                temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"


                #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file
            #TODO: Make the line break based on the length by adding \n and spaces
            translated.write("    text: ")

            #Fix for apostrophes at the start of the line
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            if "damageOnWrong:" in translateThis[x]:
                skipLine = False
            translated.write(translateThis[x])

def translateCA(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if "      questionText: " in translateThis[x] or "      flavourText: " in translateThis[x]:
            
            isQuestion = False
            isFlavour = False
            #Set bools based on which type of text
            if "      questionText: " in translateThis[x]:
                isQuestion = True
            else:
                isFlavour = True

            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Checks for setting flags
            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if " Text: " in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

                        #while "\"" in temp:
            #        index = temp.index("\"")
            #
                    #Matching set of ""
            #        if temp.count("\"") > 1:
            #            temp[index] = "ʹʹ"
            #            index = temp.index("\"")
            #            temp[index] = "ʹʹ"
            #
            #        #Only Starting "
            #        if index == 0:
            #            temp[index] = "ʹʹ"
            #
                    #Only Ending "
            #        if index == temp.index(temp[-2]):
            #            temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
            #        temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if unicodeEnabled:
                #@
                #while "@" in temp:
                #    index = temp.index("@")
                #    temp[index] = '<gradient=\\"HitText\\">'
                #    index = temp.index("@")
                #    temp[index] = '</gradient>'
                
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                    
                    #We update our translating variable so that we may break out of the loop
                    translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

            while "\"" in temp:
                index = temp.index("\"")

                #Matching set of ""
                if temp.count("\"") > 1:
                    temp[index] = "ʹʹ"
                    index = temp.index("\"")
                    temp[index] = "ʹʹ"

                #Only Starting "
                if index == 0:
                    temp[index] = "ʹʹ"

                #Only Ending "
                if index == temp.index(temp[-2]):
                    temp[index] = "ʹʹ"

                #If we come here, it means the " is in the middle
                temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"


                #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file
            #TODO: Make the line break based on the length by adding \n and spaces
            if isQuestion:
                translated.write("      questionText: ")
            else:
                translated.write("      flavourText: ")

    #Fix for apostrophes at the start of the line		
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            if "noOfLocks:" in translateThis[x]:
                skipLine = False
            translated.write(translateThis[x])

def translateMC(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if "  - text: " in translateThis[x] or "  question: " in translateThis[x]:
            
            isQuestion = False
            #Set bools based on which type of text
            if "  question: " in translateThis[x]:
                isQuestion = True

            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Checks for setting flags
            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if "  - text: " in translateThis[x] or "  question: " in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

                        #while "\"" in temp:
            #        index = temp.index("\"")
            #
                    #Matching set of ""
            #        if temp.count("\"") > 1:
            #            temp[index] = "ʹʹ"
            #            index = temp.index("\"")
            #            temp[index] = "ʹʹ"
            #
            #        #Only Starting "
            #        if index == 0:
            #            temp[index] = "ʹʹ"
            #
                    #Only Ending "
            #        if index == temp.index(temp[-2]):
            #            temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
            #        temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if unicodeEnabled:
                #@
                #while "@" in temp:
                #    index = temp.index("@")
                #    temp[index] = '<gradient=\\"HitText\\">'
                #    index = temp.index("@")
                #    temp[index] = '</gradient>'
                
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                    
                    #We update our translating variable so that we may break out of the loop
                    translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

            while "\"" in temp:
                index = temp.index("\"")

                #Matching set of ""
                if temp.count("\"") > 1:
                    temp[index] = "ʹʹ"
                    index = temp.index("\"")
                    temp[index] = "ʹʹ"

                #Only Starting "
                if index == 0:
                    temp[index] = "ʹʹ"

                #Only Ending "
                if index == temp.index(temp[-2]):
                    temp[index] = "ʹʹ"

                #If we come here, it means the " is in the middle
                temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"


                #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file
            #TODO: Make the line break based on the length by adding \n and spaces
            if isQuestion:
                translated.write("  question: ")
            else:
                translated.write("  - text: ")

    #Fix for apostrophes at the start of the line		
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            if "noOfLocks:" in translateThis[x]:
                skipLine = False
            translated.write(translateThis[x])

def translateGYMSOverworld(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if " displayName: " in translateThis[x] or "      " in translateThis[x]:
            #Skip the line if it includes a continuation
            if "      " in translateThis[x]:
                if skipLine == True:
                    continue
                else:
                    translated.write(translateThis[x])
                    continue

            skipLine = True #We have read text, so we can skip the next lines involving whitespaces

            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Checks for setting flags
            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if "  displayName: " in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

            #while "\"" in temp:
            #        index = temp.index("\"")
            #
                    #Matching set of ""
            #        if temp.count("\"") > 1:
            #            temp[index] = "ʹʹ"
            #            index = temp.index("\"")
            #            temp[index] = "ʹʹ"
            #
            #        #Only Starting "
            #        if index == 0:
            #            temp[index] = "ʹʹ"
            #
                    #Only Ending "
            #        if index == temp.index(temp[-2]):
            #            temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
            #        temp[index] = "ʹʹ"
            
            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if unicodeEnabled:
                #@
                #while "@" in temp:
                #    index = temp.index("@")
                #    temp[index] = '<gradient=\\"HitText\\">'
                #    index = temp.index("@")
                #    temp[index] = '</gradient>'
                
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                    
                    #We update our translating variable so that we may break out of the loop
                    translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

            while "\"" in temp:
                index = temp.index("\"")

                #Matching set of ""
                if temp.count("\"") > 1:
                    temp[index] = "ʹʹ"
                    index = temp.index("\"")
                    temp[index] = "ʹʹ"

                #Only Starting "
                if index == 0:
                    temp[index] = "ʹʹ"

                #Only Ending "
                if index == temp.index(temp[-2]):
                    temp[index] = "ʹʹ"

                #If we come here, it means the " is in the middle
                temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"


                #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file

            #count how many spaces at the start in translateThis[x] and print those
            ora = str(translateThis[x])
            spacy = len(ora) - len(ora.lstrip())
            #Print z amount of spaces
            #TODO: Check if this is correct
            for z in range(0,spacy):
                translated.write(" ")
            translated.write("displayName: ")

            #Fix for apostrophes at the start of the line
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            if "  box:" in translateThis[x] or "    options:" in translateThis[x]:
                skipLine = False
            translated.write(translateThis[x])

def translateControls(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if "    Description: " in translateThis[x] or "      " in translateThis[x]:
            #Skip the line if it includes a continuation
            if "      " in translateThis[x]:
                if skipLine == True:
                    continue
                else:
                    translated.write(translateThis[x])
                    continue

            skipLine = True #We have read text, so we can skip the next lines involving whitespaces

            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Checks for setting flags
            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if "    Description: " in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

            #while "\"" in temp:
            #        index = temp.index("\"")
            #
                    #Matching set of ""
            #        if temp.count("\"") > 1:
            #            temp[index] = "ʹʹ"
            #            index = temp.index("\"")
            #            temp[index] = "ʹʹ"
            #
            #        #Only Starting "
            #        if index == 0:
            #            temp[index] = "ʹʹ"
            #
                    #Only Ending "
            #        if index == temp.index(temp[-2]):
            #            temp[index] = "ʹʹ"

                    #If we come here, it means the " is in the middle
            #        temp[index] = "ʹʹ"
            
            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if unicodeEnabled:
                #@
                #while "@" in temp:
                #    index = temp.index("@")
                #    temp[index] = '<gradient=\\"HitText\\">'
                #    index = temp.index("@")
                #    temp[index] = '</gradient>'
                
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                    
                    #We update our translating variable so that we may break out of the loop
                    translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

            while "\"" in temp:
                index = temp.index("\"")

                #Matching set of ""
                if temp.count("\"") > 1:
                    temp[index] = "ʹʹ"
                    index = temp.index("\"")
                    temp[index] = "ʹʹ"

                #Only Starting "
                if index == 0:
                    temp[index] = "ʹʹ"

                #Only Ending "
                if index == temp.index(temp[-2]):
                    temp[index] = "ʹʹ"

                #If we come here, it means the " is in the middle
                temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"


                #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file
            #TODO: Make the line break based on the length by adding \n and spaces
            translated.write("    Description: ")

            #Fix for apostrophes at the start of the line
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            if "  - Left: " in translateThis[x]:
                skipLine = False
            translated.write(translateThis[x])

def translateLeaveAsk(toTranslate, transKey, translated):
    transing = transKey.readlines()
    translateThis = toTranslate.readlines()
    counter = 0
    skipLine = False #Checks if the line is actually to be skipped
    for x in range(0, len(translateThis)):
        #If we encounter a dialogue line
        if " Text: " in translateThis[x] or "      " in translateThis[x] or "  - ChoiceText: " in translateThis[x]:
            #Skip the line if it includes a continuation
            if "      " in translateThis[x]:
                if skipLine == True:
                    continue
                else:
                    translated.write(translateThis[x])
                    continue
            
            choiceText = False
            if "  - ChoiceText: " in translateThis[x]:
                choiceText = True

            skipLine = True #We have read text, so we can skip the next lines involving whitespaces
            #Set the line to translate to
            translating = transing[counter]

            #Flags for making the line formatted similar to the original text
            startsWithAp = False
            startsWithDAp = False

            #Becomes True when there already is a ' in place, meaning that we do not need to add it to the end of a line
            apAlreadyFound = False
            #Checks for setting flags
            tempor = list(translateThis[x])
            if "\'" in translateThis[x] and tempor[10] == "\'":
                startsWithAp = True

                #Save Current X
                currX = x
                #Find a matching '
                isFound = False
                #If the line itself already contains a matching pair
                #Has to be -2 cause the last character will always be a newline
                if tempor[-2] == "\'":
                    isFound = True
                #Makes sure it's text dialogue
                if " Text: " in translateThis[x] or "  - ChoiceText: " in translateThis[x]:
                    while isFound == False:
                        x = x + 1
                        if "\'" in translateThis[x]:
                            tempo = list(translateThis[x])
                            if tempo[-2] == "\'":
                                isFound = True
                            else:
                                #Else we have not found the true end of line, instead just an early apostrophe
                                continue
                            #We determine whether this matching ' is part of a line or is a seperate new line
                            if translateThis[x] == "\'\n":
                                #We 'delete' the line
                                apAlreadyFound = True
                                print("How often come here?")
                            else:
                                pass
                                #In the case there is a ' at the end of a normal line, there might still be a ' before VoiceSFX
                                #We therefore check until we find VoiceSFX

                            x = currX
            if "\"" in translateThis[x] and tempor[10] == "\"":
                startsWithDAp = True

            #If yes, search for the next x that has a similar symbol
            #Then if it contains no other symbols, delete that line, and if it does, leave it be
            #then go back to original x

            #While the dialogue line continues on the next line, skip over it

            #Turn Translating into a list temporarily
            temp = list(translating)
            #TODO: Set parameters such as ", \u2014, u\2019 using flags and edit translating based on those"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"

            if unicodeEnabled:
                #…
                while "…" in temp:
                    index = temp.index("…")
                    temp[index] = "\\u2026"
                
                #...
                while "..." in translating:
                    correct = False
                    #Ensures end of line periods are skipped
                    while correct == False:
                        index = temp.index(".")
                        if temp[index+1] == ".":
                            if temp[index+2] == ".":
                                correct = True
                            else:
                                #Sets end-of-line period to a seperate character
                                temp[index] = "&&"
                        else:
                            #Sets end-of-line period to a seperate character
                            temp[index] = "&&"
                    
                    #Turn our correct elipses into the corresponding symbol
                    temp[index] = "\\u2026"
                    temp[index+1] = ""
                    temp[index+2] = ""

                    #We have found our correct ellipses, now we fix the end of line dots
                    while "&&" in temp:
                        index = temp.index("&&")
                        temp[index] = "."
                    
                    #We update our translating variable so that we may break out of the loop
                    translating = ''.join(map(str,temp))
                
                #-
                #while "-" in temp:
                #    index = temp.index("-")
                #    temp[index] = "\\u2014"
                
                #—
                #while "—" in temp:
                #    index = temp.index("—")
                #    temp[index] = "\\u2014"

            while "\"" in temp:
                index = temp.index("\"")

                #Matching set of ""
                if temp.count("\"") > 1:
                    temp[index] = "ʹʹ"
                    index = temp.index("\"")
                    temp[index] = "ʹʹ"

                #Only Starting "
                if index == 0:
                    temp[index] = "ʹʹ"

                #Only Ending "
                if index == temp.index(temp[-2]):
                    temp[index] = "ʹʹ"

                #If we come here, it means the " is in the middle
                temp[index] = "ʹʹ"

            while "\'" in temp:
                index = temp.index("\'")

                #We assume all remaining apostrophes are in the middle of a word
                temp[index] = "ʹ"


            #TODO:Check how many characters you have and sets isCG bool
            
            #Fix for apostrophes at the end of the line
            if startsWithAp == True:
                if apAlreadyFound == False:
                    temp.insert(-1, "\'")
            if startsWithDAp == True:
                temp.insert(-1, "\"")
            
            #Update our variable so we may check character count properly
            translating = ''.join(map(str,temp))
            temp = list(translating)
            
            #TODO: Check how long the line is. If too long, print an error.
            #Otherwise, add necessary spacing into it.
            isCG = False #Variable that gets set based on whether the original line is CG
            char_limit = 256 #Minimum character limits. Gets updated to 384 if CG.
            line_limit = 80 #Variable that can be adjusted based on line limit
            
            #TODO: Check if the line is CG and if so set isCG and char_limit

            #Check if we go over the limit, if so, print an error
            if len(translating) > char_limit:
                print("WARNING: Character limit has been crossed on line ", counter+1, ". This might cause issues.")

            #If a line is too long, we divide it over multiple lines
            curr_length = len(temp)
            helper = line_limit
            while curr_length > line_limit:

                #Find last space in current segment
                while temp[helper] != " ":
                    helper = helper - 1
                    #If helper reaches the start of the segment
                    if helper == 0 or temp[helper] == "\n      ":
                        raise ValueError("No breakable line points found in line", counter+1)
                
                #Space has been found, break at space
                temp[helper] = "\n      "

                #Update segment
                curr_length = len(temp) - helper
                helper = helper + line_limit

            #Rejoin your list and put the sentence back together
            translating = ''.join(map(str,temp))

            #Places the line in the translated file
            #TODO: Make the line break based on the length by adding \n and spaces
            if not choiceText:
                translated.write("    Text: ")
            else:
                translated.write("  - ChoiceText: ")

            #Fix for apostrophes at the start of the line
            if startsWithAp == True:
                translated.write("\'")
            if startsWithDAp == True:
                translated.write("\"")
            
            #Print the Translated line into the file
            translated.write(translating)

            #Increment counter when a line has been translated
            counter = counter + 1
        else:
            if "VoiceSFX: " in translateThis[x] or "  - ChoiceText: " in translateThis[x]:
                skipLine = False
            translated.write(translateThis[x])

def translateAll(mode):
            cwd = os.getcwd()
            print("Warning! This mode requires you to have two folders in the same directory as you are running this file. \n One of these must be your custom named folder (preferably solely) containing files to translate, and the other must be a folder containing your translation keys.")
            print("Translation keys do not need to be in the same folder structure as the original, however, must have matching file names but with the file extension .translate. \n It is also required for each .translate file to be in a subdirectory, and not the main directory that is inputted for this command.")
            print("To convert csv documents into .translate format, please utilize the convert setting.")
            original = input("Input translation folder: ")
            trans = input("Input your translation keys folder: ")

            path = cwd + "/" + original
            if not os.path.exists(path):
                print("No Translation folder was found.")
                return
            pathKey = cwd + "/" + trans
            if not os.path.exists(pathKey):
                print("No Keys folder was found.")
                return
            
            #For each file we need to translate, we try to find our matching key.
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    creationPath = cwd + "/Translated/" + mode
                    no_ext = Path(file).resolve().stem #Grab the file name without extension
                    isUnity = False
                    #Search the key directory for a matching file
                    key_name = no_ext + ".translate"
                    orig_name = no_ext + ".asset"
                    findKey = find_file(key_name, pathKey)
                    if not findKey == []:
                        #If the translation key has been found, we grab the file path to the original and get to work
                        findOrig = find_file(orig_name, path)
                        if findOrig == []:
                            #It's a possibility the original file is either not a correct file, or a .unity file
                            #So we check for an unity file first
                            orig_name = no_ext + ".unity"
                            isUnity = True
                            findOrig = find_file(orig_name, path)
                            if findOrig == []:
                                #Possibility prefab file so we check here
                                orig_name = no_ext + ".prefab"
                                #isUnity is still set to true so it will be read as settings file
                                findOrig = find_file(orig_name, path)

                                if findOrig == []:
                                    #Not a parseable file
                                    print("Original file not .unity, .prefab or .asset file")
                                    break
                        try:
                            toTranslate = open(findOrig[0], "r")
                            transKey = open(findKey[0], "r")

                            #original contains given directory name
                            #findOrig[0] contains file path, so if you grab everything after the variable original you get the path you need
                            res = findOrig[0].split(original, 1)
                            splitString = res[1]
                            print(splitString)
                            helpy = os.path.basename(toTranslate.name)
                            splitString = splitString.replace(helpy, "")
                            print(splitString)
                            helpy = creationPath + splitString
                            os.makedirs(helpy, exist_ok=True)
                            creationPath = creationPath + splitString + os.path.basename(toTranslate.name) 
                            #TODO: Adust it so that the files are each printed in the same folder structure as they were before

                            translated = open(creationPath, "w") #Overwrites the file if it already exists
                        except OSError and TypeError as e:
                            print(e) #TODO: Remove
                            print("orig_name", orig_name)
                            print("findOrig: ", findOrig)
                            print("Findkey: ", findKey)
                            print("CreationPath: ", creationPath)
                            print("File not found.")
                            mode = ""
                            break
                        
                        #Translate the file based on the correct mode
                        translateThis = toTranslate.readlines()
                        toTranslate.close()
                        try:
                            toTranslate = open(findOrig[0], "r")
                        except OSError and TypeError as e:
                            print("If this ever prints, pigs can fly.")
                        isIn = False
                        isPhraseIn = False
                        isDifficultyIn = False
                        isSpotIn = False
                        isChoicesIn = False
                        isBulletsIn = False
                        isDescIn = False
                        isCapitalChoicesIn = False
                        for x in range(0, len(translateThis)):
                            if "  - translationKey: " in translateThis[x]:
                                isIn = True
                            if "PhraseText: " in translateThis[x]:
                                isPhraseIn = True
                            if "- difficulty:" in translateThis[x]:
                                isDifficultyIn = True
                            if "- spotName:" in translateThis[x]:
                                isSpotIn = True
                            if "  choices:" in translateThis[x]:
                                isChoicesIn = True
                            if "  - bulletOption: " in translateThis[x]:
                                isBulletsIn = True
                            if "    Description: " in translateThis[x]:
                                isDescIn = True
                            if "  - ChoiceText: " in translateThis[x]:
                                isCapitalChoicesIn = True
                        if isUnity:
                            #We use settings translation
                            #translateSettingsPrinter(toTranslate, transKey, translated)
                            translateSettings(toTranslate, transKey, translated)
                        else:
                            if isIn == True:
                                if isPhraseIn == True:
                                    #It is a NSD or Rebuttal Showdown
                                    translateNSD(toTranslate, transKey, translated)
                                else:
                                    if isCapitalChoicesIn:
                                        #It's LeaveAsk
                                        translateLeaveAsk(toTranslate, transKey, translated)
                                    else:
                                        #It has to be Dialogue
                                        translateDialogue(toTranslate, transKey, translated)
                            else:
                                if isDifficultyIn == True:
                                    if isSpotIn:
                                        translateSpot(toTranslate, transKey, translated)
                                    else:
                                        if isChoicesIn:
                                            translateMC(toTranslate,transKey,translated)
                                        else:
                                            if isBulletsIn:
                                                translateMC(toTranslate, transKey, translated)
                                            else:
                                                translateCA(toTranslate, transKey, translated)
                                else:
                                    if isDescIn:
                                        #Controls File
                                        translateControls(toTranslate, transKey, translated) 
                                    else:
                                        #This is a Truth Bullet file'
                                        translateTruthBullets(toTranslate, transKey, translated)
                            

                        #Close the files
                        if mode != "":
                            toTranslate.close()
                            transKey.close()
                            translated.close()
                        
                        print(no_ext, "has been fully translated.")
                    else:
                        print("Translation Key", no_ext, ".translate"," for ", no_ext,".asset was not found.")


def main():
    #Store Current Working Directory
    cwd = os.getcwd()

    #Check if the Translated folder exists, if not, create it
    path = cwd + "/" + "Translated"
    if not os.path.exists(path):
        os.makedirs("Translated")

    #Check if the Dialogue subfolder exists, if not, create it
    path = cwd + "/Translated/Dialogue"
    if not os.path.exists(path):
        os.makedirs("Translated/Dialogue")

    #Check if the NSD subfolder exists, if not, create it
    path = cwd + "/Translated/NSD"
    if not os.path.exists(path):
        os.makedirs("Translated/NSD")

    #Check if the TruthBullets subfolder exists, if not, create it
    path = cwd + "/Translated/TruthBullets"
    if not os.path.exists(path):
        os.mkdir("Translated/TruthBullets")

    #Check if the settings subfolder exists, if not, create it
    path = cwd + "/Translated/Settings"
    if not os.path.exists(path):
        os.mkdir("Translated/Settings")

    #Check if the display subfolder exists, if not, create it
    path = cwd + "/Translated/Display"
    if not os.path.exists(path):
        os.mkdir("Translated/Display")

    #Check if the settings subfolder exists, if not, create it
    path = cwd + "/Translated/All"
    if not os.path.exists(path):
        os.mkdir("Translated/All")

    #Ask for Translation mode setting. Offers exit as option as well.
    mode = ""
    while mode != "exit":
        mode = input("Please input desired translation mode. Choose between:\n 'NSD' | 'Dialogue' | 'TruthBullets' | 'Settings' | 'Display' | 'All' | 'Exit' | 'Convert'\n")

        #Make mode uniform
        match mode:
            case "Dialogue" | "dialogue":
                mode = "Dialogue"
            case "TruthBullets" | "tb" | "truthbullets":
                mode = "TruthBullets"
            case "NSD" | "nsd":
                mode = "NSD"
            case "Settings" | "settings":
                mode = "Settings"
            case "All" | "all":
                mode = "All"
            case "Exit" | "exit":
                mode = "Exit"
            case "Convert" | "convert":
                mode = "Convert"
            case "Display" | "display":
                mode = "Display"
            case _:
                continue
        
        creationPath = cwd + "/Translated/" + mode + "/"

        #Mode: Exit
        if mode == 'exit' or mode == 'Exit':
            return
        
        #Mode: All | Translates all files in designated folder with keys in another designated folder
        if mode == 'All' or mode == 'all':
            translateAll(mode)
            break

        if mode == 'Convert':
            print("Note that the given directory must contain all files to be converted directly. None of these files may be in a subdirectory.")
            #TODO: Improve on that
            original = input("Input folder with files to be converted: ")

            path = cwd + "/" + original
            if not os.path.exists(path):
                print("No Convert folder was found.")
                return
            
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    path = cwd + "/" + original
                    checker = os.path.splitext(file)
                    #If the file is a csv file
                    if checker[1] == '.csv':
                        #Try to open it
                        try:
                            fileurl = path + "/" + file
                            with open(fileurl, newline='') as csvfile:
                                data = list(csv.reader(csvfile))
                        except ValueError:
                            print(file, "is not a valid csv file.")
                            return
                        filelength = len(data)
                        for x in range(0, filelength):
                            if "File:" in data[x][2]:
                                #We have found a line that indicates we must create a new file. The new file name is stored in data[x][3]

                                #We make the correct directory
                                path = cwd + "/" + original + "/Keys"
                                if not os.path.exists(path):
                                    os.makedirs(original + "/Keys")
                                path = path + "/" + data[x][3] + ".translate"
                                #We attempt to make the file
                                try:
                                    conversion = open(path, "w")
                                except OSError and TypeError as e:
                                    print(e) #TODO: Remove
                                    print(path)
                                    print("File not found.")
                                    mode = ""
                                    break
                                
                                #Move our cursor past the line from which we just read
                                x = x + 1
                                #Now, we actually put the lines of the project in
                                while x < filelength and not "File:" in data[x][2]:
                                    #Added DONOTINCLUDE functionality | If the first column contains DONOTINCLUDE, the line will not be copied
                                    if not "DONOTINCLUDE" in data[x][0]:
                                        #While we are still reading in the file and we don't need to create a new file
                                        
                                        #TODO: Add a remover of the first "" in  front and behind the line if a , is found in the line.
                                        conversion.write(data[x][4])
                                        #if x != filelength-1:
                                        #    if not "File:" in data[x+1][2]:
                                        conversion.write("\n")
                                    x = x + 1

                                #We close the .translate file
                                conversion.close()
            break

        temp = input("Please input the file to be translated: ")
        transKeyPath = input("Please input the file to translate from here: ")
        toTranslatePath = cwd + "/" + temp
        transKeyPath = cwd + "/" + transKeyPath

        #We attempt to open the input files
        try:
            toTranslate = open(toTranslatePath, "r")
            transKey = open(transKeyPath, "r")
            creationPath = creationPath + os.path.basename(toTranslate.name)
            translated = open(creationPath, "w") #Overwrites the file if it already exists
        except OSError as e:
            print(e) #TODO: Remove
            print("File not found.")
            mode = ""

        #Execute Translation Mode
        match mode:
            case "display" | "Display":
                translateGYMSOverworld(toTranslate, transKey, translated)
            case "Dialogue" | "dialogue":
                translateDialogue(toTranslate, transKey, translated)
            case "TruthBullets" | "tb" | "truthbullets":
                translateTruthBullets(toTranslate, transKey, translated)
            case "NSD" | "nsd":
                translateNSD(toTranslate, transKey, translated)
            case "Settings" | "settings":
                translateSettings(toTranslate, transKey, translated)
            case _:
                print("Did not understand input.")


        #We close the files only if they have been opened
        if mode != "":
            toTranslate.close()
            transKey.close()
            translated.close()


if __name__ == "__main__":
    main()

    