# UCLA Catalog
A Python library to retrieve course and section information from the UCLA Registrar

## Why
While [UCB](https://old.reddit.com/r/ucla/comments/hcqyrt/a_psa_to_ucla_students_from_the_berkeley_community/) has [BerkeleyTime](https://berkeleytime.com) and UCSD has their own in-house API that students may use to request course and section information, UCLA has no such service. In fact, course numbers, titles, descriptions, and information about sections are spread between two different domains and three paths, one of which only responds properly if you spoof a request header. Not only this, but there is no documentation for the archaic and inconsistent modeling that the backend will respond to, making the lives of student developers who want to create services that allow their classmates to access course and section information unnecessarily difficult.

This library aims to make it less of a hassle for UCLA student developers to access details about courses and their related sections.

## Contributing
The foundation of this library was built in less than a week with little founding knowledge of Python. Therefore, there will be lots of code that doesn't follow Python conventions or functions that are inefficient. Feel free to contribute by fixing bugs or adding additional features. 

Bugs should be reported to the [issue tracker](https://github.com/nnhien/uclacatalog/issues).

Note that additional features should strictly expand the amount of information that the models provide. Any additional parsing should be done within the application that uses this library.

## Usage
See the [wiki](https://github.com/nnhien/uclacatalog/wiki) for documentation

## License
This project is licensed under GPLv3 and is free (both as in no-cost and freedom) software. Thus, you are free to modify, use, and distribute this library for whatever purposes you like. If you ship an application in a binary form using this library (e.g. an iOS or Android app that accesses the UCLA catalog using a library written in Swift or Kotlin that's derived from this library, since that library *should* also be licensed under GPLv3), your application must also be licensed under and must follow the terms of GPLv3. However, if you use this library as a part of a SaaS application (e.g. a Discord bot where you are the sole person hosting it), your application is not required to be licensed under GPLv3. The full implications of this license can be found [here](https://github.com/nnhien/uclacatalog/blob/master/LICENSE).