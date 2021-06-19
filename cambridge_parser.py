import requests
import bs4


user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}
dict_decoder = {0: "English",
                1: "American",
                2: "Business"}


def get_labels(block):
    """
    :param block:  "span", {"class": "def-info ddef-info"}
    :return: level, labels_and_codes, region, usage, domain
    level - english proficiency level
    labels and codes - labels and codes given by Cambridge
    region - region where the current word is mainly used
    usage - formal/informal/specialized
    domain - domain of usage of word
    """
    level = block.find("span", {"class": "epp-xref"})
    level = level.text if level is not None else ""

    labels_and_codes = block.find("span", {"class": "gram dgram"})
    labels_and_codes = labels_and_codes.text if labels_and_codes is not None else ""

    region = block.find("span", {"class": "region dregion"})
    region = region.text if region is not None else ""

    usage = block.find("span", {"class": "usage dusage"})
    usage = usage.text if usage is not None else ""

    domain = block.find("span", {"class": "domain ddomain"})
    domain = domain.text if domain is not None else ""
    return level, labels_and_codes, region, usage, domain


def tag_concatenation(tag_1, tag_2):
    if tag_1 == "" and tag_2 == "":
        return [""]
    if tag_1 == "":
        return [tag_2]
    if tag_2 == "":
        return [tag_1]
    return [tag_1] + [tag_2]


