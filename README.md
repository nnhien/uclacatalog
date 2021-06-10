# UCLA Catalog
A Python library to retrieve course and section information from the UCLA Registrar

## Why
While [UCB](https://old.reddit.com/r/ucla/comments/hcqyrt/a_psa_to_ucla_students_from_the_berkeley_community/) has [BerkeleyTime](https://berkeleytime.com) and UCSD has their own in-house API that students may use to request course and section information, UCLA has no such service. In fact, course numbers, titles, descriptions, and information about sections are spread between two different domains, one of which only responds properly if you spoof a request header. Not only this, but there is no documentation for the archaic and inconsistent modeling that the backend will respond to, making the lives of student developers who want to create services that allow their classmates to access course and section information unnecessarily difficult.

This library aims to make it less of a hassle for UCLA student developers to access details about courses and their related sections.

## Contributing
The foundation of this library was built in less than a week with little initial knowledge of Python. Therefore, there will be lots of code that doesn't follow Python conventions and functions that are inefficient. Feel free to contribute by fixing bugs, making things more efficient, and/or expanding the information given by the models. 

Bugs should be reported to the [issue tracker](https://github.com/nnhien/uclacatalog/issues).

## Usage

### Installation
`pip install uclacatalog`

See the [wiki](https://github.com/nnhien/uclacatalog/wiki) for documentation

## License
This project is licensed under [LGPLv3](https://github.com/nnhien/uclacatalog/blob/master/LICENSE) and is free (both as in no-cost and freedom) software. Thus, you are free to modify, distribute and use this library "as-is" for whatever purposes you like, including as part of a larger work. If you modify this library, you must clearly publish modifications.
