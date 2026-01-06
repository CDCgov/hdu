# Health Data Utilties (hdu)

This repository contains a collection of tools that perform the following:


* FHIR ValueSet Resources - Content Delivery Netowrk (CDN) - Fetch Read-only FHIR endpoints to get codeset information (e.g. condition codes.)
* FHIR Server Inspector - Fetch a FHIR server's discoverable metadata including its capability statement, SMART configuration, and more.
* CDA2FHIR Parsing Tool - Convert CDA(XML) to FHIR JSON Bundle.
* Data Element and Code Value Specific APIs - Content Delivery Netowrk (CDN) - Fetch information on Data Elements and specific code values.
* HL7v2 Validation and Parsing Tool - Parse HL7v2 messages into a JSON object.
* National Provider Identifier (NPI) Validation - Validate an NPI number before submitting it for processing.
* Check a Direct Address or Endpoint - Fetch certificates in DNS and LDAP(Public) for a given Direct endpoint or email address.


This repo a Django 5 project, however, the tools and libraries can be accessed in Python3 or via command-line utility. 
Each tool is seperated into its own individual Django app.  Django is not needed to use the underlying Python3 libraries of the command-line utilities.  Individual apps live under the `apps` folder.  Be sure to first  install requirements using the command `pip install -r requirements.txt`.


## License Standard Notice
The repository utilizes code licensed under the terms of the Apache Software
License and therefore is licensed under ASL v2 or later.



## Privacy Standard Notice
This repository contains only non-sensitive, publicly available data and
information. All material and community participation is covered by the
[Disclaimer](DISCLAIMER.md)
and [Code of Conduct](code-of-conduct.md).
For more information about CDC's privacy policy, please visit [http://www.cdc.gov/other/privacy.html](https://www.cdc.gov/other/privacy.html).

## Contributing Standard Notice
Anyone is encouraged to contribute to the repository by [forking](https://help.github.com/articles/fork-a-repo)
and submitting a pull request. (If you are new to GitHub, you might start with a
[basic tutorial](https://help.github.com/articles/set-up-git).) By contributing
to this project, you grant a world-wide, royalty-free, perpetual, irrevocable,
non-exclusive, transferable license to all users under the terms of the
[Apache Software License v2](http://www.apache.org/licenses/LICENSE-2.0.html) or
later.

All comments, messages, pull requests, and other submissions received through
CDC including this GitHub page may be subject to applicable federal law, including but not limited to the Federal Records Act, and may be archived. Learn more at [http://www.cdc.gov/other/privacy.html](http://www.cdc.gov/other/privacy.html).