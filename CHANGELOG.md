# Changelog

## [0.18.0](https://github.com/instill-ai/python-sdk/compare/v0.17.2...v0.18.0) (2025-06-24)


### Features

* **cli,model,llm-runtime:** unify LLM runtimes ([#285](https://github.com/instill-ai/python-sdk/issues/285)) ([9950b8a](https://github.com/instill-ai/python-sdk/commit/9950b8ab4d3de8461c3af1f49efd4ecaa2613774))


### Miscellaneous

* **deps-dev:** bump setuptools from 74.1.2 to 78.1.1 ([#279](https://github.com/instill-ai/python-sdk/issues/279)) ([33fda4f](https://github.com/instill-ai/python-sdk/commit/33fda4f77536a37c724a36b0bb6be6e34612aad7))
* **deps-dev:** bump tornado from 6.4.2 to 6.5.1 ([#280](https://github.com/instill-ai/python-sdk/issues/280)) ([0caa2fe](https://github.com/instill-ai/python-sdk/commit/0caa2fe7f79a31382141f21f0edc862650a8c107))
* **deps:** bump protobuf from 4.25.3 to 4.25.8 ([#286](https://github.com/instill-ai/python-sdk/issues/286)) ([4b122cf](https://github.com/instill-ai/python-sdk/commit/4b122cfbd228f165e62c0b56e5b4310a71567af8))
* **deps:** bump requests from 2.32.3 to 2.32.4 ([#282](https://github.com/instill-ai/python-sdk/issues/282)) ([970f693](https://github.com/instill-ai/python-sdk/commit/970f693bb0b35a3a894c42f7194fbe7d7453ad69))
* **domain:** update production domain ([3f0efe0](https://github.com/instill-ai/python-sdk/commit/3f0efe07b17fa50a9224f8c8e798a1730cad3d54))
* **mypy:** fix make check errors ([971e640](https://github.com/instill-ai/python-sdk/commit/971e64023aec28378ddc5dcea50519b1efd6e2e9))
* **pacakge:** upgrade versions ([4e45717](https://github.com/instill-ai/python-sdk/commit/4e45717fce55b10e338474688dc4ddcd9ad1f373))
* **poetry:** lock ray version on 2.47.0 ([da75851](https://github.com/instill-ai/python-sdk/commit/da75851f229bd46271c90e4e2559763fe5ac16cb))
* release v0.18.0 ([f267cad](https://github.com/instill-ai/python-sdk/commit/f267cad0bd71066ec413cd1c90165d4ab1b4234a))
* **release-please:** update config.json ([#281](https://github.com/instill-ai/python-sdk/issues/281)) ([13cbace](https://github.com/instill-ai/python-sdk/commit/13cbace811abd24c39039d907fc202cae26fda17))


### Tests

* **instill:** improve unit test coverage ([#287](https://github.com/instill-ai/python-sdk/issues/287)) ([6f38ea9](https://github.com/instill-ai/python-sdk/commit/6f38ea9036733b4c05e334fb48f9d9578f8e87df))

## [0.17.2](https://github.com/instill-ai/python-sdk/compare/v0.17.1...v0.17.2) (2025-05-17)


### Bug Fixes

* **ray:** make non-editable work with dynamic pkg import ([#277](https://github.com/instill-ai/python-sdk/issues/277)) ([0bd4807](https://github.com/instill-ai/python-sdk/commit/0bd480722c63cac9fc242766087ddd1117856ff6))

## [0.17.1](https://github.com/instill-ai/python-sdk/compare/v0.17.0...v0.17.1) (2025-05-17)


### Bug Fixes

* **ray:** fix dynamic package loading issue ([#275](https://github.com/instill-ai/python-sdk/issues/275)) ([c812d14](https://github.com/instill-ai/python-sdk/commit/c812d1453451c44607213f1a0067d16a22c17250))

## [0.17.0](https://github.com/instill-ai/python-sdk/compare/v0.16.2...v0.17.0) (2025-04-15)


### Features

* **cli:** enhance CLI functionality and add Docker support ([#268](https://github.com/instill-ai/python-sdk/issues/268)) ([8fa8fed](https://github.com/instill-ai/python-sdk/commit/8fa8fedd054a14641ee98f8527722060bc41f654))
* **ray:** add high scale config ([#261](https://github.com/instill-ai/python-sdk/issues/261)) ([ccf24b2](https://github.com/instill-ai/python-sdk/commit/ccf24b26b474dc4eac018bc183601ba9677a86d3))


### Bug Fixes

* **client, const:** add secure argument to latest SDK client ([#271](https://github.com/instill-ai/python-sdk/issues/271)) ([1355086](https://github.com/instill-ai/python-sdk/commit/1355086db4b7ed04bda02b1ac222424b9c49534d))
* **ray:** align autoscale config ([#263](https://github.com/instill-ai/python-sdk/issues/263)) ([c07b787](https://github.com/instill-ai/python-sdk/commit/c07b787ffba23eca592a08f9d2186401d67aca42))
* **ray:** fix config not applied ([0bc15de](https://github.com/instill-ai/python-sdk/commit/0bc15deea3dc3e46d2e90ed48b828b575ce81c5d))
* **ray:** override max replica ([7e456ca](https://github.com/instill-ai/python-sdk/commit/7e456ca59d51af3a62c99b53f1a7d162a1231dd8))
* **ray:** update high scale model config ([#264](https://github.com/instill-ai/python-sdk/issues/264)) ([1086e6d](https://github.com/instill-ai/python-sdk/commit/1086e6d98be3831562fa9b8650442a3c598412cb))

## [0.16.2](https://github.com/instill-ai/python-sdk/compare/v0.16.1...v0.16.2) (2025-02-19)


### Bug Fixes

* **ray:** add -y for apt package installation ([#255](https://github.com/instill-ai/python-sdk/issues/255)) ([d58787b](https://github.com/instill-ai/python-sdk/commit/d58787beafa4e18a825b84d8cecaccefe6ceaa93))

## [0.16.1](https://github.com/instill-ai/python-sdk/compare/v0.16.0...v0.16.1) (2025-02-17)


### Bug Fixes

* **ray:** remove timezone for compatibility issue ([#253](https://github.com/instill-ai/python-sdk/issues/253)) ([d242f44](https://github.com/instill-ai/python-sdk/commit/d242f4456e75c2047e66c910714c143fc2be4025))

## [0.16.0](https://github.com/instill-ai/python-sdk/compare/v0.15.1...v0.16.0) (2024-12-06)


### Features

* **cli:** support multi-gpus when running inference locally ([#249](https://github.com/instill-ai/python-sdk/issues/249)) ([6760651](https://github.com/instill-ai/python-sdk/commit/6760651cd0aa4764c2b0a88fde4689d33358f01b))
* **proto:** update protogen ([#240](https://github.com/instill-ai/python-sdk/issues/240)) ([5fd0db1](https://github.com/instill-ai/python-sdk/commit/5fd0db17c1dcb82dfbaf9c5c88ffda6c28ad50fa))
* **vdp:** return dict type instead of proto type in trigger pipeline ([#242](https://github.com/instill-ai/python-sdk/issues/242)) ([8e6b3a7](https://github.com/instill-ai/python-sdk/commit/8e6b3a730059d7ce453e51abea096d2b356a1e0a))


### Bug Fixes

* **cli:** align timezone between host and model container ([#247](https://github.com/instill-ai/python-sdk/issues/247)) ([aa84a1c](https://github.com/instill-ai/python-sdk/commit/aa84a1c0333289906133a613199de066bbed37b6))
* **cli:** fix curl script ([444b210](https://github.com/instill-ai/python-sdk/commit/444b210c190b7256f21fcf90063167c0cebc23a0))
* **cli:** replace fix wait time with curl loop ([#245](https://github.com/instill-ai/python-sdk/issues/245)) ([3f62de1](https://github.com/instill-ai/python-sdk/commit/3f62de1ac3b142c016804bb13a29f081eb778c9c))
* **cli:** update run command shmsize ([#246](https://github.com/instill-ai/python-sdk/issues/246)) ([d08cf37](https://github.com/instill-ai/python-sdk/commit/d08cf37542a0bf9189390184716fcfa36d7820b6))

## [0.15.1](https://github.com/instill-ai/python-sdk/compare/v0.15.0...v0.15.1) (2024-11-05)


### Bug Fixes

* **ray:** fix semantic segmentation task parser ([#237](https://github.com/instill-ai/python-sdk/issues/237)) ([652c548](https://github.com/instill-ai/python-sdk/commit/652c5480f11a852a7af23e09bbd8dfd91d9f659e))

## [0.15.0](https://github.com/instill-ai/python-sdk/compare/v0.14.0...v0.15.0) (2024-10-22)


### Features

* **ray:** support shorter downscale config for test models ([#234](https://github.com/instill-ai/python-sdk/issues/234)) ([954f94b](https://github.com/instill-ai/python-sdk/commit/954f94b3c0b1e15d88162dc08c707ef700156831))


### Bug Fixes

* **vdp:** allow empty input for recipe parameter ([#229](https://github.com/instill-ai/python-sdk/issues/229)) ([033ca6c](https://github.com/instill-ai/python-sdk/commit/033ca6cc977f0b216281a15f26b1f051a241115f))
* **vdp:** fix create pipeline input parameters ([#225](https://github.com/instill-ai/python-sdk/issues/225)) ([3fd0538](https://github.com/instill-ai/python-sdk/commit/3fd0538432161b201501f4e2c65b1f7ed83ceaec))
* **vdp:** fix create/update connection input parameters ([#230](https://github.com/instill-ai/python-sdk/issues/230)) ([f3d0bec](https://github.com/instill-ai/python-sdk/commit/f3d0bec9966370c2a7abe8919e61cdcb262a1b07))
* **vdp:** fix update pipeline mask ([#236](https://github.com/instill-ai/python-sdk/issues/236)) ([2107a40](https://github.com/instill-ai/python-sdk/commit/2107a409cf684fe6be61d47d4efba848f72bf26f))
* **vdp:** fix update pipeline parameter ([#233](https://github.com/instill-ai/python-sdk/issues/233)) ([b19a59c](https://github.com/instill-ai/python-sdk/commit/b19a59cc7960b24d7e226348ab7561a358b7ff07))
* **vdp:** rename create pipeline input parameters ([#228](https://github.com/instill-ai/python-sdk/issues/228)) ([2220438](https://github.com/instill-ai/python-sdk/commit/2220438a72c6c25e96a857f75f7793eb52797acd))

## [0.14.0](https://github.com/instill-ai/python-sdk/compare/v0.13.0...v0.14.0) (2024-10-12)


### Features

* **app:** update AppClient ([#221](https://github.com/instill-ai/python-sdk/issues/221)) ([ccfc9fe](https://github.com/instill-ai/python-sdk/commit/ccfc9fe283d9e63a6da8b0fb6f0eef03d32b5bad))
* **client:** update proto and add AppClient ([#213](https://github.com/instill-ai/python-sdk/issues/213)) ([6a73033](https://github.com/instill-ai/python-sdk/commit/6a73033063d5c7f6320fcc5db4c2f49365c7833b))


### Bug Fixes

* **app:** rename app_service to app ([#224](https://github.com/instill-ai/python-sdk/issues/224)) ([f33aff3](https://github.com/instill-ai/python-sdk/commit/f33aff3be1f82e1cd4e7426295c17d21af7e0cde))

## [0.13.0](https://github.com/instill-ai/python-sdk/compare/v0.12.1...v0.13.0) (2024-10-07)


### Features

* **client:** support namespace and requester ([#217](https://github.com/instill-ai/python-sdk/issues/217)) ([f524739](https://github.com/instill-ai/python-sdk/commit/f5247399e91b3334e92a74659874c4daa83252fe))
* **client:** support target namespace and extra header ([#215](https://github.com/instill-ai/python-sdk/issues/215)) ([19563ac](https://github.com/instill-ai/python-sdk/commit/19563ac9496010e0de6ec488aaf48425163aab23))

## [0.12.1](https://github.com/instill-ai/python-sdk/compare/v0.12.0...v0.12.1) (2024-09-12)


### Bug Fixes

* **ray:** fix misaligned message and image length ([#211](https://github.com/instill-ai/python-sdk/issues/211)) ([dd8ceeb](https://github.com/instill-ai/python-sdk/commit/dd8ceeb9ad216bd204c478d6b20b7afbfeed12c5))

## [0.12.0](https://github.com/instill-ai/python-sdk/compare/v0.11.0...v0.12.0) (2024-09-11)


### Features

* **artifact:** update get_file_catalog input parameter default values ([#203](https://github.com/instill-ai/python-sdk/issues/203)) ([f5da73f](https://github.com/instill-ai/python-sdk/commit/f5da73f03035dcb3022c5d212fc1c351e6c5350f))
* **ray:** implement model local run and adopt latest task spec ([#196](https://github.com/instill-ai/python-sdk/issues/196)) ([5b67b56](https://github.com/instill-ai/python-sdk/commit/5b67b569672c16d12428c82baece882e948f0d56))
* **ray:** support multimodal embedding input ([#204](https://github.com/instill-ai/python-sdk/issues/204)) ([e150ad1](https://github.com/instill-ai/python-sdk/commit/e150ad1a70fedeb743bab882c6b07ccc912a269f))


### Bug Fixes

* **dockerfile:** revert storing cache dir ([#207](https://github.com/instill-ai/python-sdk/issues/207)) ([297f1f1](https://github.com/instill-ai/python-sdk/commit/297f1f102d1fbab936b345bd3633c7005f536963))
* **ray:** append mime type for image output ([#208](https://github.com/instill-ai/python-sdk/issues/208)) ([9e38b70](https://github.com/instill-ai/python-sdk/commit/9e38b70402f3902428554750d5dfe800b8cca301))
* **ray:** fix bounding box output type ([#205](https://github.com/instill-ai/python-sdk/issues/205)) ([22242df](https://github.com/instill-ai/python-sdk/commit/22242df4d32f2605f0fb30818c49fc42ae940e85))
* **ray:** fix multimodal chat input ([#210](https://github.com/instill-ai/python-sdk/issues/210)) ([37aa13a](https://github.com/instill-ai/python-sdk/commit/37aa13a99ad725e36aa9797ce53aaf90b0a7830c))
* **ray:** fix number of sample type ([#206](https://github.com/instill-ai/python-sdk/issues/206)) ([c87527d](https://github.com/instill-ai/python-sdk/commit/c87527da2cb2f36532edfe59dbe10c587402da88))
* **ray:** replace user-agent header ([#209](https://github.com/instill-ai/python-sdk/issues/209)) ([e18b217](https://github.com/instill-ai/python-sdk/commit/e18b21734d6d64cc62b2b25017c03f6b8c00dd54))

## [0.11.0](https://github.com/instill-ai/python-sdk/compare/v0.10.2...v0.11.0) (2024-09-04)


### Features

* **artifact:** updated proto and client code ([#193](https://github.com/instill-ai/python-sdk/issues/193)) ([e6e54b1](https://github.com/instill-ai/python-sdk/commit/e6e54b1de71536564c729b77fdc556989756a9db))


### Bug Fixes

* **vdp:** fix trigger pipeline release input ([#198](https://github.com/instill-ai/python-sdk/issues/198)) ([db5224e](https://github.com/instill-ai/python-sdk/commit/db5224e995ff95ff43bb49030de43f3c1e78295a))

## [0.10.2](https://github.com/instill-ai/python-sdk/compare/v0.10.1...v0.10.2) (2024-07-31)


### Features

* **artifact:** updated proto and added client code ([#185](https://github.com/instill-ai/python-sdk/issues/185)) ([51942bd](https://github.com/instill-ai/python-sdk/commit/51942bdbd9690c3190f444170bbf820a1f825a86))
* **client:** adopt latest api spec ([#168](https://github.com/instill-ai/python-sdk/issues/168)) ([d33c050](https://github.com/instill-ai/python-sdk/commit/d33c050526e753a5e6d6d116889dff3351cc16af))


### Bug Fixes

* **client:** added some parameter default values for artifact ([#192](https://github.com/instill-ai/python-sdk/issues/192)) ([ab624f4](https://github.com/instill-ai/python-sdk/commit/ab624f42c821811cff665099769e54981d3b9d01))
* **specs:** deleted out-dated resources ([#183](https://github.com/instill-ai/python-sdk/issues/183)) ([be86e69](https://github.com/instill-ai/python-sdk/commit/be86e69c1301091db6beda202dc49db6c7658db7))


### Miscellaneous Chores

* **release:** release v0.10.2 ([f15a1a9](https://github.com/instill-ai/python-sdk/commit/f15a1a945659b6960664ed6ac9b71637bfd6dfab))

## [0.10.1](https://github.com/instill-ai/python-sdk/compare/v0.10.0...v0.10.1) (2024-06-29)


### Features

* **ray:** unify cli commands ([#167](https://github.com/instill-ai/python-sdk/issues/167)) ([6c31a4c](https://github.com/instill-ai/python-sdk/commit/6c31a4cdf21928af1910a05afe96da496c120a4a))


### Miscellaneous Chores

* **release:** release v0.10.1 ([2a88d53](https://github.com/instill-ai/python-sdk/commit/2a88d539f4739db8c74c3468600a2d53387a4b37))

## [0.10.0](https://github.com/instill-ai/python-sdk/compare/v0.9.0...v0.10.0) (2024-06-05)


### Features

* **client, resources:** adopt latest api spec ([#145](https://github.com/instill-ai/python-sdk/issues/145)) ([bafa292](https://github.com/instill-ai/python-sdk/commit/bafa2922b0a0b316cd3e454cc34b522b55640b85))
* **dockerfile:** separate config and weights into different layers ([#156](https://github.com/instill-ai/python-sdk/issues/156)) ([8d25fc3](https://github.com/instill-ai/python-sdk/commit/8d25fc325b49c64839f0460fc4f883ab012944a3))
* **ray:** support cuda version and fix user root permission ([#158](https://github.com/instill-ai/python-sdk/issues/158)) ([cd1fa69](https://github.com/instill-ai/python-sdk/commit/cd1fa69bc929f25f705dd4504506050b186ba61c))


### Bug Fixes

* **clients:** fix message length ([#147](https://github.com/instill-ai/python-sdk/issues/147)) ([8083761](https://github.com/instill-ai/python-sdk/commit/80837619ea9b1f8c535debd764a0a944c5dc088c))
* **resources:** fix nil response handling ([#151](https://github.com/instill-ai/python-sdk/issues/151)) ([c6df35c](https://github.com/instill-ai/python-sdk/commit/c6df35c8ca3c3ee16bbcddb180188a681f63371f))


### Documentation

* **readme:** update workflow name ([ba36a91](https://github.com/instill-ai/python-sdk/commit/ba36a9181dbfe679be7c92c5ff3dcd3541f88f6a))

## [0.9.0](https://github.com/instill-ai/python-sdk/compare/v0.8.1...v0.9.0) (2024-04-30)


### Features

* **ray:** implement standalone executable and optional system packages ([#141](https://github.com/instill-ai/python-sdk/issues/141)) ([c897080](https://github.com/instill-ai/python-sdk/commit/c8970802ff77b24812a10f8de19c6d2e86a67fbd))

## [0.8.1](https://github.com/instill-ai/python-sdk/compare/v0.8.0...v0.8.1) (2024-04-29)


### Bug Fixes

* **ray:** fix missing imports ([#139](https://github.com/instill-ai/python-sdk/issues/139)) ([02199b1](https://github.com/instill-ai/python-sdk/commit/02199b1a2f1e2d544a1cf8a740cce66edf8f5cd9))

## [0.8.0](https://github.com/instill-ai/python-sdk/compare/v0.7.1...v0.8.0) (2024-04-25)


### Features

* **deps:** upgrade ray version ([cc61b85](https://github.com/instill-ai/python-sdk/commit/cc61b8541c9545ca2b6768c519242af6f6b9df93))
* **ray:** adapt to native docker client instead of docker sdk ([#138](https://github.com/instill-ai/python-sdk/issues/138)) ([7d19ccb](https://github.com/instill-ai/python-sdk/commit/7d19ccbfe24eebe29e4a2e1729b2c82503ad4782))
* **ray:** add accelerator and custom resource support ([#118](https://github.com/instill-ai/python-sdk/issues/118)) ([f974f98](https://github.com/instill-ai/python-sdk/commit/f974f9826d28e4a54c89aa917ec37c5b3eac3c68))
* **ray:** add llava 13b to predeploy list ([3fd5914](https://github.com/instill-ai/python-sdk/commit/3fd591419c940f1635472b25b5bf8f6a522bfd15))
* **ray:** add metadata and infer constructor for llm tasks ([#137](https://github.com/instill-ai/python-sdk/issues/137)) ([be122d1](https://github.com/instill-ai/python-sdk/commit/be122d1b19516fa789c183f5e7128cb34a8c01e1))
* **ray:** generate sha256 as tag if not presented ([#120](https://github.com/instill-ai/python-sdk/issues/120)) ([6abb538](https://github.com/instill-ai/python-sdk/commit/6abb5380ace6df7e0eefff56d19b34559daf8982))
* **ray:** inject accelerator type at runtime ([#121](https://github.com/instill-ai/python-sdk/issues/121)) ([f78a2d0](https://github.com/instill-ai/python-sdk/commit/f78a2d0a604107d208a9783f89e54f68cb68e196))
* **ray:** support containerized model serving ([#116](https://github.com/instill-ai/python-sdk/issues/116)) ([ad0f250](https://github.com/instill-ai/python-sdk/commit/ad0f2505d49dec675558e65cc62e3901311a7673))
* **ray:** support custom accelerator type ([#134](https://github.com/instill-ai/python-sdk/issues/134)) ([ae6c139](https://github.com/instill-ai/python-sdk/commit/ae6c139d3c7eafa3015ec779628321185f76d381))
* **ray:** use env for resource and deprecate deploy/undeploy ([#124](https://github.com/instill-ai/python-sdk/issues/124)) ([a58bc50](https://github.com/instill-ai/python-sdk/commit/a58bc50f97ed8747da961b6cfbf416ea51361c95))
* **ray:** use tmp folder for image building ([#122](https://github.com/instill-ai/python-sdk/issues/122)) ([9512cec](https://github.com/instill-ai/python-sdk/commit/9512cecc47299b5542b6045fead4c70bab07628e))


### Bug Fixes

* **deps:** downgrade ray to avoid grpc servicer issue ([#128](https://github.com/instill-ai/python-sdk/issues/128)) ([9ead421](https://github.com/instill-ai/python-sdk/commit/9ead42178d606827e7f747f5e4150f6c6d12437a))
* **dockerfile:** avoid build hang at ARG statement ([#130](https://github.com/instill-ai/python-sdk/issues/130)) ([f02a27c](https://github.com/instill-ai/python-sdk/commit/f02a27c2f82c7ebe902b01037b2cdd01ddb6e231))
* **ray:** fix etrypoint module not found ([#126](https://github.com/instill-ai/python-sdk/issues/126)) ([f1ed83d](https://github.com/instill-ai/python-sdk/commit/f1ed83de1f7a8e190d3152ba9e3e9b02df5d3617))
* **ray:** fix missing default resource value ([#129](https://github.com/instill-ai/python-sdk/issues/129)) ([b2f564a](https://github.com/instill-ai/python-sdk/commit/b2f564ae2a0cb933497c49653d6707c7275a0226))
* **ray:** fix multi-platform build stage ([6f358fd](https://github.com/instill-ai/python-sdk/commit/6f358fd4b20dd33e09fdc453c9ddac1f515f3260))
* **ray:** support target platform for image building ([#127](https://github.com/instill-ai/python-sdk/issues/127)) ([f4825fc](https://github.com/instill-ai/python-sdk/commit/f4825fce259946072a71f2892a9686914c81ff55))

## [0.7.1](https://github.com/instill-ai/python-sdk/compare/v0.7.0...v0.7.1) (2024-02-22)


### Bug Fixes

* **ray:** update default resources allocation for test ([#102](https://github.com/instill-ai/python-sdk/issues/102)) ([1aaa905](https://github.com/instill-ai/python-sdk/commit/1aaa905ca74cc8afaa29e0290792b57bd12143e2))


### Miscellaneous Chores

* **release:** release v0.7.1 ([b7dec13](https://github.com/instill-ai/python-sdk/commit/b7dec13d87cf4bf1a6a25ba71b85213fc4dc582e))

## [0.7.0](https://github.com/instill-ai/python-sdk/compare/v0.6.0...v0.7.0) (2024-01-30)


### Features

* **ray:** determine ram usage by file size ([#89](https://github.com/instill-ai/python-sdk/issues/89)) ([7a0023d](https://github.com/instill-ai/python-sdk/commit/7a0023d1e2dd6600f69dd2ab08a8e9431a36da2b))
* **ray:** determine vram usage by file size ([#87](https://github.com/instill-ai/python-sdk/issues/87)) ([71e84e6](https://github.com/instill-ai/python-sdk/commit/71e84e68f029daa7b482e300e72f928cacb5e738))


### Bug Fixes

* **ray:** add vram ceiling and override list ([#94](https://github.com/instill-ai/python-sdk/issues/94)) ([5804e4a](https://github.com/instill-ai/python-sdk/commit/5804e4a182e6c3eba7011cf2d879b94b264d214f))
* **ray:** fix application name ([f2bb563](https://github.com/instill-ai/python-sdk/commit/f2bb56369c356619c95b6ef9d3568146c85a1ba7))
* **ray:** fix gpu resource &gt; 1 ([#91](https://github.com/instill-ai/python-sdk/issues/91)) ([b121f56](https://github.com/instill-ai/python-sdk/commit/b121f566011714c208ee804beba2db9f72849a56))
* **ray:** fix ray autoscaling ([#95](https://github.com/instill-ai/python-sdk/issues/95)) ([5bd8c2a](https://github.com/instill-ai/python-sdk/commit/5bd8c2a8b8432d6855854448b4f92ac755b0b020))

## [0.6.0](https://github.com/instill-ai/python-sdk/compare/v0.5.0...v0.6.0) (2024-01-12)


### Features

* **connector,operator,component:** adopt jsonscema validation and dataclass type hint ([#74](https://github.com/instill-ai/python-sdk/issues/74)) ([0c47e51](https://github.com/instill-ai/python-sdk/commit/0c47e51263f7e428499a8461db4b4725ac1e3144))
* **helpers:** add wrapper func for protobuf message ([#85](https://github.com/instill-ai/python-sdk/issues/85)) ([279bd1e](https://github.com/instill-ai/python-sdk/commit/279bd1e5ec6f9501a001c46acff93cee2a67388f))
* **resource:** adopt dataclass as config in component for type hinting ([#79](https://github.com/instill-ai/python-sdk/issues/79)) ([8c25bd1](https://github.com/instill-ai/python-sdk/commit/8c25bd106577cf75d0f24cd52c82ccc2f56baef1))
* **resources:** support recipe update in pipeline resource ([#83](https://github.com/instill-ai/python-sdk/issues/83)) ([89431fa](https://github.com/instill-ai/python-sdk/commit/89431fa39f626736b16ee279ae4b6c9f19a3c1c3))


### Bug Fixes

* **resources:** fix resource schema path ([#76](https://github.com/instill-ai/python-sdk/issues/76)) ([25f4418](https://github.com/instill-ai/python-sdk/commit/25f4418ab713556ab5a82b9bc16f7d0f9e12adc3))


### Documentation

* **notebook:** update notebook ([e5da642](https://github.com/instill-ai/python-sdk/commit/e5da642266b1666fe66b08798668bce6f7e8c05b))

## [0.5.0](https://github.com/instill-ai/python-sdk/compare/v0.4.0...v0.5.0) (2024-01-02)


### ⚠ BREAKING CHANGES

* **ray:** retire non-decorator deploy and update scaling config ([#67](https://github.com/instill-ai/python-sdk/issues/67))

### Features

* **model:** Update Text-Generation Task Schema to Align with OpenAI Standards  ([#69](https://github.com/instill-ai/python-sdk/issues/69)) ([703789a](https://github.com/instill-ai/python-sdk/commit/703789a6d09cfa857b13f296834f87a6daffb18d))


### Bug Fixes

* **model:** fix image decoding issue ([#71](https://github.com/instill-ai/python-sdk/issues/71)) ([5c571b2](https://github.com/instill-ai/python-sdk/commit/5c571b2aec543fcf2208ad83219b1b94dfca3078))
* **ray:** allow cwd as runtime env ([#66](https://github.com/instill-ai/python-sdk/issues/66)) ([00c0497](https://github.com/instill-ai/python-sdk/commit/00c0497ac6bf7232b6ac2d0d18549a7edd3cc03e))
* **ray:** avoid agressive downscale and non upscale ([#70](https://github.com/instill-ai/python-sdk/issues/70)) ([f159314](https://github.com/instill-ai/python-sdk/commit/f1593141d2d5f60faeb51e83a091cd3755c9d9f5))


### Documentation

* **notebooks:** add async example ([49ca895](https://github.com/instill-ai/python-sdk/commit/49ca8956691810590799b494120eb5b95e8b6e5c))


### Code Refactoring

* **ray:** retire non-decorator deploy and update scaling config ([#67](https://github.com/instill-ai/python-sdk/issues/67)) ([89ef078](https://github.com/instill-ai/python-sdk/commit/89ef0787d436ba45933b92e405ce5c2e3f2a6aa9))

## [0.4.0](https://github.com/instill-ai/python-sdk/compare/v0.3.2...v0.4.0) (2023-12-11)


### ⚠ BREAKING CHANGES

* **client:** support asyncio and add better client type hint ([#55](https://github.com/instill-ai/python-sdk/issues/55))

### Features

* **client:** support asyncio and add better client type hint ([#55](https://github.com/instill-ai/python-sdk/issues/55)) ([aa41246](https://github.com/instill-ai/python-sdk/commit/aa41246b6ae3c27d62438436b2023316d2e1d664))
* **org:** adopt organization endpoints for VDP ([#60](https://github.com/instill-ai/python-sdk/issues/60)) ([0c313d6](https://github.com/instill-ai/python-sdk/commit/0c313d605ceb016a7bb534a20c545d3187d1be83))
* **ray:** add io helpers for llm tasks ([#59](https://github.com/instill-ai/python-sdk/issues/59)) ([1876a20](https://github.com/instill-ai/python-sdk/commit/1876a20256f3bb82ad37ca88fd83e849a3dd14cc))
* **ray:** add nested decorators ([#63](https://github.com/instill-ai/python-sdk/issues/63)) ([900dda8](https://github.com/instill-ai/python-sdk/commit/900dda8ac952e933aa9cbb35274c19b8ecbab252))
* **ray:** add text to image io helper ([#58](https://github.com/instill-ai/python-sdk/issues/58)) ([0430977](https://github.com/instill-ai/python-sdk/commit/04309779454ef6a0078efc6636735f4e4e2d7af5))


### Bug Fixes

* **clients,resources:** fix resource creating will get None type ([#57](https://github.com/instill-ai/python-sdk/issues/57)) ([4516d46](https://github.com/instill-ai/python-sdk/commit/4516d466b6e7ce0891f06d6616123e35e3b2291e))
* **makefile:** fix wheel build missing submodule ([9aa73eb](https://github.com/instill-ai/python-sdk/commit/9aa73ebd157d08fc1ab7975eeb2fa9e407c2e330))
* **ray:** fix missing ray init ([#64](https://github.com/instill-ai/python-sdk/issues/64)) ([db0b5c4](https://github.com/instill-ai/python-sdk/commit/db0b5c49a154b73f6607fc02c8b6d157d01e619e))


### Documentation

* **notebooks:** update notebooks to adopt latest ray decorators ([52b90c6](https://github.com/instill-ai/python-sdk/commit/52b90c6283984158670773629017289f76e508d5))

## [0.3.2](https://github.com/instill-ai/python-sdk/compare/v0.3.1...v0.3.2) (2023-11-29)


### Bug Fixes

* **client:** fix async pipeline trigger and get user ([#53](https://github.com/instill-ai/python-sdk/issues/53)) ([c86274b](https://github.com/instill-ai/python-sdk/commit/c86274bb1a0332b12f2f94f4644cadbe339118a6))
* **ray:** fix mismatched grpcio version ([024471a](https://github.com/instill-ai/python-sdk/commit/024471aafb96e8ad48cfbe4c10033d584ee5b35e))
* **ray:** fix model weight file extension ([4f3a40c](https://github.com/instill-ai/python-sdk/commit/4f3a40c005b3ca0b8ab96f28b6613474d932622a))

## [0.3.1](https://github.com/instill-ai/python-sdk/compare/v0.3.0...v0.3.1) (2023-11-08)


### Bug Fixes

* **ray:** fix wrong scope of actor config ([85dd1f1](https://github.com/instill-ai/python-sdk/commit/85dd1f15c7b3d8460fa005bf58d4ef9d56f00838))


### Documentation

* **readme:** update readme for optional config file ([4efd5d6](https://github.com/instill-ai/python-sdk/commit/4efd5d6d24d88d992ca96e4044d6547bc741e391))

## [0.3.0](https://github.com/instill-ai/python-sdk/compare/v0.2.1...v0.3.0) (2023-11-07)


### ⚠ BREAKING CHANGES

* **client:** fix wrongful delete of resources and connection not close ([#42](https://github.com/instill-ai/python-sdk/issues/42))

### Features

* **ray:** add help functions for ray model ([#40](https://github.com/instill-ai/python-sdk/issues/40)) ([39b2cc7](https://github.com/instill-ai/python-sdk/commit/39b2cc7a6bcff73956d0b67f34d45ad2821ffaef))


### Bug Fixes

* **client:** fix wrongful delete of resources and connection not close ([#42](https://github.com/instill-ai/python-sdk/issues/42)) ([d32fb83](https://github.com/instill-ai/python-sdk/commit/d32fb838f1711c0a529cc1ad0327e43c9c44de39))
* **config,pipeline:** allow no config file and fix required pipeline recipe ([#43](https://github.com/instill-ai/python-sdk/issues/43)) ([5290868](https://github.com/instill-ai/python-sdk/commit/5290868ac9d6375bbf7be3a9463aab7eddfd5d59))

## [0.2.1](https://github.com/instill-ai/python-sdk/compare/v0.2.0...v0.2.1) (2023-10-27)


### Miscellaneous Chores

* **release:** release v0.2.1 ([871d7b9](https://github.com/instill-ai/python-sdk/commit/871d7b9f5a6ebd1a3eb85891a584698b4c2c0090))

## [0.2.0](https://github.com/instill-ai/python-sdk/compare/v0.1.0...v0.2.0) (2023-10-15)


### ⚠ BREAKING CHANGES

* **config:** update config file extension
* **config:** update config file path to avoid collision ([#35](https://github.com/instill-ai/python-sdk/issues/35))

### Documentation

* **readme:** update README ([#29](https://github.com/instill-ai/python-sdk/issues/29)) ([5820fff](https://github.com/instill-ai/python-sdk/commit/5820fff36ab9352463187554603e659800595870))


### Code Refactoring

* **config:** update config file extension ([9b0f17f](https://github.com/instill-ai/python-sdk/commit/9b0f17feac128045d9853afd0ae2ef3c78a0e69e))
* **config:** update config file path to avoid collision ([#35](https://github.com/instill-ai/python-sdk/issues/35)) ([0b5b3bd](https://github.com/instill-ai/python-sdk/commit/0b5b3bd869eb45b4695ade0e9c3dc1ef26283781))

## 0.1.0 (2023-10-01)


### Features

* **auth:** adopt `Instill Core` auth ([#16](https://github.com/instill-ai/python-sdk/issues/16)) ([86c0e85](https://github.com/instill-ai/python-sdk/commit/86c0e85e7d626633264303c6faefb5610f18f036))
* **auth:** support api-token for instill cloud authentication ([#6](https://github.com/instill-ai/python-sdk/issues/6)) ([e041510](https://github.com/instill-ai/python-sdk/commit/e0415105fa968b11eb2c5e902141d0dec60d07ea))
* **component,recipe:** support better component/recipe creation ([#22](https://github.com/instill-ai/python-sdk/issues/22)) ([857e260](https://github.com/instill-ai/python-sdk/commit/857e260f3ba6876dc814538aa2346ac4132a9a27))
* **config:** adopt pydantic for yaml config validation ([#9](https://github.com/instill-ai/python-sdk/issues/9)) ([8903975](https://github.com/instill-ai/python-sdk/commit/8903975753434b6f9ad25ed97feb81b76fc7f0b2))


### Bug Fixes

* **clients:** fix metadata overwrite ([#26](https://github.com/instill-ai/python-sdk/issues/26)) ([e332cb0](https://github.com/instill-ai/python-sdk/commit/e332cb09e60497f5c002a61de8ab43a03c475ced))


### Documentation

* **contributing,readme:** update docs and workflow for contributing ([#12](https://github.com/instill-ai/python-sdk/issues/12)) ([6fb0c84](https://github.com/instill-ai/python-sdk/commit/6fb0c84e44f654d7eea286405133912fe7967334))
* **readme,notebook:** add a notebook example ([9f8d728](https://github.com/instill-ai/python-sdk/commit/9f8d7283ad38865c18e4490afb5720dbbc65eb8a))
* **readme:** add usage in README ([#24](https://github.com/instill-ai/python-sdk/issues/24)) ([5af5f42](https://github.com/instill-ai/python-sdk/commit/5af5f4209391b7cfb657643456b5013ce83a8450))
