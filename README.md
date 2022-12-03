# CambridgeDict.py
Python HTML parser for [Cambridge dictionary](https://dictionary.cambridge.org/).

* [x] English, american and business dictionaries 

# Requirements
* requests
* beautifulsoup4

# Return pattern
```python
{<word>: 
       {<pos>: {'UK_IPA': [UK IPA for the 1-st definition, ..., UK IPA for the N-th definition],
                'UK_audio_links': [[1-st uk audio link for the 1-st definition, ...],
                                  ...
                                  [1-st uk audio link for the N-th definition, ...]],
                'US_IPA': [US IPA for the 1-st definition, ..., US IPA for the N-th definition],
                'US_audio_links': [[1-st us audio link for the 1-st definition, ...],
                                  ...
                                  [1-st us audio link for the N-th definition, ...]],
                'alt_terms': [[alt_terms_1], ..., [alt_terms_N]],
                'irregular_forms': [[1-st irregular form for the 1-st definition, ...],
                                    ...
                                    [1-st irregular form for the N-th definition, ...]],
                'definitions': [definition_1, ..., definition_N],
                'domain': [[domains_1], ..., [domains_N]],
                'examples': [[1-st sentence example for the 1-st definition, ...],
                             ...
                             [1-st sentence example for the N-th definition, ...]],
                'images': [dict_image_link_1, ..., dict_image_link_n],
                'labels_and_codes': [labels_and_codes_1, ..., labels_and_codes_N],
                'level': [[level_1], ..., [level_N]],
                'region': [[region_1], ..., [region_N]],
                'usage': [[usage_1], ..., [usage_N]]},
       ...
}}
```
# Example

```python
define('reconnaissance')

--->   {'reconnaissance': {'noun': {'UK_IPA': [['/rɪˈkɒn.ɪ.səns/']],
                                   'UK_audio_links': [['https://dictionary.cambridge.org//media/english/uk_pron/u/ukr/ukrec/ukrecli023.mp3']],
                                   'US_IPA': [['/rɪˈkɑː.nə.səns/']],
                                   'US_audio_links': [['https://dictionary.cambridge.org//media/english/us_pron/r/rec/recon/reconnaissance.mp3']],
                                   'alt_terms': [['(UK informal recce)',
                                                 '(US informal recon)']],
                                   'definitions': ['the process of getting '
                                                 'information about enemy forces '
                                                 'or positions by sending out '
                                                 'small groups of soldiers or by '
                                                 'using aircraft, etc.'],
                                   'domain': [['military']],
                                   'examples': [['Aerial reconnaissance of the enemy '
                                                 'position showed they were ready to '
                                                 'attack.']],
                                   'image_links': [''],
                                   'irregular_forms': [[]],
                                   'labels_and_codes': [['[ U ]']],
                                   'level': [[]],
                                   'region': [[]],
                                   'usage': [['specialized']]}}}

define("ox")
--->   {'ox': {'noun': {'UK_IPA': [['/ɒks/']],
                     'UK_audio_links': [['https://dictionary.cambridge.org//media/english/uk_pron/u/uko/ukove/ukoverw016.mp3']],
                     'US_IPA': [['/ɑːks/']],
                     'US_audio_links': [['https://dictionary.cambridge.org//media/english/us_pron/e/eus/eus75/eus75458.mp3']],
                     'alt_terms': [[]],
                     'definitions': ['a bull (= male cow) that has had its '
                                   'reproductive organs removed, used in the '
                                   'past for pulling heavy things on farms, or, '
                                   'more generally, any adult of the cattle '
                                   'family'],
                     'domain': [[]],
                     'examples': [[]],
                     'image_links': ['https://dictionary.cambridge.org/images/thumb/ox_noun_002_26064.jpg?version=5.0.275'],
                     'irregular_forms': [['plural oxen']],
                     'labels_and_codes': [['[ C ]']],
                     'level': [[]],
                     'region': [[]],
                     'usage': [[]]}}}


define("bass")

--->   {'bass': {'adjective': {'UK_IPA': [['/beɪs/']],
                            'UK_audio_links': [['https://dictionary.cambridge.org//media/english/uk_pron/u/ukb/ukbar/ukbaroq020.mp3']],
                            'US_IPA': [['/beɪs/']],
                            'US_audio_links': [['https://dictionary.cambridge.org//media/english/us_pron/b/bas/base_/base.mp3']],
                            'alt_terms': [[]],
                            'definitions': ['playing, singing, or producing the '
                                          'lowest range of musical notes'],
                            'domain': [[]],
                            'examples': [['a bass drum/guitar/trombone']],
                            'image_links': [''],
                            'irregular_forms': [[]],
                            'labels_and_codes': [['[ before noun ]']],
                            'level': [[]],
                            'region': [[]],
                            'usage': [[]]},
              'noun': {'UK_IPA': [['/beɪs/'],
                                   ['/beɪs/'],
                                   ['/beɪs/'],
                                   ['/beɪs/'],
                                   ['/bæs/']],
                     'UK_audio_links': [['https://dictionary.cambridge.org//media/english/uk_pron/u/ukb/ukbar/ukbaroq020.mp3'],
                                          ['https://dictionary.cambridge.org//media/english/uk_pron/u/ukb/ukbar/ukbaroq020.mp3'],
                                          ['https://dictionary.cambridge.org//media/english/uk_pron/u/ukb/ukbar/ukbaroq020.mp3'],
                                          ['https://dictionary.cambridge.org//media/english/uk_pron/u/ukb/ukbar/ukbaroq020.mp3'],
                                          ['https://dictionary.cambridge.org//media/english/uk_pron/u/ukb/ukbas/ukbashf020.mp3']],
                     'US_IPA': [['/beɪs/'],
                                   ['/beɪs/'],
                                   ['/beɪs/'],
                                   ['/beɪs/'],
                                   ['/bæs/']],
                     'US_audio_links': [['https://dictionary.cambridge.org//media/english/us_pron/b/bas/base_/base.mp3'],
                                          ['https://dictionary.cambridge.org//media/english/us_pron/b/bas/base_/base.mp3'],
                                          ['https://dictionary.cambridge.org//media/english/us_pron/b/bas/base_/base.mp3'],
                                          ['https://dictionary.cambridge.org//media/english/us_pron/b/bas/base_/base.mp3'],
                                          ['https://dictionary.cambridge.org//media/english/us_pron/b/bas/bass_/bass_02_00.mp3']],
                     'alt_terms': [[], [], [], ['(also bass guitar)'], []],
                     'definitions': ['the lowest range of musical notes, or a '
                                          'man with a singing voice in this range',
                                          'the set of low musical sounds on a radio, '
                                          'music system, etc.',
                                          'a \ndouble bass',
                                          'an electric guitar with four strings that '
                                          'plays very low notes',
                                          'a type of fish found in rivers or the sea '
                                          'whose flesh is eaten as a food'],
                     'domain': [[], [], [], [], []],
                     'examples': [['He sings bass.', "Italy's leading bass"],
                                   ['Turn down the bass.'],
                                   [],
                                   ['He plays bass guitar.'],
                                   ['He launched his little boat to fish for '
                                   'bass.',
                                   'This is served with a striped bass fillet.']],
                     'image_links': ['',
                                          '',
                                          'https://dictionary.cambridge.org/images/thumb/double_noun_002_11343.jpg?version=5.0.275',
                                          'https://dictionary.cambridge.org/images/thumb/bass_noun_004_0248.jpg?version=5.0.275',
                                          'https://dictionary.cambridge.org/images/thumb/bass_noun_002_02737.jpg?version=5.0.275'],
                     'irregular_forms': [['plural basses'],
                                          ['plural basses'],
                                          ['plural basses'],
                                          ['plural basses'],
                                          ['plural bass']],
                     'labels_and_codes': [['[ C or U ]'],
                                          ['[ U ]'],
                                          ['[ C ]'],
                                          ['[ C ]'],
                                          ['[ C ]']],
                     'level': [[], [], [], [], []],
                     'region': [[], [], [], [], []],
                     'usage': [[], [], [], [], []]}}}

```
