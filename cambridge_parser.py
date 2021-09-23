import requests
import bs4


user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}
dict_decoder = {0: "English",
                1: "American",
                2: "Business"}
link_prefix = "https://dictionary.cambridge.org"


def get_tags(block) -> [list, list, list, list, list]:
    """
    :param block:  "span", {"class": "def-info ddef-info"}
    :return: level, labels_and_codes, region, usage, domain
    level - english proficiency level
    labels and codes - labels and codes given by Cambridge
    region - region where the current word is mainly used
    usage - formal/informal/specialized
    domain - domain of usage of word
    """
    def find_all_tags(html_tag: str, params: dict) -> list:
        found_tags = block.find_all(html_tag, params)
        tags = []
        for tag in found_tags:
            if tag is not None:
                tag = tag.text.strip()
                tags.append(tag)
        return tags

    level = find_all_tags("span", {"class": "epp-xref"})
    labels_and_codes = find_all_tags("span", {"class": "gram dgram"})
    region_block = block.find("span", {"class": "lab dlab"})
    if region_block is not None:
        regions = region_block.find_all("span", {"class": "region dregion"})
        region = [item.text.strip() for item in regions if item.text.strip()]
    else:
        region = []
    usage = []
    use_block = block.find_all("span", {"class": "lab dlab"}, [])
    for use in use_block:
        use_parent = use.parent.get("class")
        if not any("var" in x for x in use_parent):
            text_block = use.find_all("span", {"class": "usage dusage"}, [])
            for text in text_block:
                string = text.text.strip()
                usage.append(string)
    domain = find_all_tags("span", {"class": "domain ddomain"})
    return level, labels_and_codes, region, usage, domain


def get_phonetics(header_block, dictionary_index=0):
    """
    :param header_block: header block from the page
    :param dictionary_index:
        * 0 - English dictionary (Also used to search Idioms);
        * 1 - American dictionary;
        * 2 - Business dictionary
    :return: uk_ipa, us_ipa - transcription for given word
    """
    uk_ipa = []
    us_ipa = []
    uk_audio_link = ""
    us_audio_link = ""

    audio_block = header_block.find_all("span", {"class": "daud"})

    for daud in audio_block:
        parent_class = [item.strip().lower() for item in daud.parent.get("class")]
        audio_source = daud.find("source")
        if audio_source is not None:
            audio_source_link = audio_source.get("src", "")
        else:
            audio_source_link = ""

        result_audio_link = f"{link_prefix}/{audio_source_link}" if audio_source_link else ""
        if "uk" in parent_class:
            uk_audio_link = result_audio_link
        elif "us" in parent_class:
            us_audio_link = result_audio_link

    if dictionary_index == 0:
        flag = 0
        # Not so beautiful, but working solution for obtaining IPA
        ipa = header_block.find_all("span", {"class": "pron dpron"})
        for child in ipa:
            if flag == 0:
                if child.parent.get("class") == ["uk", "dpron-i"]:
                    uk_ipa = [child.text.strip()]
                    flag = 1
            elif flag == 1:
                if child.parent.get("class") != ["us", "dpron-i"]:
                    uk_ipa += [child.text.strip()]
                else:
                    us_ipa = [child.text.strip()]
                    flag = 2
            else:
                if child.parent.get("class") is None:
                    us_ipa += [child.text.strip()]
                else:
                    break
    else:
        # Cambridge has different ways of adding IPA to american and english dictionaries
        uk_ipa = []
        us_ipa_block = header_block.find("span", {"class": "pron dpron"})
        us_ipa = [us_ipa_block.text.strip()] if us_ipa_block is not None else []
    return uk_ipa, us_ipa, uk_audio_link, us_audio_link


def concatenate_tags(tag_section, global_level, global_labels_and_codes, global_region, global_usage, global_domain):
    level, labels_and_codes, region, usage, domain = get_tags(tag_section)
    result_word_level = global_level + level
    result_word_labels_and_codes = global_labels_and_codes + labels_and_codes
    result_word_region = global_region + region
    result_word_usage = global_usage + usage
    result_word_domain = global_domain + domain
    return result_word_level, result_word_labels_and_codes, result_word_region,\
           result_word_usage, result_word_domain