def get_phonetics(header_block, dictionary_index=0):
    """
    :param header_block: header block from the page
    :param dictionary_index:
        * 0 - English dictionary (Also used to search Idioms);
        * 1 - American dictionary;
        * 2 - Business dictionary
    :return: uk_ipa, us_ipa - transcription for given word
    """
    uk_ipa = [""]
    us_ipa = [""]
    if dictionary_index % 2 == 0:
        flag = 0
        # Not so beautiful, but working solution for obtaining IPA
        ipa = header_block.find_all("span", {"class": "pron dpron"})
        for child in ipa:
            if flag == 0:
                if child.parent.get("class") == ["uk", "dpron-i"]:
                    uk_ipa = [child.text]
                    flag = 1
            elif flag == 1:
                if child.parent.get("class") != ["us", "dpron-i"]:
                    uk_ipa += [child.text]
                else:
                    us_ipa = [child.text]
                    flag = 2
            else:
                if child.parent.get("class") is None:
                    us_ipa += [child.text]
                else:
                    break
    else:
        # Cambridge has different ways of adding IPA to american and english dictionaries
        uk_ipa = [""]
        us_ipa = [header_block.find("span", {"class": "pron dpron"}).text]
    return uk_ipa, us_ipa


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
    if len(phrasal_main_block) == 0:
        # idiom parsing
        idiom_main_block = soup.find("div", {"class": "idiom-block"})
        parsed_word = idiom_main_block.find("h2", {"class": "headword"}).text
        idiom_definition_found_1 = idiom_main_block.find("div", {"class": "ddef_h"})
        if idiom_definition_found_1 is not None:
            idiom_definition_found_2 = idiom_definition_found_1.find("div", {'class': "def ddef_d db"})
        else:
            idiom_definition_found_2 = None
        idiom_definition = "" if idiom_definition_found_2 is None else idiom_definition_found_2.text

        def_block = idiom_main_block.find("span", {"class": "idiom-body didiom-body"})

        # sentence examples
        sentence_block_list = def_block.find("div", {"class": "def-body ddef_b"})
        sentence_block_list = [] if sentence_block_list is None else sentence_block_list.find_all(
            "div",
            {"class": "examp dexamp"})
        idiom_sentences = []
        if len(sentence_block_list) != 0:
            for item in sentence_block_list:
                sent_ex = item.text.strip()
                idiom_sentences.append(sent_ex)
        phrasal_idiom_word_info[parsed_word] = {}
        phrasal_idiom_word_info[parsed_word]["idiom"] = {"definitions": [idiom_definition], "examples": [idiom_sentences],
                                                   "level": [[""]],
                                                   "labels_and_codes": [[""]],
                                                   "region": [[""]],
                                                   "usage": [[""]],
                                                   "domain": [[""]],
                                                   "UK IPA": [""],
                                                   "US IPA": [""]}
        return phrasal_idiom_word_info
    else:
        # phrasal verb parsing
        if len(phrasal_main_block) < dictionary_index + 1:
            raise ValueError(f"{dict_decoder[dictionary_index]} dictionary doesn't have word {word}")
        phrasal_main_block = phrasal_main_block[dictionary_index]
        phrasal_header_block = phrasal_main_block.find("div", {"class": "pos-header dpos-h"})
        uk_ipa, us_ipa = get_phonetics(phrasal_header_block, dictionary_index)

        pos_block = phrasal_header_block.find("span", {"class": "pos dpos"})
        pos = "" if pos_block is None else pos_block.text

        m_level, m_labels_and_codes, m_region, m_usage, m_domain = get_labels(phrasal_header_block)
        parsed_word_block = phrasal_main_block.find("h2", {"class": "headword"})  # tw-bw dhw dpos-h_hw
        if parsed_word_block is None:
            return {}
        else:
            parsed_word = parsed_word_block.text
        for def_block in phrasal_main_block.find_all("div", {"class": "sense-body dsense_b"}):
            phrasal_definition_found_1 = def_block.find("div", {"class": "ddef_h"})
            if phrasal_definition_found_1 is not None:
                tags_section = phrasal_definition_found_1.find("span", {"class": "def-info ddef-info"})

                # Gathering specific tags for every word usage
                level, labels_and_codes, region, usage, domain = get_labels(tags_section)
                current_word_level = tag_concatenation(m_level, level)
                current_word_labels_and_codes = tag_concatenation(m_labels_and_codes, labels_and_codes)
                current_word_region = tag_concatenation(m_region, region)
                current_word_usage = tag_concatenation(m_usage, usage)
                current_word_domain = tag_concatenation(m_domain, domain)

                phrasal_definition_found_2 = phrasal_definition_found_1.find("div", {'class': "def ddef_d db"})
            else:
                phrasal_definition_found_2 = None

            phrasal_definition = "" if phrasal_definition_found_2 is None else phrasal_definition_found_2.text

            # sentence examples
            sentence_block_list = def_block.find("div", {"class": "def-body ddef_b"})
            sentence_block_list = [] if sentence_block_list is None else sentence_block_list.find_all(
                "div",
                {"class": "examp dexamp"})
            phrasal_sentences = []

            if len(sentence_block_list) != 0:
                for item in sentence_block_list:
                    sent_ex = item.text.strip()
                    phrasal_sentences.append(sent_ex)

            if phrasal_idiom_word_info.get(parsed_word) is None or phrasal_idiom_word_info[parsed_word].get(pos) is None:
                if phrasal_idiom_word_info.get(parsed_word) is None:
                    phrasal_idiom_word_info[parsed_word] = {}
                phrasal_idiom_word_info[parsed_word][pos] = {"definitions": [phrasal_definition], "examples": [phrasal_sentences],
                                               "level": [current_word_level],
                                               "labels_and_codes": [current_word_labels_and_codes],
                                               "region": [current_word_region],
                                               "usage": [current_word_usage],
                                               "domain": [current_word_domain],
                                               "UK IPA": uk_ipa,
                                               "US IPA": us_ipa}
            else:
                phrasal_idiom_word_info[parsed_word][pos]["definitions"].append(phrasal_definition)
                phrasal_idiom_word_info[parsed_word][pos]["examples"].append(phrasal_sentences)
                phrasal_idiom_word_info[parsed_word][pos]["level"].append(current_word_level)
                phrasal_idiom_word_info[parsed_word][pos]["labels_and_codes"].append(current_word_labels_and_codes)
                phrasal_idiom_word_info[parsed_word][pos]["region"].append(current_word_region)
                phrasal_idiom_word_info[parsed_word][pos]["usage"].append(current_word_usage)
                phrasal_idiom_word_info[parsed_word][pos]["domain"].append(current_word_domain)
    return phrasal_idiom_word_info


