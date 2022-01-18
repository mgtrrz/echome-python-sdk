# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Types of changes:

* Added
* Changed
* Deprecated
* Removed
* Fixed
* Security

## [Unreleased]

## [0.5.1] - 2022-01-17
### Fixed
- Tags assigned with None will return empty dictionary

## [0.5.0] - 2022-01-17
### Changed
- Continual changes to work with new API endpoints
- Some commands have changed and moved to different namespaces to match the server API
  
## [0.4.0] - 2021-11-11

### Changed
- API endpoints have been modified to work with with the new namespaced server-side endpoints

## [0.3.1] - 2021-09-26

### Removed
- Describe VM now returns a proper response

### Changed
- Additional testing added

## [0.3.0] - 2021-09-25

### Added
- Ability to specify server, credentials, or profile when instantiating the Session class

### Changed
- Compatibility with new server release
- Refactored a lot of Session code and allows better handling of cases

## [0.2.0] - 2021-04-03

### Added
- Add new Network, Access, and Kubernetes cluster endpoints

### Changed
- Move base resource to its own file/class
- Cleaned up a few of the classes

## [0.1.0] - 2020-07-01

### Added
- Initial import of ecHome python SDK

[unreleased]: https://github.com/mgtrrz/echome-python-sdk/compare/0.5.1...HEAD
[0.5.1]: https://github.com/mgtrrz/echome-python-sdk/compare/0.4.0...0.5.1
[0.5.0]: https://github.com/mgtrrz/echome-python-sdk/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/mgtrrz/echome-python-sdk/compare/0.3.1...0.4.0
[0.3.1]: https://github.com/mgtrrz/echome-python-sdk/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/mgtrrz/echome-python-sdk/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/mgtrrz/echome-python-sdk/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/mgtrrz/echome-python-sdk/releases/tag/0.1.0
