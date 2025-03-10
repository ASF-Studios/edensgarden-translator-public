<!-- 
README.md       
Made on 06/06/2024         
Contributed by ThisIsSomeone
Last edited on 10/03/2024 by ThisIsSomeone

Contains the README of the Eden's Garden Translator Project
-->

# Eden's Garden Translator ✨

<img src="Images/Banner.jpg" width="900"/>

Eden's Garden Translator is a project to enable translation of Project Eden's Garden through providing a way to automatically adjust the serialised game files with the user-provided translated dialogue.
The tool also provides a way to automically convert the official dialogue sheet to files which this program can use to adjust the serialised files. Information on how to use the tool as well as how to set up the dialogue sheet document are described below.

### Important Sidenote

This repository is a public version made available for open-source contributions to the code. Certain files, such as the unity asset files, have been removed. 

# Contents
- [Getting started](#getting-started)
    - [Providing Your Translation](#providing-your-translation)
    - [Creating Translation Files](#creating-translation-files)
    - [Translating Singular Files](#translating-singular-files)
    - [Translating All Files](#translating-all-files)
- [Developers](#developers)
- [Contributing Standards](#coding-and-testing-standards)
- [License](#license)

## Getting Started 

We provide a basic guideline on how to use the translation tool. We assume that Python version 3.10 or higher has been installed already. In the case that this has not, please install this either from the Windows store or with `apt install python3-pip` for linux.

### Providing Your Translation

To utilize this tool, the translation must be done or reformatted into a format similar to the official [Eden's Garden Translation Sheet]() provided. Please refer to the format guide in the document to ensure it is up to standards as a translation. Note that one can define a custom template that is compatible. If assistance is required, feel free to reach out to Alette.

We outline a few rules that any translation must adhere to.


- Each 'segment' must match with the corresponding file name
- Each line not destined for a translation file must contain 'DONOTINCLUDE' in it's first column
- Any and all trailing newlines must be removed from translation.

### Creating Translation Files

### Translating Singular Files

### Translating All Files



## Developers

The team consists out of:
- [Alette](https://github.com/ThisIsSomeone)

This project was in due part possible to the help of Sweden.

## Coding and Testing Standards

No coding or testing standards for this project have been estabilished.

## License

You can find the license information for the Eden's Garden Translator in the [license file](LICENSE.md).