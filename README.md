# CambridgeDict.py
Python HTML parser for [Cambridge dictionary](https://dictionary.cambridge.org/).

## Supports
* [x] English, american and business dictionaries 
* [x] Phrasal verbs
* [x] Idioms

# Requirements
* requests
* beautifulsoup4

# Return pattern
```python
{word: {'noun': {'UK IPA': [noun_uk_ipa],
                 'US IPA': [noun_us_ipa],
                 'definitions': [definiton_1, ..., definition_N],
                 'domain': [[domains_1, ..., domains_N],
                 'examples': [[1-st sentence example for the 1-st def, ..., N-th sentence example for the 1-st def],
                              ...
                              [1-st sentence example for the N-th def, ..., N-th sentence example for the N-th def]],
                 'labels_and_codes': [labels_and_codes_1, ..., labels_and_codes_N],
                 'level': [level_1, ..., level_N],
                 'region': [region_1, ..., region_N],
                 'usage': [usage_1, ..., usage_N]},
       {'verb': {'UK IPA': [verb_uk_ipa],
                 'US IPA': [verb_us_ipa],
                 'definitions': [definiton_1, ..., definition_N],
                 'domain': [[domains_1, ..., domains_N],
                 'examples': [[1-st sentence example for the 1-st def, ..., N-th sentence example for the 1-st def],
                              ...
                              [1-st sentence example for the N-th def, ..., N-th sentence example for the N-th def]],
                 'labels_and_codes': [labels_and_codes_1, ..., labels_and_codes_N],
                 'level': [level_1, ..., level_N],
                 'region': [region_1, ..., region_N],
                 'usage': [usage_1, ..., usage_N]},
       ...
                  
}}}
```
# Example

```python
parse('insult', dictionary_index=0)

--> {'insult': {'noun': {'UK IPA': ['/ˈɪn.sʌlt/'],
                         'US IPA': ['/ˈɪn.sʌlt/'],
                         'definition': ['an offensive remark or action: '],
                         'domain': [['']],
                         'examples': [['She made several insults about my '
                                       'appearance.',
                                       "The steelworkers' leader rejected the two "
                                       'percent pay rise saying it was an insult '
                                       'to the profession.',
                                       'The instructions are so easy they are an '
                                       'insult to your intelligence (= they seem '
                                       'to suggest you are not clever if you need '
                                       'to use them).']],
                         'labels_and_codes': [['[ C ]']],
                         'level': [['B2']],
                         'region': [['']],
                         'usage': [['']]},
                'verb': {'UK IPA': ['/ɪnˈsʌlt/'],
                         'US IPA': ['/ɪnˈsʌlt/'],
                         'definition': ['to say or do something to someone that is '
                                        'rude or offensive: '],
                         'domain': [['']],
                         'examples': [['First he drank all my wine and then he '
                                       'insulted all my friends.']],
                         'labels_and_codes': [['[ T ]']],
                         'level': [['B2']],
                         'region': [['']],
                         'usage': [['']]}}}
```
* UK/US IPA - transcription for given word  
* domain - domain of usage of word
* definitions - definitions of word for current part of speach
* examples - sentence examples
* labels and codes - [labels and codes](https://dictionary.cambridge.org/help/codes.html) given by Cambridge
* level - english proficiency level
* region - region where the current word is mainly used
* usage - formal/informal/specialized

# Known issues
Programm will raise error if:
* The phrasal verb is on the same page as the same noun-word (for example, [`make up`](https://dictionary.cambridge.org/dictionary/english/make-up))