def update_word_dict(word_dict, word, pos, definition=None, alt_terms_list=None, sentences=None, level=None,
                     labels_and_codes=None, region=None, usage=None, domain=None, image_link=None, uk_ipa=None,
                     us_ipa=None, uk_audio_link=None, us_audio_link=None):

    none2list = [uk_ipa, us_ipa, domain, sentences, level, region, usage, labels_and_codes, alt_terms_list]
    none2str = [uk_audio_link, us_audio_link, definition, image_link]

    for i in range(len(none2list)):
        if none2list[i] is None:
            none2list[i] = []
    uk_ipa, us_ipa, domain, sentences, level, region, usage, labels_and_codes, alt_terms_list = none2list

    for i in range(len(none2str)):
        if none2str[i] is None:
            none2str[i] = ""
    uk_audio_link, us_audio_link, definition, image_link = none2str

    if word_dict.get(word) is None or word_dict[word].get(pos) is None:
        if word_dict.get(word) is None:
            word_dict[word] = {}
        word_dict[word][pos] = {"definitions": [definition],
                                "alt_terms": [alt_terms_list],
                                "examples": [sentences],
                                "level": [level],
                                "labels_and_codes": [labels_and_codes],
                                "region": [region],
                                "usage": [usage],
                                "domain": [domain],
                                "image_links": [image_link],
                                "UK_IPA": uk_ipa,
                                "US_IPA": us_ipa,
                                "UK_audio_link": uk_audio_link,
                                "US_audio_link": us_audio_link}
    else:
        word_dict[word][pos]["definitions"].append(definition)
        word_dict[word][pos]["alt_terms"].append(alt_terms_list)
        word_dict[word][pos]["examples"].append(sentences)
        word_dict[word][pos]["level"].append(level)
        word_dict[word][pos]["labels_and_codes"].append(labels_and_codes)
        word_dict[word][pos]["region"].append(region)
        word_dict[word][pos]["usage"].append(usage)
        word_dict[word][pos]["domain"].append(domain)
        word_dict[word][pos]["image_links"].append(image_link)


