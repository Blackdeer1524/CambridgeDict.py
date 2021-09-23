# CambridgeDict.py
Python HTML parser for [Cambridge dictionary](https://dictionary.cambridge.org/).

* [x] English, american and business dictionaries 

# Requirements
* requests
* beautifulsoup4

# Return pattern
```python
{word: {'noun': {'UK_IPA': [UK_IPA],
                 'UK_audio_link': UK_audio_link,
                 'US_IPA': [US_IPA],
                 'US_audio_link': US_audio_link,
                 'alt_terms': [[alt_terms_1], ..., [alt_terms_N]],
                 'definitions': [definition_1, ..., definition_N],
                 'domain': [[domains_1], ..., [domains_N]],
                 'examples': [[1-st sentence example for the 1-st def, ..., N-th sentence example for the 1-st def],
                              ...
                              [1-st sentence example for the N-th def, ..., N-th sentence example for the N-th def]],
                 'images': [dict_image_link_1, ..., dict_image_link_n],
                 'labels_and_codes': [labels_and_codes_1, ..., labels_and_codes_N],
                 'level': [[level_1], ..., [level_N]],
                 'region': [[region_1], ..., [region_N]],
                 'usage': [[usage_1], ..., [usage_N]]},
       {'verb': {'UK_IPA': [UK_IPA],
                 'UK_audio_link': UK_audio_link,
                 'US_IPA': [US_IPA],
                 'US_audio_link': US_audio_link,
                 'alt_terms': [[alt_terms_1], ..., [alt_terms_N]],
                 'definitions': [definition_1, ..., definition_N],
                 'domain': [[domains_1], ..., [domains_N]],
                 'examples': [[1-st sentence example for the 1-st def, ..., N-th sentence example for the 1-st def],
                              ...
                              [1-st sentence example for the N-th def, ..., N-th sentence example for the N-th def]],
                 'images': [dict_image_link_1, ..., dict_image_link_n],
                 'labels_and_codes': [labels_and_codes_1, ..., labels_and_codes_N],
                 'level': [[level_1], ..., [level_N]],
                 'region': [[region_1], ..., [region_N]],
                 'usage': [[usage_1], ..., [usage_N]]},
       ...
                  
}}}
```
# Example

```python
parse('insult', dictionary_index=0)

--> {'insult': {'noun': {'UK_IPA': ['/ˈɪn.sʌlt/'],
                           'UK_audio_link': 'https://dictionary.cambridge.org//media/english/uk_pron/u/uki/ukins/ukinstr024.mp3',
                           'US_IPA': ['/ˈɪn.sʌlt/'],
                           'US_audio_link': 'https://dictionary.cambridge.org//media/english/us_pron/i/ins/insul/insult_01_01.mp3',
                           'alt_terms': [[]],
                           'definitions': ['an offensive remark or action'],
                           'domain': [[]],
                           'examples': [['She made several insults about my '
                                         'appearance.',
                                         "The steelworkers' leader rejected the two "
                                         'percent pay rise saying it was an insult '
                                         'to the profession.',
                                         'The instructions are so easy they are an '
                                         'insult to your intelligence (= they seem '
                                         'to suggest you are not clever if you need '
                                         'to use them).']],
                           'image_links': [''],
                           'labels_and_codes': [['[ C ]']],
                           'level': [['B2']],
                           'region': [[]],
                           'usage': [[]]},
                  'verb': {'UK_IPA': ['/ɪnˈsʌlt/'],
                           'UK_audio_link': 'https://dictionary.cambridge.org//media/english/uk_pron/u/uki/ukins/ukinstr025.mp3',
                           'US_IPA': ['/ɪnˈsʌlt/'],
                           'US_audio_link': 'https://dictionary.cambridge.org//media/english/us_pron/i/ins/insul/insult_01_00.mp3',
                           'alt_terms': [[]],
                           'definitions': ['to say or do something to someone that '
                                           'is rude or offensive'],
                           'domain': [[]],
                           'examples': [['First he drank all my wine and then he '
                                         'insulted all my friends.']],
                           'image_links': [''],
                           'labels_and_codes': [['[ T ]']],
                           'level': [['B2']],
                           'region': [[]],
                           'usage': [[]]}}}


```
