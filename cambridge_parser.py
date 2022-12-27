import bs4
import requests
from typing import Optional, TypedDict
from enum import IntEnum, auto


DEFAULT_REQUESTS_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
LINK_PREFIX = "https://dictionary.cambridge.org"

DEFINITION_T       = str
IMAGE_LINK_T       = str
LEVEL_T            = str
UK_IPA_T           = list[str]
UK_AUDIO_LINKS_T   = list[str]
US_IPA_T           = list[str]
US_AUDIO_LINKS_T   = list[str]
ALT_TERMS_T        = list[str]
DOMAINS_T          = list[str]
EXAMPLES_T         = list[str]
IRREGULAR_FORMS_T  = list[str]
LABELS_AND_CODES_T = list[str] 
REGIONS_T          = list[str]
USAGES_T           = list[str]             

WORD_T = str
POS_T = str

class POSData(TypedDict):
    UK_IPA:           list[UK_IPA_T]
    UK_audio_links:   list[UK_AUDIO_LINKS_T]
    US_IPA:           list[US_IPA_T]
    US_audio_links:   list[US_AUDIO_LINKS_T]
    alt_terms:        list[ALT_TERMS_T]
    definitions:      list[DEFINITION_T]
    domains:          list[DOMAINS_T]
    examples:         list[EXAMPLES_T]
    image_links:      list[IMAGE_LINK_T]
    irregular_forms:  list[IRREGULAR_FORMS_T]
    labels_and_codes: list[LABELS_AND_CODES_T]
    levels:           list[LEVEL_T]
    regions:          list[REGIONS_T]
    usages:           list[USAGES_T]


RESULT_FORMAT = dict[WORD_T, dict[POS_T, POSData]]

class DictionaryVariation(IntEnum):
    English = 0
    American = auto()
    Business = auto()

def get_tags(tags_section: Optional[bs4.Tag]) -> tuple[LEVEL_T, 
                                                       LABELS_AND_CODES_T, 
                                                       REGIONS_T, 
                                                       USAGES_T, 
                                                       DOMAINS_T]:
    def find_tag(html_tag: str, params: dict) -> str:
        nonlocal tags_section

        if tags_section is None:
            return ""

        found_tag = tags_section.find(html_tag, params)
        if found_tag is None:
            return ""

        tag_grandparent = found_tag.parent.parent.get("class")
        # var - var dvar; group - inf-group dinfg
        if not any("var" in x or "group" in x for x in tag_grandparent):
            tag_text = found_tag.text.strip()
            return tag_text
        return ""

    def find_all_tags(html_tag: str, params: dict) -> list[str]:
        nonlocal tags_section

        tags: list[str] = []
        if tags_section is None:
            return tags

        found_tags = tags_section.find_all(html_tag, params)
        for tag in found_tags:
            tag_grandparent = tag.parent.parent.get("class")
            # var - var dvar; group - inf-group dinfg
            if not any("var" in x or "group" in x for x in tag_grandparent):
                tag_text = tag.text.strip()
                if tag_text:
                    tags.append(tag_text)
        return tags

    level            = find_tag(     "span", {"class": "epp-xref"})
    labels_and_codes = find_all_tags("span", {"class": "gram dgram"})
    region           = find_all_tags("span", {"class": "region dregion"})
    usage            = find_all_tags("span", {"class": "usage dusage"})
    domain           = find_all_tags("span", {"class": "domain ddomain"})
    return level, labels_and_codes, region, usage, domain