def find_phrasal(word, soup, dictionary_index=0):
    """
    :param word: word to be parse
    :param soup: bs4 soup of the page
    :param dictionary_index:
        * 0 - English dictionary (Also used to search Idioms);
        * 1 - American dictionary;
        * 2 - Business dictionary
    :return: parsed info about phrasal verb / idiom found
    """
    phrasal_idiom_word_info = {}
    phrasal_main_block = soup.find_all("div", {"class": "entry"})
    # if it's not just a word, then current query is either phrasal verb, or idiom
    if not phrasal_main_block:
        # idiom parsing
        idiom_main_block = soup.find("div", {"class": "idiom-block"})
        if idiom_main_block is not None:
            parsed_word = idiom_main_block.find("h2", {"class": "headword"}).text.strip()
            found_definition_block = idiom_main_block.find("div", {"class": "ddef_h"})
            if found_definition_block is not None:
                found_definition_string = found_definition_block.find("div", {'class': "def ddef_d db"})
            else:
                found_definition_string = None
            idiom_definition = "" if found_definition_string is None else found_definition_string.text.strip(": ")

            def_and_sent_block = idiom_main_block.find("span", {"class": "idiom-body didiom-body"})

            # sentence examples
            sentence_block_list = def_and_sent_block.find("div", {"class": "def-body ddef_b"})
            sentence_block_list = [] if sentence_block_list is None else sentence_block_list.find_all(
                "div",
                {"class": "examp dexamp"})
            idiom_sentences = []
            for sent_ex in sentence_block_list:
                idiom_sentences.append(sent_ex.text.strip())
            update_word_dict(phrasal_idiom_word_info, word=parsed_word, pos="idiom", definition=idiom_definition,
                             sentences=idiom_sentences)
            return phrasal_idiom_word_info

    # phrasal verb parsing
    if len(phrasal_main_block) < dictionary_index + 1:
        raise ValueError(f"{dict_decoder[dictionary_index]} dictionary doesn't have word {word}")
    phrasal_main_block = phrasal_main_block[dictionary_index]
    phrasal_header_block = phrasal_main_block.find("div", {"class": "pos-header dpos-h"})
    uk_ipa, us_ipa, uk_audio_link, us_audio_link = get_phonetics(phrasal_header_block, dictionary_index)

    pos_block = phrasal_header_block.find("span", {"class": "pos dpos"})
    pos = "" if pos_block is None else pos_block.text.strip()

    m_level, m_labels_and_codes, m_region, m_usage, m_domain = get_tags(phrasal_header_block)
    parsed_word_block = phrasal_main_block.find("h2", {"class": "headword"})  # tw-bw dhw dpos-h_hw
    if parsed_word_block is None:
        return {}

    parsed_word = parsed_word_block.text.strip()
    for def_and_sent_block in phrasal_main_block.find_all("div", {"class": "def-block ddef_block"}):  # sense-body dsense_b
        # sentence examples
        sentence_block_list = def_and_sent_block.find("div", {"class": "def-body ddef_b"})
        sentence_block_list = [] if sentence_block_list is None else sentence_block_list.find_all("div",
                                                                                                  {"class": "examp dexamp"})
        phrasal_sentences = []
        for sent_ex in sentence_block_list:
            phrasal_sentences.append(sent_ex.text.strip())

        found_definition_block = def_and_sent_block.find("div", {"class": "ddef_h"})
        if found_definition_block is not None:
            phrasal_definition = ""

            alt_terms_list = []
            if found_definition_block is not None:
                found_definition_string = found_definition_block.find("div", {'class': "def ddef_d db"})
                phrasal_definition = "" if found_definition_string is None else found_definition_string.text.strip(
                    ": ")

                alt_terms_list = get_alt_terms(found_definition_block.find_all("span", {"class": "var dvar"}))

                # Gathering specific tags for every word usage
                tag_section = found_definition_block.find("span", {"class": "def-info ddef-info"})
                current_word_level, current_word_labels_and_codes, current_word_region, current_word_usage, current_word_domain = \
                    concatenate_tags(tag_section, m_level, m_labels_and_codes, m_region, m_usage, m_domain)

            update_word_dict(phrasal_idiom_word_info, word=parsed_word, pos=pos, definition=phrasal_definition,
                             alt_terms_list=alt_terms_list, sentences=phrasal_sentences, level=current_word_level,
                             labels_and_codes=current_word_labels_and_codes, region=current_word_region,
                             usage=current_word_usage, domain=current_word_domain, uk_ipa=uk_ipa, us_ipa=us_ipa,
                             uk_audio_link=uk_audio_link, us_audio_link=us_audio_link)
    return phrasal_idiom_word_info


def get_alt_terms(alt_terms_block):
    """
    :param alt_terms_block: = *.find_all("span", {"class": "var dvar"})
    :return:
    """
    alt_terms = []
    for alt_term in alt_terms_block:
        alt_terms.append(alt_term.text.strip())
    return alt_terms