def parse(word, dictionary_index=0, headers=headers):
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
    page = requests.get(link, headers=headers)
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
        parsed_word_block = header_block.find("span", {"class": "hw dhw"})

        uk_ipa, us_ipa = get_phonetics(header_block, dictionary_index)

        pos_block = header_block.find("span", {"class": "pos dpos"})
        pos = "" if pos_block is None else pos_block.text
        # data gathered from the word header
        m_level, m_labels_and_codes, m_region, m_usage, m_domain = get_labels(header_block)

        def_block_list = entity.find_all("div", {'class': 'def-block ddef_block'})
        if len(def_block_list) != 0:
            for def_block in def_block_list:
                definition_found_1 = def_block.find("div", {"class": "ddef_h"})
                if definition_found_1 is not None:
                    tags_section = definition_found_1.find("span", {"class": "def-info ddef-info"})

                    # Gathering specific tags for every word usage
                    level, labels_and_codes, region, usage, domain = get_labels(tags_section)
                    current_word_level = tag_concatenation(m_level, level)
                    current_word_labels_and_codes = tag_concatenation(m_labels_and_codes, labels_and_codes)
                    current_word_region = tag_concatenation(m_region, region)
                    current_word_usage = tag_concatenation(m_usage, usage)
                    current_word_domain = tag_concatenation(m_domain, domain)

                    # Phrase-block checking
                    # The reason for this is that on website there are two different tags for phrase-blocks
                    phrase_block = definition_found_1.find_parent("div",
                                                               {"class": "pr phrase-block dphrase-block"})

                    if phrase_block is not None:
                        parsed_word = phrase_block.find("span",
                                                        {"class": "phrase-title dphrase-title"}).text
                    else:
                        phrase_block_2 = definition_found_1.find_parent("div",
                                                                     {"class": "pr phrase-block dphrase-block lmb-25"})
                        if phrase_block_2 is not None:
                            parsed_word = phrase_block_2.find("span",
                                                              {"class": "phrase-title dphrase-title"}).text
                        else:
                            parsed_word = word if parsed_word_block is None else parsed_word_block.text

                    definition_found_2 = definition_found_1.find("div", {'class': "def ddef_d db"})
                else:
                    definition_found_2 = None

                definition = "" if definition_found_2 is None else definition_found_2.text

                # sentence examples
                sentence_block_list = def_block.find("div", {"class": "def-body ddef_b"})
                sentence_block_list = [] if sentence_block_list is None else sentence_block_list.find_all(
                    "div",
                    {"class": "examp dexamp"})
                sentences = []

                if len(sentence_block_list) != 0:
                    for item in sentence_block_list:
                        sent_ex = item.text.strip()
                        sentences.append(sent_ex)

                if word_info.get(parsed_word) is None or word_info[parsed_word].get(pos) is None:
                    if word_info.get(parsed_word) is None:
                        word_info[parsed_word] = {}
                    word_info[parsed_word][pos] = {"definitions": [definition], "examples": [sentences],
                                              "level": [current_word_level],
                                              "labels_and_codes": [current_word_labels_and_codes],
                                              "region": [current_word_region],
                                              "usage": [current_word_usage],
                                              "domain": [current_word_domain],
                                              "UK IPA": uk_ipa,
                                              "US IPA": us_ipa}
                else:
                    word_info[parsed_word][pos]["definitions"].append(definition)
                    word_info[parsed_word][pos]["examples"].append(sentences)
                    word_info[parsed_word][pos]["level"].append(current_word_level)
                    word_info[parsed_word][pos]["labels_and_codes"].append(current_word_labels_and_codes)
                    word_info[parsed_word][pos]["region"].append(current_word_region)
                    word_info[parsed_word][pos]["usage"].append(current_word_usage)
                    word_info[parsed_word][pos]["domain"].append(current_word_domain)

    phrasal_word_info = find_phrasal(word, soup, dictionary_index)
    word_info.update(phrasal_word_info)
    return word_info