def get_phonetics(
    header_block: Optional[bs4.Tag], 
    dictionary_index: DictionaryVariation) -> tuple[UK_IPA_T, 
                                                    US_IPA_T, 
                                                    UK_AUDIO_LINKS_T, 
                                                    US_AUDIO_LINKS_T]:
    uk_ipa: UK_IPA_T = []
    us_ipa: US_IPA_T = []
    uk_audio_links: UK_AUDIO_LINKS_T = []
    us_audio_links: US_AUDIO_LINKS_T = []
    if header_block is None:
        return uk_ipa, us_ipa, uk_audio_links, us_audio_links

    audio_block = header_block.find_all("span", {"class": "daud"})
    for daud in audio_block:
        parent_class = [item.strip().lower() for item in daud.parent.get("class")]
        audio_source = daud.find("source")
        if audio_source is None:
            continue
        audio_source_link = audio_source.get("src")
        if not audio_source_link:  # None or empty
            continue

        result_audio_link = f"{LINK_PREFIX}/{audio_source_link}"
        if "uk" in parent_class:
            uk_audio_links.append(result_audio_link)
        elif "us" in parent_class:
            us_audio_links.append(result_audio_link)

    if dictionary_index == DictionaryVariation.English:
        ipa = header_block.find_all("span", {"class": "pron dpron"})
        for child in ipa:
            ipa_parent = child.parent.get("class")
            if ipa_parent is None:
                continue

            if "uk" in ipa_parent:
                uk_ipa.append(child.text.strip())
            elif "us" in ipa_parent:
                us_ipa.append(child.text.strip())
    else:
        # Cambridge has different ways of adding IPA to american and english dictionaries
        uk_ipa = []
        us_ipa_block = header_block.find("span", {"class": "pron dpron"})
        us_ipa = [us_ipa_block.text.strip()] if us_ipa_block is not None else []
    return uk_ipa, us_ipa, uk_audio_links, us_audio_links


def concatenate_tags(tag_section:             Optional[bs4.Tag], 
                     global_level:            LEVEL_T,
                     global_labels_and_codes: LABELS_AND_CODES_T,
                     global_region:           REGIONS_T, 
                     global_usage:            USAGES_T, 
                     global_domain:           DOMAINS_T) -> tuple[LEVEL_T, LABELS_AND_CODES_T, REGIONS_T, USAGES_T, DOMAINS_T]:
    level, labels_and_codes, region, usage, domain = get_tags(tag_section)

    result_level = level if level else global_level
    result_labels_and_codes = global_labels_and_codes + labels_and_codes
    result_word_region = global_region + region
    result_word_usage = global_usage + usage
    result_word_domain = global_domain + domain
    return result_level, result_labels_and_codes, result_word_region, result_word_usage, result_word_domain


def update_word_dict(word_dict:        RESULT_FORMAT,
                     word:             Optional[WORD_T]            =None,
                     pos:              Optional[POS_T]             =None,
                     definition:       Optional[DEFINITION_T]      =None,
                     alt_terms:        Optional[ALT_TERMS_T]       =None, 
                     irregular_forms:  Optional[IRREGULAR_FORMS_T] =None,
                     examples:         Optional[EXAMPLES_T]        =None,
                     level:            Optional[LEVEL_T]           =None,
                     labels_and_codes: Optional[LABELS_AND_CODES_T]=None,
                     regions:          Optional[REGIONS_T]         =None,
                     usages:           Optional[USAGES_T]          =None,
                     domains:          Optional[DOMAINS_T]         =None,
                     image_link:       Optional[IMAGE_LINK_T]      =None,
                     uk_ipa:           Optional[UK_IPA_T]          =None,
                     us_ipa:           Optional[US_IPA_T]          =None,
                     uk_audio_links:   Optional[UK_AUDIO_LINKS_T]  =None,
                     us_audio_links:   Optional[US_AUDIO_LINKS_T]  =None):
    
    word = word if word is not None else ""
    pos = pos if pos is not None else ""

    if word_dict.get(word) is None:
        word_dict[word] = {}

    if word_dict[word].get(pos) is None:
        word_dict[word][pos] = {"definitions":      [],
                                "examples":         [],
                                "UK_IPA":           [],
                                "US_IPA":           [],
                                "UK_audio_links":   [],
                                "US_audio_links":   [],
                                "image_links":      [],
                                "alt_terms":        [],
                                "irregular_forms":  [],
                                "levels":           [],
                                "labels_and_codes": [],
                                "regions":          [],
                                "usages":           [],
                                "domains":          []}
    word_dict[word][pos]["definitions"]     .append(definition       if definition        is not None else "")
    word_dict[word][pos]["levels"]          .append(level            if level             is not None else "")
    word_dict[word][pos]["image_links"]     .append(image_link       if image_link        is not None else "")
    word_dict[word][pos]["UK_IPA"]          .append(uk_ipa           if uk_ipa            is not None else [])
    word_dict[word][pos]["US_IPA"]          .append(us_ipa           if us_ipa            is not None else [])
    word_dict[word][pos]["UK_audio_links"]  .append(uk_audio_links   if uk_audio_links    is not None else [])
    word_dict[word][pos]["US_audio_links"]  .append(us_audio_links   if us_audio_links    is not None else [])
    word_dict[word][pos]["examples"]        .append(examples         if examples          is not None else [])
    word_dict[word][pos]["alt_terms"]       .append(alt_terms        if alt_terms         is not None else [])
    word_dict[word][pos]["irregular_forms"] .append(irregular_forms  if irregular_forms   is not None else [])
    word_dict[word][pos]["labels_and_codes"].append(labels_and_codes if labels_and_codes  is not None else [])
    word_dict[word][pos]["regions"]         .append(regions          if regions           is not None else [])
    word_dict[word][pos]["usages"]          .append(usages           if usages            is not None else [])
    word_dict[word][pos]["domains"]         .append(domains          if domains           is not None else [])