def define(word, dictionary_index=0, headers=headers):
    """
    :param word: word to be parsed
    :param headers: request headers
    :param dictionary_index:
        * 0 - English dictionary (Also used to search Idioms);
        * 1 - American dictionary;
        * 2 - Business dictionary
    :return:
    """
    link = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    # will raise error if headers are None
    page = requests.get(link, headers=headers, timeout=5)
    word_info = {}

    soup = bs4.BeautifulSoup(page.content, "html.parser")
    # Only english dictionary
    # word block which contains definitions for every POS.
    primal_block = soup.find_all("div", {'class': 'pr di superentry'})
    if len(primal_block) >= dictionary_index + 1:
        main_block = primal_block[dictionary_index].find_all("div", {"class": "pr entry-body__el"})
    else:
        raise ValueError(f"{dict_decoder[dictionary_index]} dictionary doesn't have word {word}")

    for entity in main_block:
        header_block = entity.find("div", {"class": "pos-header dpos-h"})
        m_alt_terms_list = get_alt_terms(header_block.find_all("span", {"class": "var dvar"}))

        parsed_word_block = header_block.find("span", {"class": "hw dhw"})

        pos_block = header_block.find("span", {"class": "pos dpos"})
        pos = "" if pos_block is None else pos_block.text.strip()

        uk_ipa, us_ipa, uk_audio_link, us_audio_link = get_phonetics(header_block, dictionary_index)

        # data gathered from the word header
        m_level, m_labels_and_codes, m_region, m_usage, m_domain = get_tags(header_block)

        for def_and_sent_block in entity.find_all("div", {'class': 'def-block ddef_block'}):
            image_section = def_and_sent_block.find("div", {"class": "dimg"})
            image_link = ""
            if image_section is not None:
                image_link_block = image_section.find("amp-img")
                if image_link_block is not None:
                    image_link = link_prefix + image_link_block.get("src", "")

            # sentence examples
            sentence_block_list = def_and_sent_block.find("div", {"class": "def-body ddef_b"})
            sentence_block_list = [] if sentence_block_list is None else sentence_block_list.find_all(
                "div",
                {"class": "examp dexamp"})
            sentences = []

            for item in sentence_block_list:
                sent_ex = item.text.strip()
                sentences.append(sent_ex)

            found_definition_block = def_and_sent_block.find("div", {"class": "ddef_h"})

            definition = ""
            if found_definition_block is not None:
                found_definition_string = found_definition_block.find("div", {'class': "def ddef_d db"})
                definition = "" if found_definition_string is None else found_definition_string.text.strip(": ")

                tag_section = found_definition_block.find("span", {"class": "def-info ddef-info"})

                alt_terms_list = get_alt_terms(found_definition_block.find_all("span", {"class": "var dvar"}))

                # Gathering specific tags for every word usage
                current_word_level, current_word_labels_and_codes, current_word_region, current_word_usage, current_word_domain = \
                    concatenate_tags(tag_section, m_level, m_labels_and_codes, m_region, m_usage, m_domain)

                # Phrase-block checking
                # The reason for this is that on website there are two different tags for phrase-blocks
                phrase_block = found_definition_block.find_parent("div", {"class": "pr phrase-block dphrase-block"})
                if phrase_block is None:
                    phrase_block = found_definition_block.find_parent("div",
                                                                      {"class": "pr phrase-block dphrase-block lmb-25"})
                if phrase_block is not None:
                    phrase_tags_section = phrase_block.find("span", {"class": "phrase-info dphrase-info"})
                    if phrase_tags_section is not None:
                        alt_terms_list += get_alt_terms(phrase_tags_section.find_all("span", {"class": "var dvar"}))
                        current_word_level, current_word_labels_and_codes, current_word_region, current_word_usage, current_word_domain = \
                            concatenate_tags(phrase_tags_section, m_level, m_labels_and_codes, m_region, m_usage, m_domain)
                    parsed_word = phrase_block.find("span",
                                                    {"class": "phrase-title dphrase-title"}).text.strip()
                else:
                    parsed_word = word if parsed_word_block is None else parsed_word_block.text.strip()

            update_word_dict(word_info, word=parsed_word, pos=pos, definition=definition,
                             alt_terms_list=alt_terms_list, sentences=sentences, level=current_word_level,
                             labels_and_codes=current_word_labels_and_codes, region=current_word_region,
                             usage=current_word_usage, domain=current_word_domain, image_link=image_link,
                             uk_ipa=uk_ipa, us_ipa=us_ipa, uk_audio_link=uk_audio_link, us_audio_link=us_audio_link)
    phrasal_word_info = find_phrasal(word, soup, dictionary_index)
    word_info.update(phrasal_word_info)
    return word_info


if __name__ == "__main__":
    from pprint import pprint
    pprint(define("wee"))
