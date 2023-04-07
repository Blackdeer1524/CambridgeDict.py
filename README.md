# CambridgeDict.py
Python HTML parser for [Cambridge dictionary](https://dictionary.cambridge.org/).

Supports mono- and bilingual dictionaries


# Installation
```sh
pip install requests
pip install beautifulsoup4
```

# Return pattern

Returns a **list** of found definitions where each entry corresponds to a different dictionary on a page. 
For example, if one needs to extract data for word *bass* from monolingual english dictionary, on page
there will be 2 sections: 
1. Without annotation 
2. Intermediate English (former American dictionary)

Then each entry on the list will correspiond to each of these dictionaries. 

Note: length of the result is not predetermined as there may not be Intermidiate English dictionary section 
(or its analogs for bilingual dictionaries).

```python
[
{<word>: [
    {"POS": [block pos 1, ..., block pos M],
     "data": {
         'definitions': [1-st definition, ..., N-th definition],
         # one string per definition
         'definitions_translations': [1-st definition translation, ..., N-th definition translation]
         'image_links':              [image link for the 1-st definition, ..., image link for the N-th definition],
         'levels':                   [level for the 1-st definition, ..., level for the N-th definition],
         # multiple strings per definition
         'UK_IPA':                [[1-st UK IPA for the 1-st definition, ...],
                                   ...
                                   [1-st UK IPA for the N-th definition, ...]],
         'US_IPA':                [[1-st US IPA for the 1-st definition, ...],
                                   ...
                                   [1-st US IPA for the N-th definition, ...]],
         'UK_audio_links':        [[1-st uk audio link for the 1-st definition, ...],
                                   ...
                                   [1-st uk audio link for the N-th definition, ...]],
         'US_audio_links':        [[1-st us audio link for the 1-st definition, ...],
                                   ...
                                   [1-st us audio link for the N-th definition, ...]],
         'examples':              [[1-st sentence example for the 1-st definition, ...],
                                   ...
                                   [1-st sentence example for the N-th definition, ...]],
         'examples_translations': [[translation for the 1-st sentence example for the 1-st definition, ...],
                                   ...
                                   [translation for the 1-st sentence example for the N-th definition, ...]],
         'alt_terms':             [[1-st alternative term for the 1-st definition, ...],
                                   ...
                                   [1-st alternative term for the N-th definition, ...]],
         'irregular_forms':       [[1-st irregular form for the 1-st definition, ...],
                                   ...
                                   [1-st irregular form for the N-th definition, ...]],
         'domains':               [[1-st domain for the 1-st definition, ...],
                                   ...
                                   [1-st domain for the N-th definition, ...]],,
         'labels_and_codes':      [[1-st labels & codes for the 1-st definition, ...],
                                   ...
                                   [1-st labels & codes for the N-th definition, ...]],
         'regions':               [[1-st region for the 1-st definition, ...],
                                   ...
                                   [1-st region for the N-th definition, ...]],
         'usages':                [[1-st usage for the 1-st definition, ...],
                                    ...
                                    [1-st usage for the N-th definition, ...]]}}
    ...
    ]
    ...
},
...
]
```

# Examples

```python
define(word="more", 
       bilingual_vairation="")
[{'more': [{'POS': ['determiner', 'pronoun', 'adverb'],
            'data': {'UK_IPA': [['/mɔːr/'], ['/mɔːr/'], ['/mɔːr/']],
                     'UK_audio_links': [['https://dictionary.cambridge.org//media/english/uk_pron/u/ukm/ukmor/ukmorda003.mp3'],
                                        ['https://dictionary.cambridge.org//media/english/uk_pron/u/ukm/ukmor/ukmorda003.mp3'],
                                        ['https://dictionary.cambridge.org//media/english/uk_pron/u/ukm/ukmor/ukmorda003.mp3']],
                     'US_IPA': [['/mɔːr/'], ['/mɔːr/'], ['/mɔːr/']],
                     'US_audio_links': [['https://dictionary.cambridge.org//media/english/us_pron/m/mor/more_/more.mp3'],
                                        ['https://dictionary.cambridge.org//media/english/us_pron/m/mor/more_/more.mp3'],
                                        ['https://dictionary.cambridge.org//media/english/us_pron/m/mor/more_/more.mp3']],
                     'alt_terms': [[], [], []],
                     'definitions': ['a larger or extra number or amount',
                                     'used to form the comparative of many '
                                     'adjectives and adverbs',
                                     'used to emphasize the large size of '
                                     'something'],
                     'definitions_translations': ['', '', ''],
                     'domains': [[], [], []],
                     'examples': [['Would you like some more food?',
                                   "The doctors can't cope with any more "
                                   'patients.',
                                   'Add some more cream to the sauce.',
                                   'You need to listen more and talk less!',
                                   'More people live in the capital than in '
                                   'the whole of the rest of the country.',
                                   'We spent more time on the last job than '
                                   'usual.',
                                   'The noise was more than I could bear.',
                                   "It was a hundred times more fun than I'd "
                                   'expected.',
                                   "She's more of a poet than a novelist.",
                                   'Bring as much food as you can - the more, '
                                   'the better.'],
                                  ["She couldn't be more beautiful.",
                                   "Let's find a more sensible way of doing "
                                   'it.',
                                   "You couldn't be more wrong.",
                                   'He finds physics far/much more difficult '
                                   'than other science subjects.',
                                   'Play that last section more passionately.'],
                                  ['More than 20,000 demonstrators crowded '
                                   'into the square.']],
                     'examples_translations': [['',
                                                '',
                                                '',
                                                '',
                                                '',
                                                '',
                                                '',
                                                '',
                                                '',
                                                ''],
                                               ['', '', '', '', ''],
                                               ['']],
                     'image_links': ['', '', ''],
                     'irregular_forms': [[], [], []],
                     'labels_and_codes': [[], [], []],
                     'levels': ['A1', 'A1', ''],
                     'regions': [[], [], []],
                     'usages': [[], [], []]}}],
  'more and more': [{'POS': ['determiner', 'pronoun', 'adverb'],
                     'data': {'UK_IPA': [['/mɔːr/']],
                              'UK_audio_links': [['https://dictionary.cambridge.org//media/english/uk_pron/u/ukm/ukmor/ukmorda003.mp3']],
                              'US_IPA': [['/mɔːr/']],
                              'US_audio_links': [['https://dictionary.cambridge.org//media/english/us_pron/m/mor/more_/more.mp3']],
                              'alt_terms': [[]],
                              'definitions': ['increasingly'],
                              'definitions_translations': [''],
                              'domains': [[]],
                              'examples': [['It gets more and more difficult '
                                            'to understand what is going on.']],
                              'examples_translations': [['']],
                              'image_links': [''],
                              'irregular_forms': [[]],
                              'labels_and_codes': [[]],
                              'levels': ['B2'],
                              'regions': [[]],
                              'usages': [[]]}}],
  'the more...the more/less': [{'POS': ['determiner', 'pronoun', 'adverb'],
                                'data': {'UK_IPA': [['/mɔːr/']],
                                         'UK_audio_links': [['https://dictionary.cambridge.org//media/english/uk_pron/u/ukm/ukmor/ukmorda003.mp3']],
                                         'US_IPA': [['/mɔːr/']],
                                         'US_audio_links': [['https://dictionary.cambridge.org//media/english/us_pron/m/mor/more_/more.mp3']],
                                         'alt_terms': [[]],
                                         'definitions': ['used to say that '
                                                         'when an action or '
                                                         'event continues, '
                                                         'there will be a '
                                                         'particular result'],
                                         'definitions_translations': [''],
                                         'domains': [[]],
                                         'examples': [['The more he drank, the '
                                                       'more violent he '
                                                       'became.']],
                                         'examples_translations': [['']],
                                         'image_links': [''],
                                         'irregular_forms': [[]],
                                         'labels_and_codes': [[]],
                                         'levels': [''],
                                         'regions': [[]],
                                         'usages': [[]]}}]},
 {'more': [{'POS': ['adjective', 'adverb'],
            'data': {'UK_IPA': [[], []],
                     'UK_audio_links': [[], []],
                     'US_IPA': [['/mɔr, moʊr/'], ['/mɔr, moʊr/']],
                     'US_audio_links': [['https://dictionary.cambridge.org//media/english/us_pron/m/mor/more_/more.mp3'],
                                        ['https://dictionary.cambridge.org//media/english/us_pron/m/mor/more_/more.mp3']],
                     'alt_terms': [[], []],
                     'definitions': ['a larger or extra number or amount (of); '
                                     'comparative ofmany or much',
                                     'More is used to form the comparative of '
                                     'many adjectives and adverbs'],
                     'definitions_translations': ['', ''],
                     'domains': [[], []],
                     'examples': [['You need to listen more and talk less.',
                                   'There were no more seats on the bus, so we '
                                   'had to stand.',
                                   'DisneyWorld was more fun than I expected.',
                                   'Would you play the song once more (= '
                                   'again)?'],
                                  ['You couldn’t be more wrong.',
                                   'He finds physics much more difficult than '
                                   'biology.']],
                     'examples_translations': [['', '', '', ''], ['', '']],
                     'image_links': ['', ''],
                     'irregular_forms': [[], []],
                     'labels_and_codes': [[], []],
                     'levels': ['', ''],
                     'regions': [[], []],
                     'usages': [[], []]}}]}]

define(word="bass", 
       bilingual_vairation="chinese-traditional")
[{'bass': [{'POS': ['noun'],
            'data': {'UK_IPA': [['/beɪs/'], ['/beɪs/'], ['/beɪs/'], ['/beɪs/']],
                     'UK_audio_links': [['https://dictionary.cambridge.org//media/english-chinese-traditional/uk_pron/u/ukb/ukbar/ukbaroq020.mp3'],
                                        ['https://dictionary.cambridge.org//media/english-chinese-traditional/uk_pron/u/ukb/ukbar/ukbaroq020.mp3'],
                                        ['https://dictionary.cambridge.org//media/english-chinese-traditional/uk_pron/u/ukb/ukbar/ukbaroq020.mp3'],
                                        ['https://dictionary.cambridge.org//media/english-chinese-traditional/uk_pron/u/ukb/ukbar/ukbaroq020.mp3']],
                     'US_IPA': [['/beɪs/'], ['/beɪs/'], ['/beɪs/'], ['/beɪs/']],
                     'US_audio_links': [['https://dictionary.cambridge.org//media/english-chinese-traditional/us_pron/b/bas/base_/base.mp3'],
                                        ['https://dictionary.cambridge.org//media/english-chinese-traditional/us_pron/b/bas/base_/base.mp3'],
                                        ['https://dictionary.cambridge.org//media/english-chinese-traditional/us_pron/b/bas/base_/base.mp3'],
                                        ['https://dictionary.cambridge.org//media/english-chinese-traditional/us_pron/b/bas/base_/base.mp3']],
                     'alt_terms': [[], [], [], ['(also bass guitar)']],
                     'definitions': ['the lowest range of musical notes, or a '
                                     'man with a singing voice in this range',
                                     'the set of low musical sounds on a '
                                     'radio, music system, etc.',
                                     'a double bass',
                                     'an electric guitar with four strings '
                                     'that plays very low notes'],
                     'definitions_translations': ['低音部；男低音',
                                                  '低音；低音鍵',
                                                  '低音提琴（同 double bass）',
                                                  '低音吉他'],
                     'domains': [[], [], [], []],
                     'examples': [['He sings bass.', "Italy's leading bass"],
                                  ['Turn down the bass.'],
                                  [],
                                  ['He plays bass guitar.']],
                     'examples_translations': [['他唱男低音。', '義大利頭號男低音'],
                                               ['把低音調低。'],
                                               [],
                                               ['他彈低音吉他。']],
                     'image_links': ['', '', '', ''],
                     'irregular_forms': [['plural basses'],
                                         ['plural basses'],
                                         ['plural basses'],
                                         ['plural basses']],
                     'labels_and_codes': [['[ C or U ]'],
                                          ['[ U ]'],
                                          ['[ C ]'],
                                          ['[ C ]']],
                     'levels': ['', '', '', ''],
                     'regions': [[], [], [], []],
                     'usages': [[], [], [], []]}},
           {'POS': ['adjective'],
            'data': {'UK_IPA': [['/beɪs/']],
                     'UK_audio_links': [['https://dictionary.cambridge.org//media/english-chinese-traditional/uk_pron/u/ukb/ukbar/ukbaroq020.mp3']],
                     'US_IPA': [['/beɪs/']],
                     'US_audio_links': [['https://dictionary.cambridge.org//media/english-chinese-traditional/us_pron/b/bas/base_/base.mp3']],
                     'alt_terms': [[]],
                     'definitions': ['playing, singing, or producing the '
                                     'lowest range of musical notes'],
                     'definitions_translations': ['低音的'],
                     'domains': [[]],
                     'examples': [['a bass drum/guitar/trombone']],
                     'examples_translations': [['低音鼓／吉他／長號']],
                     'image_links': [''],
                     'irregular_forms': [[]],
                     'labels_and_codes': [['[ before noun ]']],
                     'levels': [''],
                     'regions': [[]],
                     'usages': [[]]}},
           {'POS': ['noun'],
            'data': {'UK_IPA': [['/bæs/']],
                     'UK_audio_links': [['https://dictionary.cambridge.org//media/english-chinese-traditional/uk_pron/u/ukb/ukbas/ukbashf020.mp3']],
                     'US_IPA': [['/bæs/']],
                     'US_audio_links': [['https://dictionary.cambridge.org//media/english-chinese-traditional/us_pron/b/bas/bass_/bass_02_00.mp3']],
                     'alt_terms': [[]],
                     'definitions': ['a type of fish found in rivers or the '
                                     'sea'],
                     'definitions_translations': ['鱸魚'],
                     'domains': [[]],
                     'examples': [[]],
                     'examples_translations': [[]],
                     'image_links': [''],
                     'irregular_forms': [['plural bass']],
                     'labels_and_codes': [['[ C ]']],
                     'levels': [''],
                     'regions': [[]],
                     'usages': [[]]}}]}]
```