def get_irregular_forms(word_header_block: Optional[bs4.Tag]) -> IRREGULAR_FORMS_T:
    forms: IRREGULAR_FORMS_T = []
    if word_header_block is None:
        return forms

    all_irreg_forms_block = word_header_block.find("span", {"class": "irreg-infls dinfls"})
    if all_irreg_forms_block is None:
        return forms

    for irreg_form_block in all_irreg_forms_block:
        text = []
        for containing_tag in (x for x in irreg_form_block if isinstance(x, bs4.Tag)):
            tag_class = containing_tag.get("class")
            if tag_class is not None and not any("dpron" in x for x in tag_class):
                text.append(containing_tag.text.strip())
        if (joined_text := " ".join(text)):
            forms.append(joined_text)
    return forms


def get_alt_terms(word_header_block: Optional[bs4.Tag]) -> ALT_TERMS_T:
    alt_terms: ALT_TERMS_T = []
    if word_header_block is None:
        return alt_terms

    var_block = word_header_block.find_all("span", {"class": "var dvar"})
    var_block.extend(word_header_block.find_all("span", {"class": "spellvar dspellvar"}))
    for alt_term in var_block:
        alt_terms.append(alt_term.text.strip())
    return alt_terms


def define(word: str, 
           dictionary_index: DictionaryVariation=DictionaryVariation.English, 
           request_headers: Optional[dict]=None, 
           timeout:float=5.0) -> RESULT_FORMAT:
    if request_headers is None:
        request_headers = DEFAULT_REQUESTS_HEADERS

    link = f"{LINK_PREFIX}/dictionary/english/{word}"
    # will raise error if request_headers are None
    page = requests.get(link, headers=request_headers, timeout=timeout)

    word_info: RESULT_FORMAT = {}

    soup = bs4.BeautifulSoup(page.content, "html.parser")
    # Only english dictionary
    # word block which contains definitions for every POS_T.
    primal_block = soup.find_all("div", {'class': 'pr di superentry'})
    if len(primal_block) <= dictionary_index:
        return {}

    main_block = primal_block[dictionary_index].find_all("div", {"class": "pr entry-body__el"})
    main_block.extend(primal_block[dictionary_index].find_all("div", {"class": "pv-block"}))
    main_block.extend(primal_block[dictionary_index].find_all("div", {"class": "pr idiom-block"}))

    for entity in main_block:
        header_block = entity.find("span", {"class": "di-info"})
        if header_block is None:
            header_block = entity.find("div", {"class": "pos-header dpos-h"})
        pos_alt_terms_list = get_alt_terms(header_block)
        pos_irregular_forms_list = get_irregular_forms(header_block)

        parsed_word_block = entity.find("h2", {"class": "headword"})
        if parsed_word_block is None:
            parsed_word_block = header_block.find("span", {"class": "hw dhw"}) if header_block is not None else None
        header_word = parsed_word_block.text.strip() if parsed_word_block is not None else ""

        pos_block = header_block.find_all("span", {"class": "pos dpos"}) if header_block is not None else []
        pos = "idiom" if not pos_block else ",".join((pos_section.text.strip() for pos_section in pos_block))

        uk_ipa, us_ipa, uk_audio_links, us_audio_links = get_phonetics(header_block, dictionary_index)

        # data gathered from the word header
        pos_level, pos_labels_and_codes, pos_regions, pos_usages, pos_domains = get_tags(header_block)

        for def_and_sent_block in entity.find_all("div", {'class': 'def-block ddef_block'}):
            definition:                    DEFINITION_T       = ""
            alt_terms:                     ALT_TERMS_T        = []
            irregular_forms:               IRREGULAR_FORMS_T  = []
            current_word_level:            LEVEL_T            = ""
            current_word_labels_and_codes: LABELS_AND_CODES_T = []
            current_word_regions:          REGIONS_T          = []
            current_word_usages:           USAGES_T           = []
            current_word_domains:          DOMAINS_T          = []

            current_def_block_word = header_word

            image_section = def_and_sent_block.find("div", {"class": "dimg"})
            image_link = ""
            if image_section is not None:
                image_link_block = image_section.find("amp-img")
                if image_link_block is not None:
                    image_link = LINK_PREFIX + image_link_block.get("src", "")

            # sentence examples
            sentence_block_list = def_and_sent_block.find("div", {"class": "def-body ddef_b"})
            sentence_block_list = [] if sentence_block_list is None else sentence_block_list.find_all(
                "div",
                {"class": "examp dexamp"})
            examples = []
            for item in sentence_block_list:
                sent_ex = item.text.strip()
                examples.append(sent_ex)

            found_definition_block = def_and_sent_block.find("div", {"class": "ddef_h"})

            if found_definition_block is not None:
                found_definition_string = found_definition_block.find("div", {'class': "def ddef_d db"})
                definition = "" if found_definition_string is None else found_definition_string.text.strip(": ")

                # Gathering specific tags for every word usage
                tag_section = found_definition_block.find("span", {"class": "def-info ddef-info"})
                current_word_level, current_word_labels_and_codes, current_word_regions, current_word_usages, current_word_domains = \
                    concatenate_tags(tag_section, pos_level, pos_labels_and_codes, pos_regions, pos_usages, pos_domains)

                alt_terms = get_alt_terms(found_definition_block)
                irregular_forms = get_irregular_forms(found_definition_block)

                # Phrase-block check
                # The reason for this is that on website there are two different tags for phrase-blocks
                phrase_block = found_definition_block.find_parent("div",
                                                                  {"class": "pr phrase-block dphrase-block"})
                if phrase_block is None:
                    phrase_block = found_definition_block.find_parent("div",
                                                                      {"class": "pr phrase-block dphrase-block lmb-25"})
                if phrase_block is not None:
                    phrase_tags_section = phrase_block.find("span",
                                                            {"class": "phrase-info dphrase-info"})
                    if phrase_tags_section is not None:
                        alt_terms += get_alt_terms(phrase_tags_section)
                        irregular_forms += get_irregular_forms(phrase_tags_section)

                        current_word_level, current_word_labels_and_codes, current_word_regions, current_word_usages, current_word_domains = \
                            concatenate_tags(phrase_tags_section,
                                             current_word_level,
                                             current_word_labels_and_codes,
                                             current_word_regions,
                                             current_word_usages,
                                             current_word_domains)
                    current_def_block_word = phrase_block.find("span",
                                                               {"class": "phrase-title dphrase-title"}).text.strip()

            update_word_dict(word_info,
                             word=current_def_block_word,
                             pos=pos,
                             definition=definition,
                             alt_terms=pos_alt_terms_list + alt_terms,
                             irregular_forms=irregular_forms + pos_irregular_forms_list,
                             examples=examples,
                             level=current_word_level,
                             labels_and_codes=current_word_labels_and_codes,
                             regions=current_word_regions,
                             usages=current_word_usages,
                             domains=current_word_domains,
                             image_link=image_link,
                             uk_ipa=uk_ipa,
                             us_ipa=us_ipa,
                             uk_audio_links=uk_audio_links,
                             us_audio_links=us_audio_links)
    return word_info


if __name__ == "__main__":
    from pprint import pprint

    pprint(define("reconnaissance", dictionary_index=DictionaryVariation.English, timeout=5.3))
