The ```GhidraTool``` is a key component of the Reverse Mosaic multi-agent binary analysis toolkit. It facilitates interactions with Ghidra, an open-source software reverse engineering framework.

This tool provides several functionalities for analyzing binary files using Ghidra:

- **Retrieving Function Names and Addresses**: The ```get_all_function_names_and_addresses``` method retrieves all function names and their respective addresses in a binary.

- **Cross-Referencing Functions**: The ```get_cross_references_to_function_name``` method retrieves a list of cross-references to a given function name.

- **Decompiling Functions**: The ```get_decom_for_function``` method decompiles a function of a binary and returns the decompiled C code.

- **Retrieving Function Addresses and Names**: The ```get_function_address_by_name``` method retrieves the address of a function, while the get_function_name_by_address method retrieves the name of a function.

<p align="center"> <img margin-right: auto width=25% src="../../../../small-logo.png"> </p>
