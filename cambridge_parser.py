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
        tags = []
        if block is not None:
            found_tags = block.find_all(html_tag, params)
            for tag in found_tags:
                tag_grandparent = tag.parent.parent.get("class")
                # var - var dvar; group - inf-group dinfg
                if not any("var" in x or "group" in x for x in tag_grandparent):
                    tag_text = tag.text.strip()
                    if tag_text:
                        tags.append(tag_text)
        return tags

    level = find_all_tags("span", {"class": "epp-xref"})
    labels_and_codes = find_all_tags("span", {"class": "gram dgram"})
    region = find_all_tags("span", {"class": "region dregion"})
    usage = find_all_tags("span", {"class": "usage dusage"})
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
    if header_block is not None:
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
            ipa = header_block.find_all("span", {"class": "pron dpron"})
            for child in ipa:
                ipa_parent = child.parent.get("class")
                if flag == 0:
                    if ipa_parent == ["uk", "dpron-i"]:
                        uk_ipa = [child.text.strip()]
                        flag = 1
                elif flag == 1:
                    if ipa_parent != ["us", "dpron-i"]:
                        uk_ipa += [child.text.strip()]
                    else:
                        us_ipa = [child.text.strip()]
                        flag = 2
                else:
                    if ipa_parent is None:
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
    return result_word_level, result_word_labels_and_codes, result_word_region, result_word_usage, result_word_domain


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


def get_alt_terms(alt_terms_block):
    """
    :param alt_terms_block
    :return:
    """
    alt_terms = []
    if alt_terms_block is not None:
        var_block = alt_terms_block.find_all("span", {"class": "var dvar"})
        var_block.extend(alt_terms_block.find_all("span", {"class": "spellvar dspellvar"}))

        for alt_term in var_block:
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
        main_block.extend(primal_block[dictionary_index].find_all("div", {"class": "pv-block"}))
        main_block.extend(primal_block[dictionary_index].find_all("div", {"class": "pr idiom-block"}))
    else:
        return {}

    for entity in main_block:
        header_block = entity.find("span", {"class": "di-info"})
        if header_block is None:
            header_block = entity.find("div", {"class": "pos-header dpos-h"})
        m_alt_terms_list = get_alt_terms(header_block)

        parsed_word_block = entity.find("h2", {"class": "headword"})
        if parsed_word_block is None:
            parsed_word_block = header_block.find("span", {"class": "hw dhw"}) if header_block is not None else None
        parsed_word = parsed_word_block.text.strip() if parsed_word_block is not None else ""

        pos_block = header_block.find("span", {"class": "pos dpos"}) if header_block is not None else None
        pos = "idiom" if pos_block is None else pos_block.text.strip()

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
            alt_terms_list = []
            current_word_level = []
            current_word_labels_and_codes = []
            current_word_region = []
            current_word_usage = []
            current_word_domain = []

            if found_definition_block is not None:
                found_definition_string = found_definition_block.find("div", {'class': "def ddef_d db"})
                definition = "" if found_definition_string is None else found_definition_string.text.strip(": ")

                # Gathering specific tags for every word usage
                tag_section = found_definition_block.find("span", {"class": "def-info ddef-info"})
                current_word_level, current_word_labels_and_codes, current_word_region, current_word_usage, current_word_domain = \
                    concatenate_tags(tag_section, m_level, m_labels_and_codes, m_region, m_usage, m_domain)

                alt_terms_list = get_alt_terms(found_definition_block)

                # Phrase-block checking
                # The reason for this is that on website there are two different tags for phrase-blocks
                phrase_block = found_definition_block.find_parent("div", {"class": "pr phrase-block dphrase-block"})
                if phrase_block is None:
                    phrase_block = found_definition_block.find_parent("div",
                                                                      {"class": "pr phrase-block dphrase-block lmb-25"})
                if phrase_block is not None:
                    phrase_tags_section = phrase_block.find("span", {"class": "phrase-info dphrase-info"})
                    if phrase_tags_section is not None:
                        alt_terms_list += get_alt_terms(phrase_tags_section)
                        current_word_level, current_word_labels_and_codes, current_word_region, current_word_usage, current_word_domain = \
                            concatenate_tags(phrase_tags_section, current_word_level, current_word_labels_and_codes, current_word_region, current_word_usage, current_word_domain)
                    parsed_word = phrase_block.find("span",
                                                    {"class": "phrase-title dphrase-title"}).text.strip()

            update_word_dict(word_info, word=parsed_word, pos=pos, definition=definition,
                             alt_terms_list=m_alt_terms_list + alt_terms_list, sentences=sentences, level=current_word_level,
                             labels_and_codes=current_word_labels_and_codes, region=current_word_region,
                             usage=current_word_usage, domain=current_word_domain, image_link=image_link,
                             uk_ipa=uk_ipa, us_ipa=us_ipa, uk_audio_link=uk_audio_link, us_audio_link=us_audio_link)
    return word_info


if __name__ == "__main__":
    from pprint import pprint
    pprint(define("born and bred"))
